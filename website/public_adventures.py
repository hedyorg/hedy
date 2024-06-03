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

    @route("/", methods=["GET"])
    @route("/filter", methods=["GET"])
    @requires_teacher
    def filtering(self, user):
        level = request.args["level"] if request.args.get("level") else "1"
        page = request.args.get('page')
        language = request.args.get("lang")
        # This is needed to differentiate between getting the PA page,
        # or merely filtering, since we only update the filters and content
        # and not the whole page.
        filtering = request.path.split("/")[-1] == "filter"
        if language == "reset":
            language = ""
        elif not language and not filtering:
            language = g.lang
        tag = request.args.get("tag", "")
        search = request.form.get("search", request.args.get("search", ""))

        tags = []
        if tag:
            toReset = request.args.get("reset")
            if toReset:
                # then it's the current selected tags, so remove current's tag
                tags = [_tag for _tag in toReset.split(",") if _tag != tag]
            else:
                tags = tag.split(",")
            tags = [t for t in tags if t]

        # Get all possible filters
        available_levels, available_languages, available_tags = self.db.get_public_adventure_filters()

        customizations = {"available_levels": sorted(available_levels, key=lambda x: int(x))}

        # Get public adventures.
        adventures, prev_page_token, next_page_token = self.db.get_public_adventures(level, language, tags, page)

        initial_tab = None
        initial_adventure = None
        commands = {}
        prev_level = None
        next_level = None

        customized_adventures = []
        included = {}
        for adventure in adventures.values():
            content = safe_format(adventure.get('formatted_content', adventure['content']),
                                  **hedy_content.KEYWORDS.get(g.keyword_lang))
            current_adventure = {
                "id": adventure.get("id"),
                "name": adventure.get("name"),
                "short_name": adventure.get("name"),
                "author": adventure.get("author", adventure["creator"]),
                "creator": adventure.get("creator"),
                "date": utils.localized_date_format(adventure.get("date")),
                "level": adventure.get("level"),
                "levels": adventure.get("levels"),
                "language": adventure.get("language", g.lang),
                "cloned_times": adventure.get("cloned_times"),
                "tags": adventure.get("tags", []),
                "text": content,
                "is_teacher_adventure": True,
            }
            # this happens if teacher1 clones an adventure from teacher2, same name different creator.
            # show only the cloned ones.
            adv_name = current_adventure["name"]
            if included.get(adv_name):
                if included[adv_name]["creator"] != user["username"]:
                    customized_adventures.remove(included[adv_name])
                else:
                    continue

            customized_adventures.append(current_adventure)
            included[current_adventure["name"]] = current_adventure

        adventures = sorted(customized_adventures, key=lambda adv: adv["name"])
        if adventures:
            initial_tab = adventures[0]["name"]
            initial_adventure = adventures[-1]

            # Add the commands to enable the language switcher dropdown
            commands = hedy.commands_per_level.get(level)
            if customizations["available_levels"]:
                prev_level, next_level = utils.find_prev_next_levels(list(customizations["available_levels"]), level)

        js = dict(
            page='code',
            lang=g.lang,
            level=level,
            adventures=adventures,
            initial_tab='',
            current_user_name=user['username'],
        )

        temp = render_template(
            f"public-adventures/{'index' if filtering else 'index'}.html",
            adventures=adventures,
            teacher_adventures=adventures,
            available_languages=available_languages,
            available_tags=available_tags,
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
            prev_page_token=prev_page_token,
            next_page_token=next_page_token,

            customizations=customizations,

            public_adventures_page=True,
            javascript_page_options=js,
        )

        response = make_response(temp)
        response.headers["HX-Trigger-After-Settle"] = json.dumps({"updateTSCode": js})
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

        # TODO: add achievement
        return render_partial('htmx-adventure-card.html', user=user, adventure=adventure, level=level,)
