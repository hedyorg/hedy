
from flask import request, make_response
from flask_babel import gettext
import json
import uuid
import utils

from website.auth import requires_teacher

from .database import Database
from .website_module import WebsiteModule, route


class FeedbackModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("feedback", __name__, url_prefix="/feedback")
        self.db = db

    @route("/", methods=["POST"])
    @requires_teacher
    def teacher_feedback(self, user):
        body = request.form
        # Request validation
        if not body.get("message") or not body.get("category"):
            return gettext('feedback_message_error'), 400

        feedback = {
            "id": uuid.uuid4().hex,
            "username": user.get("username"),
            "message": body.get("message"),
            "category": body.get("category"),
            "page": body.get("page", ""),
            "date": utils.timems(),
        }

        try:
            self.db.store_feedback(feedback)
        except Exception as e:
            print(e)
            return gettext('feedback_message_error'), 500

        response = make_response("")
        response.headers["HX-Push-URL"] = 'false'
        response.headers["HX-Trigger"] = json.dumps({"hideFeedbackModal": True})

        return response
