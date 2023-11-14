import copy
import uuid
from flask_babel import gettext

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

    @route("/", methods=["GET"])
    @requires_teacher
    def index(self, user):
        public_adventures = self.db.get_public_adventures()
        adventures = []
        for adventure in public_adventures:
            adventures.append(
                {
                    "id": adventure.get("id"),
                    "name": adventure.get("name"),
                    "creator": adventure.get("creator"),
                    "date": utils.localized_date_format(adventure.get("date")),
                    "level": adventure.get("level"),
                    "language": adventure.get("language", ""),
                    "tags": adventure.get("tags", []),
                }
            )
        adventures = sorted(adventures, key=lambda a: a["creator"] == user["username"], reverse=True)

        available_languages = set([adv["language"] for adv in adventures])
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

        adventure = copy.deepcopy(current_adventure)
        adventure["cloned_from"] = adventure["id"]
        adventure["id"] = uuid.uuid4().hex
        adventure["creator"] = user["username"]

        self.db.store_adventure(adventure)
        return {"id": adventure["id"]}, 200
        # return self.index()
