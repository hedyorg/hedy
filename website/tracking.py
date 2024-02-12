
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

    @route("/", methods=["POST"])
    @requires_login
    def index(self, user):
        # /tracking/
        user = self.db.user_by_username(user["username"])
        print("\n\n\n TRACKING index \n\n")
        body = request.json
        data = []

        class_id = session["class_id"]

        for row in body:
            data_row = {}
            data_row["class_id"] = class_id
            data_row["username"] = user["username"]
            data_row["gender"] = user.get("gender", 'm')
            for key in row.keys():
                data_row[key] = row[key]
            data.append(data_row)

        print(data)

        try:
            parse_logger.log(data)
            return {}, 200
        except IOError:
            return "Not logged", 400
