import uuid
from flask import g, request, make_response
from flask_babel import gettext
import json

import hedy
import hedy_content
import utils
from config import config
from website.auth import requires_teacher
from website.flask_helpers import render_template
from jinja_partials import render_partial

from .achievements import Achievements
from .database import Database
from .website_module import WebsiteModule, route
from safe_format import safe_format

cookie_name = config["session"]["cookie_name"]
invite_length = config["session"]["invite_length"] * 60


class PublicAdventuresModule(WebsiteModule):
    def __init__(self, db: Database, achievements: Achievements):
        super().__init__("public_adventures", __name__, url_prefix="/public-adventures")

        self.db = db
        self.achievements = achievements
        self.adventures = {}
        self.customizations = {"available_levels": set()}
        self.available_languages = set()
        self.available_tags = set()

    def init(self, user):
        included = {}
        self.adventures = {}
        self.available_languages = set()
        self.available_tags = set()

        public_adventures = self.db.get_public_adventures()
        public_adventures = sorted(public_adventures, key=lambda a: a["creator"] == user["username"], reverse=True)
        for adventure in public_adventures:
            adv_lang = adventure.get("language", g.lang)
            adv_tags = adventure.get("tags", [])
            self.available_languages.update([adv_lang])
            self.available_tags.update(adv_tags)
            # NOTE: what if another author has an adventure with the same name?
            # Perhaps we could make this name#creator!
            if included.get(adventure["name"]):
                continue
            public_profile = self.db.get_public_profile_settings(adventure.get('creator'))
            included[adventure["name"]] = True

            content = safe_format(adventure.get('formatted_content', adventure['content']),
                                  **hedy_content.KEYWORDS.get(g.keyword_lang))
            current_adventure = {
                "id": adventure.get("id"),
                "name": adventure.get("name"),
                "short_name": adventure.get("name"),
                "author": adventure.get("author", adventure["creator"]),
                "creator": adventure.get("creator"),
                "creator_public_profile": public_profile,
                "date": utils.localized_date_format(adventure.get("date")),
                "level": adventure.get("level"),
                "levels": adventure.get("levels"),
                "language": adv_lang,
                "cloned_times": adventure.get("cloned_times"),
                "tags": adv_tags,
                "text": content,
                "is_teacher_adventure": True,
            }

            # save adventures for later usage.
            for _level in adventure.get("levels", [adventure.get("level")]):
                _level = int(_level)
                if self.adventures.get(_level):
                    self.adventures[_level].append(current_adventure)
                else:
                    self.adventures[_level] = [current_adventure]

            available_levels = adventure["levels"] if adventure.get("levels") else [adventure["level"]]
            self.customizations["available_levels"].update([int(adv_level) for adv_level in available_levels])

    @route("/", methods=["GET"])
    @route("/filter", methods=["POST"])
    @requires_teacher
    def filtering(self, user, index_page=False):
        index_page = request.method == "GET"

        level = int(request.args["level"]) if request.args.get("level") else 1
        language = request.args.get("lang", "")
        tag = request.args.get("tag", "")
        search = request.form.get("search", request.args.get("search", ""))
        if index_page or not self.adventures or not self.adventures.get(level):
            self.init(user)

        adventures = self.adventures.get(level, [])
        # adjust available filters for the selected level.
        self.update_filters(adventures, "tag")
        self.update_filters(adventures, "lang")
        # In case a selected set of adventures doesn't have the given lang to filter on,
        # we decide that that language cannot be used for filtering.
        if not any(adv.get("language") == language for adv in adventures):
            language = ""

        if language:
            if language != "rest":
                adventures = [adv for adv in adventures if adv.get("language") == language]
            else:
                language = ""
            # adjust available tags after fitlering on languages.
            self.update_filters(adventures, "tag")

        tags = []
        if tag:
            toReset = request.args.get("reset")
            if toReset:
                # then it's the current selected tags, so remove current's tag
                tags = [_tag for _tag in toReset.split(",") if _tag != tag]
            else:
                tags = tag.split(",")

            tags = [_tag for _tag in tags if _tag]  # filter out empty strings.
            for _tag in tags:
                # In case a selected set of adventures doesn't have the given tag to filter on,
                # we decide that that tag cannot be used for filtering.
                if not any(_tag in adv.get("tags") for adv in adventures):
                    tags.remove(_tag)
            if tags:
                adventures = [adv for i, adv in enumerate(adventures) if any(tag in tags for tag in adv.get("tags"))]
            # adjust available languages after fitlering on tags.
            self.update_filters(adventures, "lang")

        if search:
            adventures = [adv for adv in adventures if search.lower() in adv.get("name").lower()]
            self.update_filters(adventures, "lang")
            self.update_filters(adventures, "tag")

        initial_tab = None
        initial_adventure = None
        commands = {}
        prev_level = None
        next_level = None
        if adventures:
            initial_tab = adventures[0]["name"]
            initial_adventure = adventures[-1]

            # Add the commands to enable the language switcher dropdown
            commands = hedy.commands_per_level.get(level)
            prev_level, next_level = utils.find_prev_next_levels(list(self.customizations["available_levels"]), level)

        js = dict(
            page='code',
            lang=g.lang,
            level=level,
            adventures=adventures,
            initial_tab='',
            current_user_name=user['username'],
        )

        temp = render_template(
            "public-adventures/index.html" if index_page else "public-adventures/body.html",
            adventures=adventures,
            teacher_adventures=adventures,
            available_languages=self.available_languages,
            available_tags=self.available_tags,
            selectedLevel=level,
            selectedLang=language,
            # selectedTag=",".join(self.selectedTag),
            selectedTag=",".join(tags),
            currentSearch=search,

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
            javascript_page_options=js,
        )

        response = make_response(temp)
        response.headers["HX-Trigger"] = json.dumps({"updateTSCode": js})
        return response

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
                    break
        # TODO: add achievement
        return render_partial('htmx-adventure-card.html', user=user, adventure=adventure, level=level,)

    def update_filters(self, adventures,  to_filter):
        if to_filter == 'lang':
            self.available_languages = set()
        else:
            self.available_tags = set()
        for adventure in adventures:
            if to_filter == 'lang':
                adv_lang = adventure.get("language", g.lang)
                self.available_languages.update([adv_lang])
            else:
                adv_tags = adventure.get("tags", [])
                self.available_tags.update(adv_tags)
