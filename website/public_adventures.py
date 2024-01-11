import uuid
from flask import g, request
from flask_babel import gettext

import hedy
import utils
from config import config
from website.auth import requires_teacher
from website.flask_helpers import render_template
from jinja_partials import render_partial

from .achievements import Achievements
from .database import Database
from .website_module import WebsiteModule, route

cookie_name = config["session"]["cookie_name"]
invite_length = config["session"]["invite_length"] * 60


class PublicAdventuresModule(WebsiteModule):
    def __init__(self, db: Database, achievements: Achievements):
        super().__init__("public_adventures", __name__, url_prefix="/public-adventures")

        self.db = db
        self.achievements = achievements
        self.initial_level = 1
        self.adventures = {}
        self.included = {}
        self.customizations = {"available_levels": set()}

    @route("/", methods=["GET"], defaults={'level': 1})
    @route("/<level>", methods=["GET"])
    @requires_teacher
    def index(self, user, level):
        if not request.args.get("level"):
            public_adventures = self.db.get_public_adventures()
            public_adventures = sorted(public_adventures, key=lambda a: a["creator"] == user["username"], reverse=True)
            adventures = []
            for adventure in public_adventures:
                # NOTE: what if another author has an adventure with the same name?
                # Perhaps we could make this name#creator!
                if self.included.get(adventure["name"]):
                    continue
                public_profile = self.db.get_public_profile_settings(adventure.get('creator'))
                self.included[adventure["name"]] = True
                adventures.append(
                    {
                        "id": adventure.get("id"),
                        "name": adventure.get("name"),
                        "short_name": adventure.get("name"),
                        "author": adventure.get("author", adventure["creator"]),
                        "creator": adventure.get("creator"),
                        "creator_public_profile": public_profile,
                        "date": utils.localized_date_format(adventure.get("date")),
                        "level": adventure.get("level"),
                        "levels": adventure.get("levels"),
                        "language": adventure.get("language", g.lang),
                        "cloned_times": adventure.get("cloned_times"),
                        "tags": adventure.get("tags", []),
                        "text": adventure.get("content"),
                        "is_teacher_adventure": True,
                        # "content": adventure.get("content")
                    }
                )
                print('\n\n\n\n\nadd now: ', adventure["name"])
                # save adventures for later usage.
                for _level in adventure.get("levels", [adventure.get("level")]):
                    _level = int(_level)
                    if self.adventures.get(_level):
                        self.adventures[_level].append(adventures[-1])
                    else:
                        self.adventures[_level] = [adventures[-1]]

                available_levels = adventure["levels"] if adventure.get("levels") else [adventure["level"]]
                self.customizations["available_levels"].update([int(adv_level) for adv_level in available_levels])
        else:
            level = request.args["level"]

        level = int(level)
        adventures = self.adventures[level]
        print("adventures \n\n", self.adventures)
        available_languages = set([adv["language"] for adv in adventures if adv["language"]])
        available_tags = set([tag for adv in adventures for tag in adv.get("tags", [])])

        initial_tab = adventures[0]["name"]
        initial_adventure = adventures[0]

        # Add the commands to enable the language switcher dropdown
        commands = hedy.commands_per_level.get(initial_adventure["level"])
        prev_level, next_level = utils.find_prev_next_levels(
            list(self.customizations["available_levels"]), int(initial_adventure["level"]))

        return render_template(
            "public-adventures.html",
            adventures=adventures,
            teacher_adventures=adventures,
            available_languages=available_languages,
            available_tags=available_tags,
            selectedLevel=level,

            user=user,
            current_page="public-adventures",
            page_title=gettext("title_public-adventures"),

            initial_adventure=initial_adventure,
            initial_tab=initial_tab,
            commands=commands,
            level=level,
            max_level=18,
            level_nr=str(level),
            prev_level=prev_level,
            next_level=next_level,

            customizations=self.customizations,

            javascript_page_options=dict(
                page='code',
                lang=g.lang,
                level=level,
                adventures=adventures,
                initial_tab='',
                current_user_name=user['username'],
            ))

    @route("/filter", methods=["GET"])
    @requires_teacher
    def filtering(self, user,):
        print("\n\nfilteringggggggg\n\n")
        level = int(request.args["level"]) if request.args.get("level") else 1
        language = request.args.get("adv-language")
        print(level, language)
        adventures = self.adventures[int(level)]
        available_languages = set([adv["language"] for adv in adventures if adv["language"]])
        available_tags = set([tag for adv in adventures for tag in adv.get("tags", [])])

        if language:
            # adventures = list(filter(lambda adv: adv.get("language") != language, adventures))
            adventures = [adv for adv in adventures if adv.get("language") == language]

        initial_tab = None
        initial_adventure = None
        if adventures:
            initial_tab = adventures[0]["name"]
            initial_adventure = adventures[-1]
        print(initial_adventure, initial_tab)
        # Add the commands to enable the language switcher dropdown
        commands = hedy.commands_per_level.get(level)
        prev_level, next_level = utils.find_prev_next_levels(list(self.customizations["available_levels"]), level)

        # return redirect(f"/public-adventures/{level}#language={language}")
        return render_partial(
            "public-adventures-body.html",
            adventures=adventures,
            teacher_adventures=adventures,
            available_languages=available_languages,
            available_tags=available_tags,
            selectedLevel=level,

            user=user,
            current_page="public-adventures-body",
            page_title=gettext("title_public-adventures"),

            initial_adventure=initial_adventure,
            initial_tab=initial_tab,
            commands=commands,
            level=level,
            level_nr=str(level),
            max_level=18,
            prev_level=prev_level,
            next_level=next_level,

            customizations=self.customizations,
            javascript_page_options=dict(
                lang=g.lang,
                level=level,
                adventures=adventures,
                initial_tab='',
                current_user_name=user['username'],
            ))

    @route("/clone/<adventure_id>", methods=["POST"])
    @requires_teacher
    def clone_adventure(self, user, adventure_id):
        current_adventure = self.db.get_adventure(adventure_id)
        if not current_adventure:
            return utils.error_page(error=404, ui_message=gettext("no_such_adventure"))
        elif current_adventure["creator"] == user["username"]:
            return gettext("adventure_duplicate"), 400

        adventures = self.db.get_teacher_adventures(user["username"])
        for adventure in adventures:
            if adventure["name"] == current_adventure["name"]:
                return gettext("adventure_duplicate"), 400

        level = current_adventure.get("level")
        adventure = {
            "id": uuid.uuid4().hex,
            "cloned_from": adventure_id,
            "name": current_adventure.get("name"),
            "content": current_adventure.get("content"),
            "public": 1,
            # creator here is the new owner; we don't change it to owner because that'd introduce many conflicts.
            # Instead handle it in html.
            "creator": user["username"],
            "author": current_adventure.get("creator"),
            "date": utils.timems(),
            "level": level,
            "levels": current_adventure.get("levels", [level]),
            "language": current_adventure.get("language", g.lang),
            "tags": current_adventure.get("tags", []),
        }

        self.db.update_adventure(adventure_id, {"cloned_times": current_adventure.get("cloned_times", 0) + 1})
        self.db.store_adventure(adventure)
        adventure["date"] = utils.localized_date_format(adventure.get("date"))
        return render_partial('htmx-adventure-card.html',
                              adventure=adventure,
                              user=user,)
