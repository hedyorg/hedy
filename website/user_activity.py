
import os
from flask import make_response, request, session

# import utils
from config import config
from website.auth import requires_login, is_teacher

from .database import Database
from .website_module import WebsiteModule, route
import utils

from website import s3_logger

cookie_name = config["session"]["cookie_name"]
invite_length = config["session"]["invite_length"] * 60


# Add LOG_USER_ACTIVITY=True to your env. to log the data for testing
if utils.is_heroku():
    logger = s3_logger.S3Logger(name="activity", config_key="s3-activity-logs")
elif os.getenv("LOG_USER_ACTIVITY"):
    logger = s3_logger.FileLogger()
else:
    logger = s3_logger.NullLogger()


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
            data_row = {
                "class_id": class_id,
                "username": user["username"],
                "is_teacher": is_teacher(user),
                "gender": user.get("gender", "o"),
                # Data from front-end
                "time": row["time"],
                "id": row["id"],
                "page": row["page"],
                "extra": row["extra"]
            }

            data.append(data_row)

        print(data)

        try:
            logger.log(data)
            return make_response('', 204)
        except IOError:
            return "Not logged", 400
