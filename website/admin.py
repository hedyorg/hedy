from flask import make_response, request
from website.flask_helpers import gettext_with_fallback as gettext

import utils
from website.flask_helpers import render_template
from website.auth import (
    create_verify_link,
    current_user,
    is_admin,
    is_super_teacher,
    is_teacher,
    make_salt,
    password_hash,
    pick,
    requires_admin,
    send_localized_email_template,
    refresh_current_user_from_db,
)

from .database import Database
from .website_module import WebsiteModule, route


class AdminModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("admin", __name__, url_prefix="/admin")

        self.db = db

    @route("/", methods=["GET"])
    def get_admin_page(self):
        # Todo TB: Why do we check for the testing_request here? (09-22)
        if not utils.is_testing_request(request) and not is_admin(current_user()):
            return utils.error_page(error=401, ui_message=gettext("unauthorized"))
        return render_template("admin/admin.html", page_title=gettext("title_admin"), current_page="admin")

    @route("/users", methods=["GET"])
    @requires_admin
    def get_admin_users_page(self, user):
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
            "experience_languages",
            "language",
            "keyword_language",
        ]

        for user in users:
            data = pick(user, *fields)
            data["email_verified"] = not bool(data["verification_pending"])
            data["is_teacher"] = bool(data["is_teacher"])
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
            "admin/admin-users.html",
            users=userdata,
            page_title=gettext("title_admin"),
            filter=category,
            start_date=start_date,
            end_date=end_date,
            text_filter=substring,
            language_filter=language,
            keyword_language_filter=keyword_language,
            prev_page_token=users.prev_page_token,
            next_page_token=users.next_page_token,
            current_page="admin",
            javascript_page_options=dict(page='admin-users'),
        )

    @route("/adventures", methods=["GET"])
    @requires_admin
    def get_admin_adventures_page(self, user):
        all_adventures = sorted(self.db.all_adventures(), key=lambda d: d.get("date", 0), reverse=True)
        adventures = [
            {
                "id": adventure.get("id"),
                "creator": adventure.get("creator"),
                "name": adventure.get("name"),
                "level": adventure.get("level"),
                "public": "Yes" if adventure.get("public") else "No",
                "date": utils.localized_date_format(adventure.get("date")),
            }
            for adventure in all_adventures
        ]

        return render_template(
            "admin/admin-adventures.html",
            adventures=adventures,
            page_title=gettext("title_admin"),
            current_page="admin",
        )

    @route("/mark-as-teacher/<username_teacher>", methods=["POST"])
    def mark_as_teacher(self, username_teacher):
        user = current_user()
        # the user that wants to mark a teacher
        if (not is_admin(user) and not is_super_teacher(user)) and not utils.is_testing_request(request):
            return utils.error_page(error=401, ui_message=gettext("unauthorized"))
        if not username_teacher:
            return make_response(gettext("username_invalid"), 400)

        # the user that is going to be a teacher
        teacher = self.db.user_by_username(username_teacher.strip().lower())
        if not teacher:
            return make_response(gettext("username_invalid"), 400)
        if utils.is_testing_request(request):
            is_teacher_value = request.json['is_teacher']
        else:
            is_teacher_value = 0 if teacher.get("is_teacher") else 1

        update_is_teacher(self.db, teacher, is_teacher_value)

        return make_response({}, 200)

    @route("/mark-super-teacher/<username_teacher>", methods=["POST"])
    @requires_admin
    def mark_super_teacher(self, user, username_teacher):
        # the user that wants to mark a teacher
        if not user and not utils.is_testing_request(request):
            return utils.error_page(error=401, ui_message=gettext("unauthorized"))
        if not username_teacher:
            return make_response(gettext("username_invalid"), 400)
        if not is_teacher:
            return make_response(gettext("teacher_invalid"), 400)

        # the user that is going to be a teacher
        teacher = self.db.user_by_username(username_teacher.strip().lower())

        if not teacher:
            return make_response(gettext("username_invalid"), 400)
        elif not is_teacher(user):
            return make_response("user must be a teacher.", 400)

        self.db.update_user(username_teacher, {"is_super_teacher": 0 if teacher.get("is_super_teacher") else 1, })
        refresh_current_user_from_db()

        return make_response(f"{username_teacher} is now a super-teacher.", 200)

    @route("/changeUserEmail", methods=["POST"])
    @requires_admin
    def change_user_email(self, user):
        body = request.json

        # Validations
        if not isinstance(body, dict):
            return make_response(gettext("ajax_error"), 400)
        if not isinstance(body.get("username"), str):
            return make_response(gettext("username_invalid"), 400)
        if not isinstance(body.get("email"), str) or not utils.valid_email(body["email"]):
            return make_response(gettext("email_invalid"), 400)

        user = self.db.user_by_username(body["username"].strip().lower())

        if not user:
            return make_response(gettext("email_invalid"), 400)

        token = make_salt()
        hashed_token = password_hash(token, make_salt())

        # We assume that this email is not in use by any other users.
        # In other words, we trust the admin to enter a valid, not yet used email address.
        self.db.update_user(user["username"], {"email": body["email"], "verification_pending": hashed_token})

        # If this is an e2e test, we return the email verification token directly instead of emailing it.
        if utils.is_testing_request(request):
            return make_response({"username": user["username"], "token": hashed_token}, 200)
        else:
            try:
                send_localized_email_template(
                    locale=user["language"],
                    template="welcome_verify",
                    email=body["email"],
                    link=create_verify_link(user["username"], hashed_token),
                    username=user["username"],
                )
            except BaseException:
                return make_response(gettext("mail_error_change_processed"), 400)
        return make_response({}, 200)

    @route("/getUserTags", methods=["POST"])
    @requires_admin
    def get_user_tags(self, user):
        body = request.json
        user = self.db.get_public_profile_settings(body["username"].strip().lower())
        if not user:
            return make_response(gettext("request_invalid"), 400)
        return make_response({"tags": user.get("tags", [])}, 200)

    @route("/updateUserTags", methods=["POST"])
    @requires_admin
    def update_user_tags(self, user):
        body = request.json
        db_user = self.db.get_public_profile_settings(body["username"].strip().lower())
        if not user:
            return make_response(gettext("request_invalid"), 400)

        tags = []
        if "admin" in user.get("tags", []):
            tags.append("admin")
        if "teacher" in user.get("tags", []):
            tags.append("teacher")
        if body.get("certified"):
            tags.append("certified_teacher")
        if body.get("distinguished"):
            tags.append("distinguished_user")
        if body.get("contributor"):
            tags.append("contributor")

        # We have to pop the username otherwise Dynamo gets mad -> we can't update a value that is also the index key
        username = db_user.get("username")
        db_user["tags"] = tags

        self.db.update_public_profile(username, db_user)
        return make_response('', 204)


def update_is_teacher(db: Database, user, is_teacher_value=1):
    user_is_teacher = is_teacher(user)
    user_becomes_teacher = is_teacher_value and not user_is_teacher

    db.update_user(user["username"], {"is_teacher": is_teacher_value})

    # Some (student users) may not have emails, and this code would explode otherwise
    if user_becomes_teacher and not utils.is_testing_request(request) and user.get('email'):
        try:
            send_localized_email_template(
                locale=user["language"], template="welcome_teacher", email=user["email"], username=user["username"]
            )
        except Exception:
            print(f"An error occurred when sending a welcome teacher mail to {user['email']}, changes still processed")
