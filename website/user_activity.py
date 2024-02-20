
from flask import request, session
# from flask_babel import gettext
# import jinja_partials
# import uuid

# import utils
from config import config
from website.auth import requires_login, is_teacher

from .database import Database
from .website_module import WebsiteModule, route

from website import s3_logger

cookie_name = config["session"]["cookie_name"]
invite_length = config["session"]["invite_length"] * 60


HEADER = ["class_id", "username", "is_teacher", "gender", "time", "id", "page", "extra"]
parse_logger = s3_logger.S3ParseLogger.from_env_vars(header=HEADER, tracking=True)


class UserActivityModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("activity", __name__, url_prefix="/activity")
        self.db = db

    @route("/", methods=["POST"])
    @requires_login
    def index(self, user):
        # /tracking activity/
        user = self.db.user_by_username(user["username"])
        if not user:
            return {}, 304
        print("\n\n TRACKING index \n\n")
        body = request.json
        data = []

        class_id = session.get("class_id")

        for row in body:
            # Values in data_row should be consistent with the header.
            data_row = []
            data_row.append(class_id)
            data_row.append(user["username"])
            data_row.append(is_teacher(user))
            data_row.append(user.get("gender", 'm'))
            # Date from front-end
            data_row.append(row["time"])
            data_row.append(row["id"])
            data_row.append(row["page"])
            data_row.append(row["extra"])

            data.append(data_row)

        print(data)

        try:
            parse_logger.log(data)
            return {}, 200
        except IOError:
            return "Not logged", 400
