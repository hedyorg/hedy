import uuid
import time
from functools import lru_cache
from flask import g, request, make_response
from website.flask_helpers import gettext_with_fallback as _
import json
import bs4

import hedy_content
import utils
from website.auth import requires_teacher
from website.flask_helpers import render_template
from jinja_partials import render_partial

from . import dynamo
from .database import Database
from .website_module import WebsiteModule, route
from safe_format import safe_format

# For now, hardcoded limits for how often an adventure has to be cloned to
# qualify for stars.
CLONED_STARS_THRESHOLDS = [5, 10, 50, 100, 500]


class PublicAdventuresModule2(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("public_adventures", __name__, url_prefix="/public-adventures")
        self.db = db

    def all_tags(self):
        return self._all_tags(get_ttl_hash(300))

    @lru_cache(maxsize=1)
    def _all_tags(self, _ttl_hash):
        """Uncached version of `all_tags`. ttl_hash is unused but exists to make the arguments unique for lru_cache."""
        return list(sorted(self.db.get_public_adventures_tags()))

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

        adventures = [self.enhance_adventure_for_list(a) for a in adventures]

        template = "body" if is_hx_request() else "index"

        return render_template(f"public-adventures/{template}.html",
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
            page_title=_("title_public-adventures"),
        )

    def enhance_adventure_for_list(self, adventure):
        """For each adventure in the list, add some extra information."""
        if 'levels' not in adventure:
            adventure['levels'] = [adventure.get('level', '1')]
        adventure['tags'] = list(sorted(adventure.get('tags', [])))
        adventure['cloned_stars'] = cloned_times_to_stars(adventure.setdefault('cloned_times', 0))
        adventure['creator'] = adventure.get('creator', adventure.get('username'))
        adventure['solution_example'] = adventure.get('solution_example', '').strip()

        # The solution_example is already HTML, with keyword markers. If it is empty HTML, remove it. If it is non-empty
        # HTML, render the keywords to the current language.
        if bs4.BeautifulSoup(adventure['solution_example'], 'html.parser').text.strip() == '':
            adventure['solution_example'] = ''
        else:
            adventure['solution_example'] = hedy_content.try_render_keywords(adventure['solution_example'], g.keyword_lang)

        return adventure

    @route("/preview/<adventure_id>", methods=["GET"])
    @requires_teacher
    def preview_adventure(self, user, adventure_id):
        adventure = self.db.get_adventure(adventure_id)

        # Confirm that we're not trying to sneak peek at a non-public adventure
        if not adventure.get('public'):
            return utils.error_page(error=404, ui_message=_("no_such_adventure"))

        adventure = self.format_adventure_for_preview(adventure)
        level=int(adventure.get('level', 1))

        response = make_response(
                        render_template("public-adventures/htmx-preview-adventure.html",
                               adventure=adventure,
                               user=user,
                               current_page="public-adventures",

                               # The next bits are to make the editor work
                               level=level
                               ), 200)

        # Activate some JavaScript on the client to make parts of the page dynamic
        response.headers["HX-Trigger-After-Settle"] = json.dumps({
            # public-adventures.ts
            'updateTSCode': dict(
                page='code',
                lang=g.lang,
                level=level,
                adventures=[],
                initial_tab='',
                current_user_name=user['username'],
            ),
        })
        return response

    def format_adventure_for_preview(self, adventure):
        """Given a database adventure, return a representation for preview."""
        adventure = self.enhance_adventure_for_list(adventure)

        public_profile = self.db.get_public_profile_settings(adventure.get('creator'))

        content = safe_format(adventure.get('formatted_content', adventure['content']),
                                **hedy_content.KEYWORDS.get(g.keyword_lang))

        return dict(adventure,
                    short_name=adventure.get('name'),
                    author=adventure.get("author", adventure["creator"]),
                    creator_public_profile=public_profile,
                    date=utils.localized_date_format(adventure.get("date")),
                    text=content,
                    is_teacher_adventure=True,
                    flagged=adventure.get("flagged", 0))

    @route("/clone/<adventure_id>", methods=["POST"])
    @requires_teacher
    def clone_adventure(self, user, adventure_id):
        current_adventure = self.db.get_adventure(adventure_id)
        if not current_adventure:
            return utils.error_page(error=404, ui_message=_("no_such_adventure"))
        elif current_adventure["creator"] == user["username"]:
            return render_template("public-adventures/htmx-after-clone.html",
                                    adventure=current_adventure,
                                    message=_('adventure_duplicate'))

        adventures = self.db.get_teacher_adventures(user["username"])
        for adventure in adventures:
            if adventure["name"] == current_adventure["name"]:
                return render_template("public-adventures/htmx-after-clone.html",
                                       adventure=adventure,
                                       message=_('adventure_duplicate'))

        level = current_adventure.get("level")
        adventure = {
            "id": uuid.uuid4().hex,
            "cloned_from": adventure_id,
            "name": current_adventure.get("name"),
            "content": current_adventure.get("content"),

            # Crucially, a cloned public adventure is not necessarily automatically public
            "public": 0,

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

        self.db.update_adventure(adventure_id, {"cloned_times": dynamo.DynamoIncrement(1)})
        self.db.store_adventure(adventure)
        return render_template("public-adventures/htmx-after-clone.html",
                                adventure=adventure,
                                message=_('adventure_cloned'))

    @route("/flag/<adventure_id>/<flagged>", methods=["POST"])
    @requires_teacher
    def flag_adventure(self, user, adventure_id, flagged=None):
        self.db.update_adventure(adventure_id, {"flagged": 0 if int(flagged) else 1})
        return render_template("public-adventures/htmx-after-flag.html")


def is_hx_request():
    return bool(request.headers.get('Hx-Request'))


def get_ttl_hash(seconds=3600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)

def cloned_times_to_stars(times):
    for i, threshold in reversed(list(enumerate(CLONED_STARS_THRESHOLDS))):
        if times >= threshold:
            return i + 1
    return 0