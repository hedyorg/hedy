
from flask import request, session
# from flask_babel import gettext
# import jinja_partials
# import uuid

# import utils
from config import config
from website.auth import requires_login

from .database import Database
from .website_module import WebsiteModule, route

from website import s3_logger

cookie_name = config["session"]["cookie_name"]
invite_length = config["session"]["invite_length"] * 60


parse_logger = s3_logger.S3ParseLogger.from_env_vars()


class TrackingModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("tracking", __name__, url_prefix="/tracking")

        self.db = db
        self.activity_id = None

    def index_teacher(self, user):
        return {}

    @route("/", methods=["POST"])
    @requires_login
    def index(self, user):
        # /tracking/
        user = self.db.user_by_username(user["username"])
        # if user.get("is_teacher"):
        #     return self.index_teacher(user)

        print("\n\n\n TRACKING index \n\n")
        body = request.json
        data = {}

        class_id = session["class_id"]
        data["class_id"] = class_id
        data["username"] = user["username"]
        data["gender"] = user["gender"]
        # print(data)
        # counts = data.counts
        # page = data.page
        # page_title = data.pageTitle

        data["data"] = body

        parse_logger.log(data, filename="data_track.csv")
        return {}

        # hits = body.get("hits", {})
        # pages = {body.get("page")}
        # page_titles = {body.get("pageTitle")}

        # data["pages"] = pages
        # data["page_titles"] = page_titles

        # activity = self.db.get_activity(user["username"])
        # if activity:
        #     activity.get("hits").update(hits)
        #     hits = activity.get("hits")

        #     activity.get("pages").update(pages)
        #     pages = activity.get("pages")

        #     activity.get("page_titles").update(page_titles)
        #     page_titles = activity.get("page_titles")

        #     self.activity_id = activity.get("id")

        # data["hits"] = hits
        # data["pages"] = pages
        # data["page_titles"] = page_titles

        # if self.activity_id:
        #     self.db.log_activity(data, self.activity_id)
        # else:
        #     self.activity_id = uuid.uuid4().hex
        #     data["id"] = self.activity_id
        #     self.db.log_activity(data)

        # return {}
