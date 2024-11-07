
from flask import request, make_response, render_template
from website.flask_helpers import gettext_with_fallback as gettext
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
        self.valid_categories = ["bug", "feedback", "feature"]

    def is_valid_category(self, cat):
        return cat in self.valid_categories

    @route("/", methods=["POST"])
    @requires_teacher
    def teacher_feedback(self, user):
        body = request.form
        # Request validation
        if not body.get("message") or not body.get("category"):
            return make_response(gettext('feedback_message_error'), 400)

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
            return make_response(gettext('feedback_message_error'), 500)

        response = make_response('', 200)
        response.headers["HX-Push-URL"] = 'false'
        response.headers["HX-Trigger"] = json.dumps({"hideFeedbackModal": True})

        return response

    @route("/", methods=["GET"])
    @requires_super_teacher
    def get_feedback(self, user):
        category = request.args.get('category') or ""
        if category and not self.is_valid_category(category):
            return gettext('feedback_message_error'), 400
        page = request.args.get('page') or ""
        username = request.args.get('username') or ""
        keys = {"category": category, "page": page, "username": username}
        keys = {key: value for key, value in keys.items() if value}

        all_feedback = self.db.get_feedback()
        if not all_feedback:
            return render_template('feedback.html', feedback_by_category={})

        # Group feedback by category
        feedback_by_category = defaultdict(list)
        categories = set()
        users = set()
        pages = set()
        for feedback in all_feedback:
            # only if given filters are valid we add current feedback
            if not keys or any([feedback.get(key) == value for key, value in keys.items()]):
                feedback_by_category[feedback.get("category")].append(feedback)
            categories.add(feedback.get("category"))
            users.add(feedback.get("username"))
            pages.add(feedback.get("page"))

        return render_template('feedback.html', feedback_by_category=feedback_by_category,
                               categories=categories,
                               users=users,
                               pages=pages,)
