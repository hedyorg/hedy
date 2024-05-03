import datetime

from flask import jsonify, make_response, redirect, request, session
from flask_babel import gettext

from config import config
from safe_format import safe_format
from hedy_content import ALL_LANGUAGES, COUNTRIES
from utils import extract_bcrypt_rounds, is_heroku, is_testing_request, timems, times, remove_class_preview
from website.auth import (
    MAILCHIMP_API_URL,
    RESET_LENGTH,
    SESSION_LENGTH,
    TOKEN_COOKIE_NAME,
    JUST_LOGGED_OUT,
    check_password,
    create_recover_link,
    create_verify_link,
    forget_current_user,
    is_admin,
    is_teacher,
    mailchimp_subscribe_user,
    make_salt,
    password_hash,
    prepare_user_db,
    remember_current_user,
    requires_login,
    send_email,
    send_email_template,
    validate_signup_data,
)

from .database import Database
from .website_module import WebsiteModule, route


class AuthModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("auth", __name__, url_prefix="/auth")

        self.db = db

    @route("/login", methods=["POST"])
    def login(self):
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400
        if not isinstance(body.get("password"), str):
            return gettext("password_invalid"), 400

        # If username has an @-sign, then it's an email
        if "@" in body["username"]:
            user = self.db.user_by_email(body["username"])
        else:
            user = self.db.user_by_username(body["username"])

        if not user or not check_password(body["password"], user["password"]):
            return gettext("invalid_username_password") + " " + gettext("no_account"), 403

        # If the number of bcrypt rounds has changed, create a new hash.
        new_hash = None
        if config["bcrypt_rounds"] != extract_bcrypt_rounds(user["password"]):
            new_hash = password_hash(body["password"], make_salt())

        cookie = make_salt()
        self.db.store_token({"id": cookie, "username": user["username"], "ttl": times() + SESSION_LENGTH})
        if new_hash:
            self.db.record_login(user["username"], new_hash)
        else:
            self.db.record_login(user["username"])

        # Check if the user has a public profile, if so -> retrieve the profile image
        public_profile = self.db.get_public_profile_settings(user["username"])
        if public_profile:
            session["profile_image"] = public_profile.get("image", 1)

        # Make an empty response to make sure we have one
        resp_body = {}

        if is_admin(user):
            resp_body = {"admin": True}
        elif user.get("is_teacher"):
            resp_body = {"teacher": True}

        # If the user is a student (and has a related teacher) and the verification is still pending -> first login
        if user.get("teacher") and user.get("verification_pending"):
            self.db.update_user(user["username"], {"verification_pending": None})
            resp_body = {"first_time": True}

        resp = make_response(resp_body)
        # We set the cookie to expire in a year,
        # just so that the browser won't invalidate it if the same cookie gets renewed by constant use.
        # The server will decide whether the cookie expires.
        resp.set_cookie(
            TOKEN_COOKIE_NAME,
            value=cookie,
            httponly=True,
            secure=is_heroku(),
            samesite="Lax",
            path="/",
            max_age=365 * 24 * 60 * 60,
        )

        # Remember the current user on the session. This is "new style" logins, which should ultimately
        # replace "old style" logins (with the cookie above), as it requires fewer database calls.
        remember_current_user(user)
        return resp

    @route("/signup", methods=["POST"])
    def signup(self):
        body = request.json
        # Validations, mandatory fields
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400

        # Validate the essential data using a function -> also used for multiple account creation
        validation = validate_signup_data(body)
        if validation:
            return validation, 400

        # Validate fields only relevant when creating a single user account
        if not isinstance(body.get("password_repeat"), str) or body["password"] != body["password_repeat"]:
            return gettext("repeat_match_password"), 400
        if not isinstance(body.get("language"), str) or body.get("language") not in ALL_LANGUAGES.keys():
            return gettext("language_invalid"), 400
        if not isinstance(body.get("agree_terms"), str) or not body.get("agree_terms"):
            return gettext("agree_invalid"), 400
        if not isinstance(body.get("keyword_language"), str) or body.get("keyword_language") not in [
            "en",
            body.get("language"),
        ]:
            return gettext("keyword_language_invalid"), 400

        # Validations, optional fields
        if "birth_year" in body:
            year = datetime.datetime.now().year
            try:
                body["birth_year"] = int(body.get("birth_year"))
            except ValueError:
                return safe_format(gettext("year_invalid"), current_year=str(year)), 400
            if not isinstance(body.get("birth_year"), int) or body["birth_year"] <= 1900 or body["birth_year"] > year:
                return safe_format(gettext("year_invalid"), current_year=str(year)), 400
        if "gender" in body:
            if body["gender"] != "m" and body["gender"] != "f" and body["gender"] != "o":
                return gettext("gender_invalid"), 400
        if "country" in body:
            if not body["country"] in COUNTRIES:
                return gettext("country_invalid"), 400
        if "heard_about" in body:
            if isinstance(body["heard_about"], str):
                body["heard_about"] = [body["heard_about"]]
            if not isinstance(body["heard_about"], list):
                return gettext("heard_about_invalid"), 400
            for option in body["heard_about"]:
                if option not in ["from_another_teacher", "social_media", "from_video", "from_magazine_website",
                                  "other_source"]:
                    return gettext("heard_about_invalid"), 400
        if "prog_experience" in body and body["prog_experience"] not in ["yes", "no"]:
            return gettext("experience_invalid"), 400
        if "experience_languages" in body:
            if isinstance(body["experience_languages"], str):
                body["experience_languages"] = [body["experience_languages"]]
            if not isinstance(body["experience_languages"], list):
                return gettext("experience_invalid"), 400
            for language in body["experience_languages"]:
                if language not in ["scratch", "other_block", "python", "other_text"]:
                    return gettext("programming_invalid"), 400

        if self.db.user_by_username(body["username"].strip().lower()):
            return gettext("exists_username"), 403
        if self.db.user_by_email(body["email"].strip().lower()):
            return gettext("exists_email"), 403

        # We receive the pre-processed user and response package from the function
        user, resp = self.store_new_account(body, body["email"].strip().lower())

        if not is_testing_request(request) and "subscribe" in body:
            # If we have a Mailchimp API key, we use it to add the subscriber through the API
            if MAILCHIMP_API_URL:
                mailchimp_subscribe_user(user["email"], body["country"])
            # Otherwise, we send an email to notify about the subscription to the main email address
            else:
                send_email(
                    config["email"]["sender"],
                    "Subscription to Hedy newsletter on signup",
                    user["email"],
                    "<p>" + user["email"] + "</p>",
                )

        # We automatically login the user
        cookie = make_salt()
        self.db.store_token({"id": cookie, "username": user["username"], "ttl": times() + SESSION_LENGTH})
        # We set the cookie to expire in a year,
        # just so that the browser won't invalidate it if the same cookie gets renewed by constant use.
        # The server will decide whether the cookie expires.
        resp.set_cookie(
            TOKEN_COOKIE_NAME,
            value=cookie,
            httponly=True,
            secure=is_heroku(),
            samesite="Lax",
            path="/",
            max_age=365 * 24 * 60 * 60,
        )

        remember_current_user(user)
        return resp

    @ route("/verify", methods=["GET"])
    def verify_email(self):
        username = request.args.get("username", None)
        token = request.args.get("token", None)
        if not token:
            return gettext("token_invalid"), 400
        if not username:
            return gettext("username_invalid"), 400

        # Verify that user actually exists
        user = self.db.user_by_username(username)
        if not user:
            return gettext("username_invalid"), 403

        # If user is already verified -> re-direct to landing-page anyway
        if "verification_pending" not in user:
            return redirect("/landing-page")

        # Verify the token
        if token != user["verification_pending"]:
            return gettext("token_invalid"), 403

        # Remove the token from the user
        self.db.update_user(username, {"verification_pending": None})

        # We automatically login the user
        cookie = make_salt()
        self.db.store_token({"id": cookie, "username": user["username"], "ttl": times() + SESSION_LENGTH})
        remember_current_user(user)

        return redirect("/landing-page")

    @ route("/logout", methods=["POST"])
    def logout(self):
        forget_current_user()
        if request.cookies.get(TOKEN_COOKIE_NAME):
            self.db.forget_token(request.cookies.get(TOKEN_COOKIE_NAME))
        session[JUST_LOGGED_OUT] = True
        remove_class_preview()
        return make_response('', 204)

    @ route("/destroy", methods=["POST"])
    @ requires_login
    def destroy(self, user):
        forget_current_user()
        self.db.forget_token(request.cookies.get(TOKEN_COOKIE_NAME))
        self.db.forget_user(user["username"])
        session[JUST_LOGGED_OUT] = True
        return make_response('', 204)

    @ route("/destroy_public", methods=["POST"])
    @ requires_login
    def destroy_public(self, user):
        self.db.forget_public_profile(user["username"])
        session.pop("profile_image", None)  # Delete profile image id if existing
        return make_response('', 204)

    @ route("/change_student_password", methods=["POST"])
    @ requires_login
    def change_student_password(self, user):
        body = request.json
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400
        if not isinstance(body.get("password"), str):
            return gettext("password_invalid"), 400
        if len(body["password"]) < 6:
            return gettext("password_six"), 400

        if not is_teacher(user):
            return gettext("password_change_not_allowed"), 400
        students = self.db.get_teacher_students(user["username"])
        if body["username"] not in students:
            return gettext("password_change_not_allowed"), 400

        hashed = password_hash(body["password"], make_salt())
        self.db.update_user(body["username"], {"password": hashed})

        return {"success": gettext("password_change_success")}, 200

    @ route("/change_password", methods=["POST"])
    @ requires_login
    def change_password(self, user):
        body = request.json

        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("old_password"), str) or not isinstance(body.get("new-password"), str):
            return gettext("password_invalid"), 400
        if not isinstance(body.get("password_repeat"), str):
            return gettext("repeat_match_password"), 400
        if len(body["new-password"]) < 6:
            return gettext("password_six"), 400
        if body["new-password"] != body["password_repeat"]:
            return gettext("repeat_match_password"), 400

        # The user object we got from 'requires_login' doesn't have the password, so look that up in the database
        user = self.db.user_by_username(user["username"])

        if not check_password(body["old_password"], user["password"]):
            return gettext("password_invalid"), 403

        hashed = password_hash(body["new-password"], make_salt())

        self.db.update_user(user["username"], {"password": hashed})
        # We are not updating the user in the Flask session, because we should not rely on the password in anyway.
        if not is_testing_request(request):
            try:
                send_email_template(template="change_password", email=user["email"], username=user["username"])
            except BaseException:
                return gettext("mail_error_change_processed"), 400

        return jsonify({"message": gettext("password_updated")}), 200

    @ route("/recover", methods=["POST"])
    def recover(self):
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400

        # If username has an @-sign, then it's an email
        if "@" in body["username"]:
            user = self.db.user_by_email(body["username"].strip().lower())
        else:
            user = self.db.user_by_username(body["username"].strip().lower())

        if not user:
            return gettext("username_invalid"), 403

        # In this case -> account has a related teacher (and is a student)
        # We still store the token, but sent the mail to the teacher instead
        if user.get("teacher") and not user.get("email"):
            email = self.db.user_by_username(user.get("teacher")).get("email")
        else:
            email = user["email"]

        # Create a token -> use the reset_length value as we don't want the token to live as long as a login one
        token = make_salt()
        # Todo TB -> Don't we want to use a hashed token here as well?
        self.db.store_token({"id": token, "username": user["username"], "ttl": times() + RESET_LENGTH})

        if is_testing_request(request):
            # If this is an e2e test, we return the email verification token directly instead of emailing it.
            return jsonify({"username": user["username"], "token": token}), 200
        else:
            try:
                send_email_template(
                    template="recover_password",
                    email=email,
                    link=create_recover_link(user["username"], token),
                    username=user["username"],
                )
            except BaseException:
                return gettext("mail_error_change_processed"), 400

            return jsonify({"message": gettext("sent_password_recovery")}), 200

    @ route("/reset", methods=["POST"])
    def reset(self):
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("username"), str):
            return gettext("username_invalid"), 400
        if not isinstance(body.get("token"), str):
            return gettext("token_invalid"), 400
        if not isinstance(body.get("password"), str):
            return gettext("password_invalid"), 400
        if len(body["password"]) < 6:
            return gettext("password_six"), 400
        if not isinstance(body.get("password_repeat"), str) or body["password"] != body["password_repeat"]:
            return gettext("repeat_match_password"), 400

        token = self.db.get_token(body["token"])
        if not token or body["token"] != token.get("id") or body["username"] != token.get("username"):
            return gettext("token_invalid"), 401

        hashed = password_hash(body["password"], make_salt())
        self.db.update_user(body["username"], {"password": hashed})
        user = self.db.user_by_username(body["username"])

        # Delete all tokens of the user -> automatically logout all long-lived sessions
        self.db.delete_all_tokens(body["username"])

        # In this case -> account has a related teacher (and is a student)
        # We mail the teacher instead
        if user.get("teacher") and not user.get("email"):
            email = self.db.user_by_username(user.get("teacher")).get("email")
        else:
            email = user["email"]

        if not is_testing_request(request):
            try:
                send_email_template(template="reset_password", email=email, username=user["username"])
            except BaseException:
                return gettext("mail_error_change_processed"), 400

        return jsonify({"message": gettext("password_resetted")}), 200

    @route("/request_teacher", methods=["POST"])
    @requires_login
    def request_teacher_account(self, user):
        account = self.db.user_by_username(user["username"])
        if account.get("is_teacher"):
            return gettext("already_teacher"), 400
        if account.get("teacher_request"):
            return gettext("already_teacher_request"), 400

        self.db.update_user(user["username"], {"teacher_request": True})
        return jsonify({"message": gettext("teacher_account_success")}), 200

    def store_new_account(self, account, email):
        username, hashed, hashed_token = prepare_user_db(account["username"], account["password"])
        user = {
            "username": username,
            "password": hashed,
            "email": email,
            "language": account["language"],
            "keyword_language": account["keyword_language"],
            "created": timems(),
            "teacher_request": True if account.get("is_teacher") else None,
            "verification_pending": hashed_token,
            "last_login": timems(),
            "pair_with_teacher": 1 if account.get("pair_with_teacher") else 0,
        }

        for field in ["country", "birth_year", "gender", "language", "heard_about", "prog_experience",
                      "experience_languages"]:
            if field in account:
                if field == "heard_about" and len(account[field]) == 0:
                    continue
                if field == "experience_languages" and len(account[field]) == 0:
                    continue
                user[field] = account[field]

        self.db.store_user(user)

        # If this is an e2e test, we return the email verification token directly instead of emailing it.
        if is_testing_request(request):
            resp = make_response({"username": username, "token": hashed_token})
        # Otherwise, we send an email with a verification link and we return an empty body
        else:
            try:
                send_email_template(
                    template="welcome_verify",
                    email=email,
                    link=create_verify_link(username, hashed_token),
                    username=user["username"],
                )
            except BaseException:
                return user, make_response({gettext("mail_error_change_processed")}, 400)
            resp = make_response({})
        return user, resp
