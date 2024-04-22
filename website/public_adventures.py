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

    @route("/", methods=["GET"])
    @route("/filter", methods=["POST"])
    @requires_teacher
    def filtering(self, user):
        level = request.args["level"] if request.args.get("level") else "1"
        language = request.args.get("lang")
        if language == "reset":
            language = ""
        elif not language and request.method == 'GET':
            language = g.lang
        tag = request.args.get("tag", "")
        search = request.form.get("search", request.args.get("search", ""))

        available_languages = set()
        available_levels = set()
        available_tags = set()

        # Get all possible filters
        field_filters = self.db.get_public_adventures_filters()

        available_levels.update(field_filters.get("level", []))
        available_languages.update(field_filters.get("lang", []))
        available_tags.update(field_filters.get("tag", []))

        customizations = {"available_levels": sorted(available_levels)}

        tags = []
        if tag:
            toReset = request.args.get("reset")
            if toReset:
                # then it's the current selected tags, so remove current's tag
                tags = [_tag for _tag in toReset.split(",") if _tag != tag]
            else:
                tags = tag.split(",")
            tags = [t for t in tags if t]

        # Get indexes
        level_adventure_ids = self.db.get_public_adventures_indexes({"field#value": f"level#{level}"})
        lang_adventure_ids = self.db.get_public_adventures_indexes({"field#value": f"lang#{language}"})
        tag_adventure_ids = set()
        for _t in tags:
            tag_adventure_ids.update(self.db.get_public_adventures_indexes({"field#value": f"tag#{_t}"}))

        lang_adventure_ids.intersection_update(level_adventure_ids)
        tag_adventure_ids.intersection_update(level_adventure_ids)
        adventure_ids = level_adventure_ids.union(lang_adventure_ids, tag_adventure_ids)

        adventures = self.db.batch_get_adventures(adventure_ids)

        initial_tab = None
        initial_adventure = None
        commands = {}
        prev_level = None
        next_level = None

        if adventures:
            adventures = list(adventures.values())
            initial_tab = adventures[0]["name"]
            initial_adventure = adventures[-1]

            # Add the commands to enable the language switcher dropdown
            commands = hedy.commands_per_level.get(level)
            if customizations["available_levels"]:
                prev_level, next_level = utils.find_prev_next_levels(list(customizations["available_levels"]), level)

            customized_adventures = []
            included = {}
            for adventure in adventures:
                if language and adventure.get("language", g.lang) != language:
                    continue
                if tags and not any(_t in adventure.get("tags", []) for _t in tags):
                    continue
                if search and not search.lower() in adventure.get("name").lower():
                    continue

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
            adventures = customized_adventures

        js = dict(
            page='code',
            lang=g.lang,
            level=level,
            adventures=adventures,
            initial_tab='',
            current_user_name=user['username'],
        )

        temp = render_template(
            f"public-adventures/{'index' if request.method == 'GET' else 'body'}.html",
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

            customizations=customizations,

            public_adventures_page=True,
            javascript_page_options=js,
        )

        response = make_response(temp)
        response.headers["HX-Trigger"] = json.dumps({"updateTSCode": js})
        return response

    @route("/filter-old", methods=["POST"])
    @requires_teacher
    def filtering_old(self, user, index_page=False):
        index_page = request.method == "GET"

        level = int(request.args["level"]) if request.args.get("level") else 1
        language = request.args.get("lang", "")
        tag = request.args.get("tag", "")
        search = request.form.get("search", request.args.get("search", ""))
        if index_page or not self.adventures or not self.adventures.get(level):
            print("\n\n\n GET IT MORE TIME!!\n\n", level, language, tag)
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
        self.db.update_public_adventure_filters_indexes(adventure)
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
