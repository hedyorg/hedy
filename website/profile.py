import datetime
import hashlib

import requests
from flask import jsonify, request, session
from flask_babel import gettext

from hedy_content import ALL_KEYWORD_LANGUAGES, ALL_LANGUAGES, COUNTRIES
from utils import is_testing_request, timems, valid_email
from website.auth import (
    MAILCHIMP_API_HEADERS,
    MAILCHIMP_API_URL,
    SESSION_LENGTH,
    create_verify_link,
    mailchimp_subscribe_user,
    make_salt,
    password_hash,
    remember_current_user,
    requires_login,
    send_email_template,
)

from .database import Database
from .website_module import WebsiteModule, route


class ProfileModule(WebsiteModule):
    def __init__(self, db: Database):
        super().__init__("profile", __name__, url_prefix="/profile")
        self.db = db

    @route("/", methods=["POST"])
    @requires_login
    def update_profile(self, user):
        body = request.json
        if not isinstance(body, dict):
            return gettext("ajax_error"), 400
        if not isinstance(body.get("language"), str) or body.get("language") not in ALL_LANGUAGES.keys():
            return gettext("language_invalid"), 400
        if (
            not isinstance(body.get("keyword_language"), str)
            or body.get("keyword_language") not in ["en", body.get("language")]
            or body.get("keyword_language") not in ALL_KEYWORD_LANGUAGES.keys()
        ):
            return gettext("keyword_language_invalid"), 400

        # Mail is a unique field, only mandatory if the user doesn't have a related teacher (and no mail address)
        user = self.db.user_by_username(user["username"])
        if not user.get("teacher") or "email" in body:
            if not isinstance(body.get("email"), str) or not valid_email(body["email"]):
                return gettext("email_invalid"), 400

        # Validations, optional fields
        if "birth_year" in body:
            year = datetime.datetime.now().year
            try:
                body["birth_year"] = int(body.get("birth_year"))
            except ValueError:
                return gettext("year_invalid").format(**{"current_year": str(year)}), 400
            if not isinstance(body.get("birth_year"), int) or body["birth_year"] <= 1900 or body["birth_year"] > year:
                return gettext("year_invalid").format(**{"current_year": str(year)}), 400
        if "gender" in body:
            if body["gender"] not in ["m", "f", "o"]:
                return gettext("gender_invalid"), 400
        if "country" in body:
            if not body["country"] in COUNTRIES:
                return gettext("country_invalid"), 400

        resp = {}
        if "email" in body:
            email = body["email"].strip().lower()
            old_user_email = user.get("email")
            if email != user.get("email"):
                exists = self.db.user_by_email(email)
                if exists:
                    return gettext("exists_email"), 403
                token = make_salt()
                hashed_token = password_hash(token, make_salt())
                self.db.update_user(user["username"], {"email": email, "verification_pending": hashed_token})
                # If this is an e2e test, we return the email verification token directly instead of emailing it.
                if is_testing_request(request):
                    resp = {"username": user["username"], "token": hashed_token}
                else:
                    try:
                        send_email_template(
                            template="welcome_verify",
                            email=email,
                            link=create_verify_link(user["username"], hashed_token),
                            username=user["username"],
                        )
                    except BaseException:
                        # Todo TB: Now we only log to the back-end, would be nice to also return the user some info
                        # We have two options: return an error at this point (don't process changes)
                        # Add a notification to the response, still process the changes
                        print(f"Profile changes processed for {user['username']}, mail sending invalid")

                # We check whether the user is in the Mailchimp list.
                if not is_testing_request(request) and MAILCHIMP_API_URL:
                    # We hash the email with md5 to avoid emails with unescaped characters triggering errors
                    request_path = (
                        MAILCHIMP_API_URL + "/members/" + hashlib.md5(old_user_email.encode("utf-8")).hexdigest()
                    )
                    r = requests.get(request_path, headers=MAILCHIMP_API_HEADERS)
                    # If user is subscribed, we remove the old email from the list and add the new one
                    if r.status_code == 200:
                        r = requests.delete(request_path, headers=MAILCHIMP_API_HEADERS)
                        role = self.db.get_username_role(user["username"])
                        mailchimp_subscribe_user(email, body["country"])

        username = user["username"]

        updates = {}
        for field in ["country", "birth_year", "gender", "language", "keyword_language"]:
            if field in body:
                updates[field] = body[field]
            else:
                updates[field] = None
        if body.get("agree_third_party"):
            updates["third_party"] = True
        else:
            updates["third_party"] = None

        if updates:
            self.db.update_user(username, updates)

        # Always make sure that the country stored on the public profile is identical to the profile one
        self.db.update_country_public_profile(username, body.get("country", None))

        # We want to check if the user choose a new language, if so -> reload
        # We can use g.lang for this to reduce the db calls
        resp["reload"] = False
        if session["lang"] != body["language"] or session["keyword_lang"] != body["keyword_language"]:
            resp["message"] = gettext("profile_updated_reload")
            resp["reload"] = True
        else:
            resp["message"] = gettext("profile_updated")

        remember_current_user(self.db.user_by_username(user["username"]))
        return jsonify(resp)

    @route("/", methods=["GET"])
    @requires_login
    def get_profile(self, user):
        print(self, user)
        # The user object we got from 'requires_login' is not fully hydrated yet. Look up the database user.
        user = self.db.user_by_username(user["username"])

        output = {"username": user["username"], "email": user["email"], "language": user.get("language", "en")}
        for field in ["birth_year", "country", "gender", "prog_experience", "experience_languages", "third_party"]:
            if field in user:
                output[field] = user[field]
        if "verification_pending" in user:
            output["verification_pending"] = True

        output["student_classes"] = self.db.get_student_classes(user["username"])

        output["session_expires_at"] = timems() + SESSION_LENGTH * 1000

        return jsonify(output), 200
