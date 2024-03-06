
import os
from flask import request, make_response, jsonify
from flask_babel import gettext
import datetime
import json
import uuid

# import utils
from config import config
from website.auth import requires_teacher

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


class FeedbackModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("feedback", __name__, url_prefix="/feedback")
        self.db = db

    @route("/", methods=["POST"])
    @requires_teacher
    def teacher_feedback(self, user):
        body = request.form
        print('\n\n\n', body)
        print('\n\n\n', request)
        # Request validation
        if not body.get("message") or not body.get("category"):
            return gettext('feedback_message_error'), 400

        feedback = {
            "id": uuid.uuid4().hex,
            "username": user.get('username'),
            "message": body.get('message'),
            "category": body.get('category'),
            "timestamp": str(datetime.datetime.now()),
        }

        try:
            self.db.store_feedback(feedback)
        except Exception as e:
            print(e)
            return make_response(jsonify({'error': gettext('feedback_message_error')}), 500)

        response = make_response(jsonify({'success': gettext("feedback_message_success")}))
        response.headers["HX-Push-URL"] = 'false'
        response.headers["HX-Trigger"] = json.dumps({"hideFeedbackModal": "success"})

        return response
