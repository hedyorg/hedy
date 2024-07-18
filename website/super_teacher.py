
from flask import make_response, render_template, request
from website.auth import requires_super_teacher, pick, is_teacher
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
            "support_teacher",
            "pair_with_teacher",
        ]

        for user in users:
            data = pick(user, *fields)
            data["email_verified"] = not bool(data["verification_pending"])
            data["is_teacher"] = bool(data["is_teacher"])
            if not data["is_teacher"] and not data["teacher_request"]:
                continue
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
            page_title="Support teachers",
            filter=category,
            start_date=start_date,
            end_date=end_date,
            text_filter=substring,
            language_filter=language,
            keyword_language_filter=keyword_language,
            next_page_token=users.next_page_token,
            current_page="admin",
            javascript_page_options=dict(page='super-teacher'),
        )

    @route("/invite-support", methods=["POST"])
    @requires_super_teacher
    def invite_support(self, user):
        body = request.json
        if not body.get("sourceUser"):
            return "Please provide a user who needs help", 400
        if not body.get("targetUser"):
            return "Please provide a username", 400

        username = body["sourceUser"]
        source_user = self.db.user_by_username(username)
        if not source_user:
            return f"{username} is not an existing user.", 400
        elif not is_teacher(source_user):
            return f"{username} is not a teacher.", 400

        username = body["targetUser"]
        target_user = self.db.user_by_username(username)
        if not target_user:
            return f"{username} is not an existing user.", 400
        elif not is_teacher(target_user):
            return f"{username} is not a teacher.", 400

        if source_user["username"] == target_user["username"]:
            return "Both usernames are the same", 400

        if (source_user.get("support_teacher") and source_user["support_teacher"] == target_user["username"]) \
                or (target_user.get("support_teacher") and target_user["support_teacher"] == source_user["username"]):
            return "Not possible to add this support teacher", 400

        self.db.update_user(source_user["username"], {"support_teacher": target_user["username"]})
        return make_response("Done", 200)

    @route("/tags", methods=["GET"])
    @requires_super_teacher
    def get_tags(self, user):
        all_tags = self.db.read_public_tags()
        return render_template('super-teacher/tags.html', tags=all_tags)
