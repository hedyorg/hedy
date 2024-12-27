import uuid
import time
from functools import lru_cache
from flask import g, request, make_response
from website.flask_helpers import gettext_with_fallback as gettext
import json

import hedy
import hedy_content
import utils
from website.auth import requires_teacher
from website.flask_helpers import render_template
from jinja_partials import render_partial

from .database import Database
from .website_module import WebsiteModule, route
from safe_format import safe_format


class PublicAdventuresModule2(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("public_adventures2", __name__, url_prefix="/public-adventures2")
        self.db = db

    def all_tags(self):
        return self._all_tags(get_ttl_hash(300))

    @lru_cache(maxsize=1)
    def _all_tags(self, _ttl_hash):
        """Uncached version of `all_tags`. ttl_hash is unused but exists to make the arguments unique for lru_cache."""
        return list(sorted(self.db.get_public_adventures_tags()))

    def init(self, user):
        included = {}

        public_adventures = self.db.get_public_adventures()
        public_adventures = sorted(public_adventures, key=lambda a: a["creator"] == user["username"], reverse=True)
        for adventure in public_adventures:
            # The adventure lang can be None if it is not set
            adv_lang = adventure.get("language")
            if adv_lang:
                self.available_languages.update([adv_lang])
            adv_tags = adventure.get("tags", [])
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
                "flagged": adventure.get("flagged", 0),
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
    @requires_teacher
    def search(self, user):
        """Render the search page including the form."""

        # Input arguments
        selected_level = request.args.get("selected_level", '')
        selected_lang = request.args.get("selected_lang", g.lang)
        q = request.args.get("q", "")
        selected_tag = request.args.get("selected_tag")
        page = request.args.get("page", '')

        # Dropbox options
        available_languages = hedy_content.ALL_LANGUAGES.keys()
        available_levels = list(range(1, hedy_content.MAX_LEVEL + 1))
        available_tags = self.all_tags()

        # Search results
        adventures = self.db.get_public_adventures_filtered(selected_lang, int(selected_level) if selected_level else None, selected_tag or None, q or None, pagination_token=page if page else None)
        next_page_token = adventures.next_page_token
        prev_page_token = adventures.prev_page_token

        adventures = [self.enhance_adventure(a) for a in adventures]

        template = "body" if is_hx_request() else "index"

        return render_template(f"public-adventures2/{template}.html",
            available_languages=available_languages,
            available_levels=available_levels,
            available_tags=available_tags,
            selected_level=selected_level,
            selected_lang=selected_lang,
            selected_tag=selected_tag,
            q=q,
            page=page,

            adventures=adventures,
            next_page_token=next_page_token,
            prev_page_token=prev_page_token,

            user=user,
            current_page="public-adventures",
            page_title=gettext("title_public-adventures"),
        )

        response = make_response(temp, 200)
        # response.headers["HX-Trigger"] = json.dumps({"updateTSCode": js})
        return response

    def enhance_adventure(self, adventure):
        """For each adventure, add some extra information."""
        if 'levels' not in adventure:
            adventure['levels'] = [adventure.get('level', '1')]
        adventure['tags'] = list(sorted(adventure.get('tags', [])))
        return adventure

    @route("/preview/<adventure_id>", methods=["GET"])
    @requires_teacher
    def preview_adventure(self, user, adventure_id):
        adventure = self.db.get_adventure(adventure_id)

        # Confirm that we're not trying to sneak peek at a non-public adventure
        if not adventure.get('public'):
            return utils.error_page(error=404, ui_message=gettext("no_such_adventure"))

        return render_template("public-adventures2/htmx-preview-adventure.html",
                               adventure=adventure,
                               user=user,
                               current_page="public-adventures")

    @route("/clone/<adventure_id>", methods=["POST"])
    @requires_teacher
    def clone_adventure(self, user, adventure_id):
        # TODO: perhaps get it from self.adventures
        current_adventure = self.db.get_adventure(adventure_id)
        if not current_adventure:
            return utils.error_page(error=404, ui_message=gettext("no_such_adventure"))
        elif current_adventure["creator"] == user["username"]:
            return make_response(gettext("adventure_duplicate"), 400)

        adventures = self.db.get_teacher_adventures(user["username"])
        for adventure in adventures:
            if adventure["name"] == current_adventure["name"]:
                return make_response(gettext("adventure_duplicate"), 400)

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
            "solution_example": current_adventure.get("solution_example", ""),
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
        return render_partial('htmx-adventure-card.html', user=user, adventure=adventure, level=level,)

    def update_lang_filter(self, adventures):
        langs = [a['language'] for a in adventures if a.get('language')]
        self.available_languages = set(langs)

    def update_tag_filter(self, adventures):
        tags = [t for a in adventures for t in a.get('tags', [])]
        self.available_tags = set(tags)

    @route("/flag/<adventure_id>", methods=["POST"])
    @route("/flag/<adventure_id>/<flagged>", methods=["POST"])
    @requires_teacher
    def flag_adventure(self, user, adventure_id, flagged=None):
        self.db.update_adventure(adventure_id, {"flagged": 0 if int(flagged) else 1})
        return gettext("adventure_flagged"), 200


def is_hx_request():
    return bool(request.headers.get('Hx-Request'))


def get_ttl_hash(seconds=3600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)