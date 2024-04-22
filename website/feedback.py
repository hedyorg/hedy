
from flask import request, make_response, render_template
from flask_babel import gettext
import json
import uuid
from collections import defaultdict

import utils

from website.auth import requires_teacher, requires_super_teacher

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
            "email": user.get("email", ""),
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

    @route("/", methods=["GET"])
    @requires_super_teacher
    def get_feedback(self, user):
        all_feedback = self.db.get_feedback()
        category = request.args.get('category', default=None, type=str) or None
        page = request.args.get('page', default=None, type=str) or None
        user = request.args.get('user', default=None, type=str) or None
        print('\n\n\n')
        print(all_feedback)
        if not all_feedback:
            return render_template('feedback.html', feedback_by_category={})
        # Group feedback by category
        feedback_by_category = defaultdict(list)
        for feedback in all_feedback:
            print(feedback)
            feedback_by_category[category].append(feedback)

        return render_template('feedback.html', feedback_by_category=feedback_by_category)
