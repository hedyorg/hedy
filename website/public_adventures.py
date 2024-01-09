import uuid
from flask import g
from flask_babel import gettext

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

    @route("/", methods=["GET"])
    @requires_teacher
    def index(self, user):
        public_adventures = self.db.get_public_adventures()
        public_adventures = sorted(public_adventures, key=lambda a: a["creator"] == user["username"], reverse=True)
        adventures = []
        included = {}
        for adventure in public_adventures:
            # NOTE: what if another author has an adventure with the same name? Perhaps we could make this name#creator!
            if included.get(adventure["name"]):
                continue
            public_profile = self.db.get_public_profile_settings(adventure.get('creator'))
            included[adventure["name"]] = True
            adventures.append(
                {
                    "id": adventure.get("id"),
                    "name": adventure.get("name"),
                    "author": adventure.get("author", adventure["creator"]),
                    "creator": adventure.get("creator"),
                    "creator_public_profile": public_profile,
                    "date": utils.localized_date_format(adventure.get("date")),
                    "level": adventure.get("level"),
                    "levels": adventure.get("levels"),
                    "language": adventure.get("language", g.lang),
                    "cloned_times": adventure.get("cloned_times"),
                    "tags": adventure.get("tags", []),
                }
            )

        available_languages = set([adv["language"] for adv in adventures if adv["language"]])
        available_tags = set([tag for adv in adventures for tag in adv.get("tags", [])])

        return render_template(
            "public-adventures.html",
            adventures=adventures,
            available_languages=available_languages,
            available_tags=available_tags,
            user=user,
            current_page="public-adventures",
            page_title=gettext("title_public-adventures"),
            javascript_page_options=dict(
                page='public-adventures',
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
