from flask import make_response, request
from flask_babel import gettext

import hedyweb
import utils
from website.flask_helpers import render_template
from website.auth import (
    create_verify_link,
    current_user,
    is_admin,
    is_teacher,
    make_salt,
    password_hash,
    pick,
    requires_admin,
    send_localized_email_template,
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
            "admin/admin-users.html",
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

    @route("/achievements", methods=["GET"])
    @requires_admin
    def get_admin_achievements_page(self, user):
        stats = {}
        achievements = hedyweb.AchievementTranslations().get_translations("en").get("achievements")
        for achievement in achievements.keys():
            stats[achievement] = {}
            stats[achievement]["name"] = achievements.get(achievement).get("title")
            stats[achievement]["description"] = achievements.get(achievement).get("text")
            stats[achievement]["count"] = 0

        user_achievements = self.db.get_all_achievements()
        total = len(user_achievements)
        for user in user_achievements:
            for achieved in user.get("achieved", []):
                stats[achieved]["count"] += 1

        return render_template(
            "admin/admin-achievements.html",
            stats=stats,
            current_page="admin",
            total=total,
            page_title=gettext("title_admin"),
        )

    @route("/markAsTeacher", methods=["POST"])
    def mark_as_teacher(self):
        user = current_user()
        if not is_admin(user) and not utils.is_testing_request(request):
            return utils.error_page(error=401, ui_message=gettext("unauthorized"))

        body = request.json

        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400
        if not isinstance(body.get("is_teacher"), bool):
            return gettext("teacher_invalid"), 400

        user = self.db.user_by_username(body["username"].strip().lower())

        if not user:
            return gettext("username_invalid"), 400

        is_teacher_value = 1 if body["is_teacher"] else 0
        update_is_teacher(self.db, user, is_teacher_value)

        # Todo TB feb 2022 -> Return the success message here instead of fixing in the front-end
        return "", 200

    @route("/changeUserEmail", methods=["POST"])
    @requires_admin
    def change_user_email(self, user):
        body = request.json

        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400
        if not isinstance(body.get("email"), str) or not utils.valid_email(body["email"]):
            return gettext("email_invalid"), 400

        user = self.db.user_by_username(body["username"].strip().lower())

        if not user:
            return gettext("email_invalid"), 400

        token = make_salt()
        hashed_token = password_hash(token, make_salt())

        # We assume that this email is not in use by any other users.
        # In other words, we trust the admin to enter a valid, not yet used email address.
        self.db.update_user(user["username"], {"email": body["email"], "verification_pending": hashed_token})

        # If this is an e2e test, we return the email verification token directly instead of emailing it.
        if utils.is_testing_request(request):
            return {"username": user["username"], "token": hashed_token}, 200
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
                return gettext("mail_error_change_processed"), 400

        return make_response('', 204)

    @route("/getUserTags", methods=["POST"])
    @requires_admin
    def get_user_tags(self, user):
        body = request.json
        user = self.db.get_public_profile_settings(body["username"].strip().lower())
        if not user:
            return "User doesn't have a public profile", 400
        return {"tags": user.get("tags", [])}, 200

    @route("/updateUserTags", methods=["POST"])
    @requires_admin
    def update_user_tags(self, user):
        body = request.json
        db_user = self.db.get_public_profile_settings(body["username"].strip().lower())
        if not user:
            return "User doesn't have a public profile", 400

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

    db.update_user(user["username"], {"is_teacher": is_teacher_value, "teacher_request": None})

    # Some (student users) may not have emails, and this code would explode otherwise
    if user_becomes_teacher and not utils.is_testing_request(request) and user.get('email'):
        try:
            send_localized_email_template(
                locale=user["language"], template="welcome_teacher", email=user["email"], username=user["username"]
            )
        except Exception:
            print(f"An error occurred when sending a welcome teacher mail to {user['email']}, changes still processed")
