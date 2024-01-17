import uuid
from flask import g, request
from flask_babel import gettext

import hedy
import utils
from config import config
from website.auth import requires_teacher
from website.flask_helpers import render_template

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
        self.filtered_names = set()

    @route("/", methods=["GET"], defaults={'level': 1})
    @route("/<level>", methods=["GET"])
    @requires_teacher
    def index(self, user, level):
        self.filtered_names = set()
        public_adventures = self.db.get_public_adventures()
        public_adventures = sorted(public_adventures, key=lambda a: a["creator"] == user["username"], reverse=True)
        adventures = []
        available_languages = set()
        available_tags = set()
        for adventure in public_adventures:
            available_languages.update([adventure["language"]])
            available_tags.update(adventure["tags"])
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
            # save adventures for later usage.
            for _level in adventure.get("levels", [adventure.get("level")]):
                _level = int(_level)
                if self.adventures.get(_level):
                    self.adventures[_level].append(adventures[-1])
                else:
                    self.adventures[_level] = [adventures[-1]]

            available_levels = adventure["levels"] if adventure.get("levels") else [adventure["level"]]
            self.customizations["available_levels"].update([int(adv_level) for adv_level in available_levels])

        if not request.args.get("level"):
            level = 1
            adventures = self.adventures.get(level, [])
        else:
            level = int(request.args["level"])
            adventures = self.adventures.get(level, [])
        initial_tab = None
        initial_adventure = None
        if adventures:
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
            selectedLang=request.args.get("lang"),
            selectedTag=request.args.get("tag", []),
            currentSearch=request.args.get("search", ""),

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

            public_adventures_page=True,
            javascript_page_options=dict(
                page='code',
                lang=g.lang,
                level=level,
                adventures=adventures,
                initial_tab='',
                current_user_name=user['username'],
            ))

    @route("/filter", methods=["GET", "POST"])
    @requires_teacher
    def filtering(self, user,):
        level = int(request.args["level"]) if request.args.get("level") else 1
        language = request.args.get("lang")
        tags = request.args.get("tag")
        search = request.args.get("search")

        adventures = self.adventures.get(level, [])

        available_languages = set([adv["language"] for adv in adventures if adv["language"]])
        available_tags = set([tag for adv in adventures for tag in adv.get("tags", [])])

        if language:
            adventures = [adv for adv in adventures if adv.get("language") == language]
        if tags:
            tags = tags.split(",")
            adventures = [adv for i, adv in enumerate(adventures) if any(tag in tags for tag in adv.get("tags"))]

        if search:
            adventures = [adv for adv in adventures if search in adv.get("name")]

        initial_tab = None
        initial_adventure = None
        state_changed = True

        if adventures:
            new_filtered_names = {adv["name"] for adv in adventures}
            # Check if the filtered names are different from the last filter call
            state_changed = new_filtered_names != self.filtered_names
            self.filtered_names = new_filtered_names.copy()
            initial_tab = adventures[0]["name"]
            initial_adventure = adventures[-1]
        else:
            self.filtered_names = set()
        # Add the commands to enable the language switcher dropdown
        commands = hedy.commands_per_level.get(level)
        prev_level, next_level = utils.find_prev_next_levels(list(self.customizations["available_levels"]), level)

        return {
            "html": render_template(
                "public-adventures-body.html",
                adventures=adventures,
                teacher_adventures=adventures,
                available_languages=available_languages,
                available_tags=available_tags,
                selectedLevel=level,
                selectedTag=request.args.get("tag", []),

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

                public_adventures_page=True,
                customizations=self.customizations),

            "js": dict(
                page="code",
                lang=g.lang,
                level=level,
                adventures=adventures,
                initial_tab=initial_tab,
                current_user_name=user['username'],
                state_changed=state_changed,)
        }

    @route("/clone/<adventure_id>", methods=["POST"])
    @requires_teacher
    def clone_adventure(self, user, adventure_id):
        # TODO: perhaps get it from self.adventures
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
            "is_teacher_adventure": True,
        }

        self.db.update_adventure(adventure_id, {"cloned_times": current_adventure.get("cloned_times", 0) + 1})
        self.db.store_adventure(adventure)

        # update cloned adv. that's saved in this class
        for _level in current_adventure.get("levels", [level]):
            _level = int(_level)
            for i, adv in enumerate(self.adventures.get(_level, [])):
                if adv.get("id") == current_adventure.get("id"):
                    adventure["short_name"] = adventure.get("name")
                    adventure["text"] = adventure.get("content")
                    # Replace the old adventure with the new adventure
                    self.adventures[_level][i] = adventure
                    # del self.included[adventure.get("name")]
                    self.filtered_names = set()
                    break
        # TODO: add achievement
        return {"message": gettext("adventure_cloned")}
