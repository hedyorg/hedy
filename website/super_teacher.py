
from flask import render_template, request
from flask_babel import gettext


from website.auth import requires_super_teacher, pick
import utils

from .database import Database
from .website_module import WebsiteModule, route


class SuperTeacherModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("super_teacher", __name__, url_prefix="/super-teacher")
        self.db = db

    @route("/", methods=["GET"])
    @requires_super_teacher
    def get_super_teacher_page(self, user):
        return render_template('super-teacher/index.html')

    @route("/support", methods=["GET"])
    @requires_super_teacher
    def get_support(self, user):
        category = request.args.get("filter", default=None, type=str)
        category = None if category == "null" else category

        substring = request.args.get("substring", default=None, type=str)
        start_date = request.args.get("start", default=None, type=str)
        end_date = request.args.get("end", default=None, type=str)
        language = request.args.get("language", default=None, type=str)
        keyword_language = request.args.get("keyword_language", default=None, type=str)

        substring = None if substring == "null" else substring
        start_date = None if start_date == "null" else start_date
        end_date = None if end_date == "null" else end_date
        language = None if language == "null" else language
        keyword_language = None if keyword_language == "null" else keyword_language

        pagination_token = request.args.get("page", default=None, type=str)

        users = self.db.all_users(pagination_token)

        userdata = []
        fields = [
            "username",
            "email",
            "birth_year",
            "country",
            "gender",
            "created",
            "last_login",
            "verification_pending",
            "is_teacher",
            "is_super_teacher",
            "program_count",
            "prog_experience",
            "teacher_request",
            "experience_languages",
            "language",
            "keyword_language",
        ]

        for user in users:
            data = pick(user, *fields)
            data["email_verified"] = not bool(data["verification_pending"])
            data["is_teacher"] = bool(data["is_teacher"])
            data["teacher_request"] = True if data["teacher_request"] else None
            data["created"] = utils.timestamp_to_date(data["created"])
            data["last_login"] = utils.timestamp_to_date(data["last_login"]) if data.get("last_login") else None
            if category == "language":
                if language != data["language"]:
                    continue
            if category == "keyword_language":
                if keyword_language != data["keyword_language"]:
                    continue
            if category == "username":
                if substring and substring not in data.get("username"):
                    continue
            if category == "email":
                if not data.get("email") or (substring and substring not in data.get("email")):
                    continue
            if category == "created":
                if start_date and utils.string_date_to_date(start_date) > data["created"]:
                    continue
                if end_date and utils.string_date_to_date(end_date) < data["created"]:
                    continue
            if category == "last_login":
                if not data.get("last_login"):
                    continue
                if start_date and utils.string_date_to_date(start_date) > data["last_login"]:
                    continue
                if end_date and utils.string_date_to_date(end_date) < data["last_login"]:
                    continue
            userdata.append(data)

        return render_template(
            "super-teacher/support.html",
            users=userdata,
            page_title=gettext("title_admin"),
            filter=category,
            start_date=start_date,
            end_date=end_date,
            text_filter=substring,
            language_filter=language,
            keyword_language_filter=keyword_language,
            next_page_token=users.next_page_token,
            current_page="admin",
            javascript_page_options=dict(page='admin-users'),
        )
