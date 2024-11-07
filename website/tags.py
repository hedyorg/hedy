from flask import make_response, request, g
from website.flask_helpers import gettext_with_fallback as gettext
import jinja_partials
import uuid

import utils
from config import config
from website.auth import requires_teacher
from .database import Database
from .website_module import WebsiteModule, route

cookie_name = config["session"]["cookie_name"]
invite_length = config["session"]["invite_length"] * 60


class TagsModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("tags", __name__, url_prefix="/tags")
        self.db = db

    @route("/<adventure_id>", methods=["GET"])
    @route("/", methods=["GET"], defaults={"adventure_id": None})
    @requires_teacher
    def get_public_tags(self, user, adventure_id):
        public_tags = self.db.read_public_tags()
        adventure_id = request.args.get("adventure_id")
        adventure = self.db.get_adventure(adventure_id)
        if adventure:
            # exclude current adventure's tags
            public_tags = list(filter(lambda t: t["name"] not in adventure.get("tags", []), public_tags))

        return jinja_partials.render_partial('htmx-tags-dropdown.html',
                                             tags=public_tags, adventure_id=adventure_id, creator=user)

    @route("/create/<adventure_id>", methods=["POST"])
    @route("/create/<adventure_id>/<new_tag>", methods=["POST"])
    @requires_teacher
    def create(self, user, adventure_id, new_tag=None):
        new_tag = new_tag or request.form.get("tag")
        if not new_tag:
            return utils.error_page(error=400, ui_message=gettext("no_tag"))
        if not adventure_id:
            return utils.error_page(error=400, ui_message=gettext("retrieve_adventure_error"))

        tag_name = new_tag.strip()
        db_adventure = self.db.get_adventure(adventure_id)

        if not db_adventure:
            return make_response(gettext("not_adventure_yet"), 400)
        public = request.args.get("public", db_adventure.get("public", False))
        language = request.args.get("language", db_adventure.get("language", g.lang))

        adventure_tags = db_adventure.get("tags", [])
        if tag_name not in adventure_tags:
            adventure_tags.append(tag_name)
            adventure_tags = sorted(adventure_tags, key=lambda tag: tag)
            self.db.update_adventure(adventure_id, {"tags": adventure_tags})
        else:
            return make_response(gettext("tag_in_adventure"), 400)

        db_tag = self.db.read_tag(tag_name)
        if not db_tag:
            tagged_in = [{"id": adventure_id, "public": public, "language": language, }]
            db_tag = {
                "id": uuid.uuid4().hex,
                "name": tag_name,
                "tagged_in": tagged_in,
                "popularity": 1,
            }
            self.db.create_tag(db_tag)
        else:
            tagged_in = db_tag["tagged_in"]
            tagged_in.append({"id": adventure_id, "public": public, "language": language, })
            self.db.update_tag(db_tag["id"], {"tagged_in": tagged_in, "popularity": db_tag["popularity"] + 1})

        return jinja_partials.render_partial('htmx-tags-list.html', tags=adventure_tags,
                                             adventure_id=adventure_id, creator=user["username"])

    @route("/update/<tag>/<adventure_id>", methods=["PUT"])
    def update(self, tag, adventure_id):
        # TODO: allow admin to update tags.
        pass

    @route("/delete/<tag>/<adventure_id>", methods=["DELETE"])
    @requires_teacher
    def delete_from_adventure(self, user, tag, adventure_id):
        if not tag:
            return utils.error_page(error=400, ui_message=gettext("no_tag"))
        if not adventure_id:
            return utils.error_page(error=400, ui_message=gettext("retrieve_adventure_error"))

        tag_name = tag.strip()
        db_tag = self.db.read_tag(tag_name)
        if not db_tag:
            return utils.error_page(error=400, ui_message=gettext("retrieve_tag_error"))

        # (1) delete the adventure from the tag and decrese the popularity
        tagged_in = list(filter(lambda t: t["id"] != adventure_id, db_tag["tagged_in"]))
        self.db.update_tag(db_tag["id"], {"tagged_in": tagged_in, "popularity": db_tag["popularity"] - 1})

        # (2) delete the tag from the adventure
        self.db.delete_tag_from_adventure(tag, adventure_id)

        return jinja_partials.render_partial('htmx-tags-dropdown-item.html', tag=db_tag, adventure_id=adventure_id)

    @route("/delete/<tag>", methods=["DELETE"])
    @requires_teacher
    def delete_tag(self, user, tag):
        if not tag:
            return utils.error_page(error=400, ui_message=gettext("no_tag"))

        tag_name = tag.strip()
        db_tag = self.db.read_tag(tag_name)
        if not db_tag:
            return utils.error_page(error=400, ui_message=gettext("retrieve_tag_error"))

        # delete tag
        self.db.delete_tag(db_tag['id'])
        # delete tag from the adventures
        for adventure in db_tag['tagged_in']:
            self.db.delete_tag_from_adventure(tag, adventure['id'])

        return make_response('', 200)
