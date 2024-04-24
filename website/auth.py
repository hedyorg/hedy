import json
import logging
import os
import re
import urllib
from functools import wraps

import bcrypt
import boto3
import requests
from botocore.exceptions import ClientError as email_error
from botocore.exceptions import NoCredentialsError
from flask import g, request, session, redirect
from flask_babel import force_locale, gettext

import utils
from config import config
from safe_format import safe_format
from utils import is_debug_mode, timems, times
from website import querylog

TOKEN_COOKIE_NAME = config["session"]["cookie_name"]

# A special value in the session, if this is set and we hit a 403 on the
# very next page load, we redirect to the front page.
JUST_LOGGED_OUT = 'just-logged-out'

# The session_length in the session is set to 60 * 24 * 14 (in minutes) config.py#13
# The reset_length in the session is set to 60 * 4 (in minutes) config.py#14
# We multiply this by 60 to set the session_length to 14 days and reset_length to 4 hours
SESSION_LENGTH = config["session"]["session_length"] * 60
RESET_LENGTH = config["session"]["reset_length"] * 60


env = os.getenv("HEROKU_APP_NAME")

MAILCHIMP_API_URL = None
MAILCHIMP_API_HEADERS = {}
if os.getenv("MAILCHIMP_API_KEY") and os.getenv("MAILCHIMP_AUDIENCE_ID"):
    # The domain in the path is the server name, which is contained in the Mailchimp API key
    MAILCHIMP_API_URL = (
        "https://"
        + os.getenv("MAILCHIMP_API_KEY").split("-")[1]
        + ".api.mailchimp.com/3.0/lists/"
        + os.getenv("MAILCHIMP_AUDIENCE_ID")
    )
    MAILCHIMP_API_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "apikey " + os.getenv("MAILCHIMP_API_KEY"),
    }


def mailchimp_subscribe_user(email, country):
    # Request is always for teachers as only they can subscribe to newsletters
    request_body = {"email_address": email, "status": "subscribed", "tags": [country, "teacher"]}
    r = requests.post(MAILCHIMP_API_URL + "/members", headers=MAILCHIMP_API_HEADERS, data=json.dumps(request_body))

    subscription_error = None
    if r.status_code != 200 and r.status_code != 400:
        subscription_error = True
    # We can get a 400 if the email is already subscribed to the list. We should ignore this error.
    if r.status_code == 400 and not re.match(".*already a list member", r.text):
        subscription_error = True
    # If there's an error in subscription through the API, we report it to the main email address
    if subscription_error:
        send_email(
            config["email"]["sender"],
            "ERROR - Subscription to Hedy newsletter on signup",
            email,
            "<p>" + email + "</p><pre>Status:" + str(r.status_code) + "    Body:" + r.text + "</pre>",
        )


@querylog.timed
def check_password(password, hash):
    return bcrypt.checkpw(bytes(password, "utf-8"), bytes(hash, "utf-8"))


def make_salt():
    return bcrypt.gensalt(rounds=config["bcrypt_rounds"]).decode("utf-8")


@querylog.timed
def password_hash(password, salt):
    return bcrypt.hashpw(bytes(password, "utf-8"), bytes(salt, "utf-8")).decode("utf-8")


# The current user is a slice of the user information from the database and placed on the Flask session.
# The main purpose of the current user is to provide a convenient container for
# * username
# * email
# * is_teacher
#
# Since the is_teacher can be changed during a session we also store a time-to-live.
#  When retrieving the current user, we can check if we need to reload data from the database.
#
# The current user should be retrieved with `current_user` function since it will return a sane default.
# You can remove the current user from the Flask session with the `forget_current_user`.
def remember_current_user(db_user):
    session["user-ttl"] = times() + 5 * 60
    session["lang"] = db_user.get("language", "en")
    session["keyword_lang"] = db_user.get("keyword_language", "en")

    # Prepare the cached user object
    session["user"] = pick(db_user, "username", "email", "is_teacher", "second_teacher_in")
    session["user"]["second_teacher_in"] = db_user.get("second_teacher_in", [])
    # Classes is a set in dynamo, but it must be converted to an array otherwise it cannot be stored in a session
    session["user"]["classes"] = list(db_user.get("classes", []))


def pick(d, *requested_keys):
    return {key: force_json_serializable_type(d.get(key, None)) for key in requested_keys}


def force_json_serializable_type(x):
    """Turn the given value into something that can be stored in a session.

    May not be the same type, but it'll be Close Enough(tm).
    """
    if isinstance(x, set):
        return list(x)
    return x


# Retrieve the current user from the Flask session.
#
# If the current user is too old, as determined by the time-to-live, we repopulate from the database.
def current_user(refresh=False):
    now = times()
    ttl = session.get("user-ttl", None)
    if ttl is None or now >= ttl or refresh:
        refresh_current_user_from_db()

    user = session.get("user", {"username": "", "email": ""})
    return user


def refresh_current_user_from_db():
    """Refresh the cached session data for the current user from the database."""
    user = session.get("user", {"username": "", "email": ""})
    username = user["username"]
    if username:
        db_user = g.db.user_by_username(username)
        if not db_user:
            raise RuntimeError(f"Cannot find current user in db anymore: {username}")
        remember_current_user(db_user)


def is_user_logged_in():
    """Return whether or not a user is currently logged in."""
    return bool(current_user()["username"])


# Remove the current info from the Flask session.
def forget_current_user():
    session.pop("user", None)  # We are not interested in the value of the use key.
    session.pop("messages", None)  # Delete messages counter for current user if existed
    session.pop("achieved", None)  # Delete session achievements if existing
    session.pop("keyword_lang", None)  # Delete session keyword language if existing
    session.pop("profile_image", None)  # Delete profile image id if existing


def is_admin(user):
    """Whether the given user (object) is an admin.

    Shecks the configuration in environment variables $ADMIN_USER and $ADMIN_USERS.
    """
    admin_users = []
    if os.getenv("ADMIN_USER"):
        admin_users.append(os.getenv("ADMIN_USER"))
    if os.getenv("ADMIN_USERS"):
        admin_users.extend(os.getenv("ADMIN_USERS").split(","))

    return user.get("username") in admin_users or user.get("email") in admin_users


def is_teacher(user, cls=None):
    # the `is_teacher` field is either `0`, `1` or not present.
    return bool(user.get("is_teacher", False))


def is_second_teacher(user, class_id=None):
    # the `second_teacher_in` field indicates the classes where the user is a second teacher.
    if not class_id:
        return bool(user.get("second_teacher_in", False))
    return is_teacher(user) and class_id in user.get("second_teacher_in", [])


def has_public_profile(user):
    if 'username' not in user or user.get('username') == '':
        return False
    username = user.get('username')
    public_profile_settings = g.db.get_public_profile_settings(username)
    has_public_profile = public_profile_settings is not None
    return has_public_profile

# Thanks to https://stackoverflow.com/a/34499643


def hide_explore(user):
    if 'username' not in user or user.get('username') == '':
        return False
    username = user.get('username')
    customizations = g.db.get_student_class_customizations(username)
    hide_explore = True if customizations and 'hide_explore' in customizations.get('other_settings') else False
    return hide_explore


def requires_login(f):
    """Decoractor to indicate that a particular route requires the user to be logged in.

    If the user is not logged in, an error page will be shown. If they are, the
    function is executed as normal with the user information passed to it.

    The function MUST take an argument named 'user', which will contain the
    minimal user object from the session (containing 'username', 'email' and
    'is_teacher').

    Example:

        @app.route('/bla', method=['GET'])
        @requires_login
        def show_bla(user):
            pass
    """

    @wraps(f)
    def inner(*args, **kws):
        print('session before', session)
        just_logged_out = session.pop(JUST_LOGGED_OUT, False)
        print('session after', session)
        if not is_user_logged_in():
            return redirect('/') if just_logged_out else utils.error_page(error=401)
        # The reason we pass by keyword argument is to make this
        # work logically both for free-floating functions as well
        # as [unbound] class methods.
        return f(*args, user=current_user(), **kws)

    return inner


def requires_login_redirect(f):
    """Decoractor to indicate that a particular route requires the user to be logged in.

    If the user is not logged in, they will be redirected to the front page.
    """

    @wraps(f)
    def inner(*args, **kws):
        if not is_user_logged_in():
            return redirect('/')
        # The reason we pass by keyword argument is to make this
        # work logically both for free-floating functions as well
        # as [unbound] class methods.
        return f(*args, user=current_user(), **kws)

    return inner


def requires_admin(f):
    """Similar to 'requires_login', but also tests that the user is an admin.

    The decorated function MUST declare an argument named 'user'.
    """

    @wraps(f)
    def inner(*args, **kws):
        just_logged_out = session.pop(JUST_LOGGED_OUT, False)
        if not is_user_logged_in() or not is_admin(current_user()):
            return redirect('/') if just_logged_out else utils.error_page(error=401, ui_message=gettext("unauthorized"))
        return f(*args, user=current_user(), **kws)

    return inner


def requires_teacher(f):
    """Similar to 'requires_login', but also tests that the user is a teacher.

    The decorated function MUST declare an argument named 'user'.
    """

    @wraps(f)
    def inner(*args, **kws):
        just_logged_out = session.pop(JUST_LOGGED_OUT, False)
        if not is_user_logged_in() or not is_teacher(current_user()):
            return redirect('/') if just_logged_out else utils.error_page(error=401, ui_message=gettext("unauthorized"))
        return f(*args, user=current_user(), **kws)

    return inner


def login_user_from_token_cookie():
    """Use the long-term token cookie in the user's request to try and look them up, if not already logged in."""
    if is_user_logged_in():
        return

    if not request.cookies.get(TOKEN_COOKIE_NAME):
        return

    token = g.db.get_token(request.cookies.get(TOKEN_COOKIE_NAME))
    if not token:
        return

    # We update the login record with the current time -> this way the last login is closer to correct
    g.db.record_login(token["username"])
    user = g.db.user_by_username(token["username"])
    if user:
        remember_current_user(user)


def validate_student_signup_data(account):
    if not isinstance(account.get("username"), str):
        return gettext("username_invalid")
    if "@" in account.get("username") or ":" in account.get("username"):
        return gettext("username_special")
    if len(account.get("username").strip()) < 3:
        return gettext("username_three")
    if not isinstance(account.get("password"), str):
        return gettext("password_invalid")
    if len(account.get("password")) < 6:
        return gettext("passwords_six")
    return None


def validate_signup_data(account):
    if not isinstance(account.get("username"), str):
        return gettext("username_invalid")
    if "@" in account.get("username") or ":" in account.get("username"):
        return gettext("username_special")
    if len(account.get("username").strip()) < 3:
        return gettext("username_three")
    if not isinstance(account.get("email"), str) or not utils.valid_email(account.get("email")):
        return gettext("email_invalid")
    if not isinstance(account.get("password"), str):
        return gettext("password_invalid")
    if len(account.get("password")) < 6:
        return gettext("passwords_six")
    return None


# Turn off verbose logs from boto/SES, thanks to https://github.com/boto/boto3/issues/521

for name in logging.Logger.manager.loggerDict.keys():
    if (
        ("boto" in name)
        or ("urllib3" in name)
        or ("s3transfer" in name)
        or ("boto3" in name)
        or ("botocore" in name)
        or ("nose" in name)
    ):
        logging.getLogger(name).setLevel(logging.CRITICAL)

# https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
email_client = boto3.client("ses", region_name=config["email"]["region"])


@querylog.timed
def send_email(recipient, subject, body_plain, body_html):
    try:
        email_client.send_email(
            Source=config["email"]["sender"],
            Destination={"ToAddresses": [recipient]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {
                    "Text": {"Data": body_plain, "Charset": "UTF-8"},
                    "Html": {"Data": body_html, "Charset": "UTF-8"},
                },
            },
        )
    except email_error as error:
        print("Email send error", error.response["Error"]["Message"])
    except NoCredentialsError as e:
        if not is_debug_mode():
            raise e
    else:
        print("Email sent to " + recipient)


def get_template_translation(template):
    if template == "welcome_verify":
        return gettext("mail_welcome_verify_body")
    elif template == "change_password":
        return gettext("mail_change_password_body")
    elif template == "recover_password":
        return gettext("mail_recover_password_body")
    elif template == "reset_password":
        return gettext("mail_reset_password_body")
    elif template == "welcome_teacher":
        return gettext("mail_welcome_teacher_body")
    return None


def get_subject_translation(template):
    if template == "welcome_verify":
        return gettext("mail_welcome_verify_subject")
    elif template == "change_password":
        return gettext("mail_change_password_subject")
    elif template == "recover_password":
        return gettext("mail_recover_password_subject")
    elif template == "reset_password":
        return gettext("mail_reset_password_subject")
    elif template == "welcome_teacher":
        return gettext("mail_welcome_teacher_subject")
    return None


def send_email_template(template, email, link=None, username=None):
    if username is None:
        username = gettext("user")
    subject = get_subject_translation(template)
    if not subject:
        print("Something went wrong, mail template could not be found...")
        return
    body = safe_format(gettext("mail_hello"), username=username) + "\n\n"
    body += get_template_translation(template) + "\n\n"
    body += gettext("mail_goodbye")

    with open("templates/email/base_email.html", "r", encoding="utf-8") as f:
        body_html = f.read()

    body_html = body_html.format(content=body)
    body_plain = body
    if link:
        body_plain = safe_format(body_plain, link=gettext("copy_mail_link") + " " + link)
        body_html = safe_format(body_html, link='<a href="' + link + '">{link}</a>')
        body_html = safe_format(body_html, link=gettext("link"))

    send_email(email, subject, body_plain, body_html)


# By default, emails are sent in the locale of the logged-in user.
# This function is to be used if the email needs to be sent in another locale.
# For example when an action by a logged in admin (like oking a teacher's account) triggers an email
def send_localized_email_template(locale, template, email, link=None, username=None):
    with force_locale(locale):
        if username is None:
            # We want to use the correct locale for this text
            username = gettext("user")
        send_email_template(template, email, link, username)


def store_new_student_account(db, account, teacher_username):
    username, hashed, hashed_token = prepare_user_db(account["username"], account["password"])
    user = {
        "username": username,
        "password": hashed,
        "language": account["language"],
        "keyword_language": account["keyword_language"],
        "created": timems(),
        "teacher": teacher_username,
        "verification_pending": hashed_token,
        "last_login": timems(),
    }
    db.store_user(user)
    return user


def prepare_user_db(username, password):
    hashed = password_hash(password, make_salt())

    token = make_salt()
    hashed_token = password_hash(token, make_salt())
    username = username.strip().lower()

    return username, hashed, hashed_token


def create_verify_link(username, token):
    email = email_base_url() + "/auth/verify?username="
    email += urllib.parse.quote_plus(username) + "&token=" + urllib.parse.quote_plus(token)
    return email


def email_base_url():
    """Return the base URL for the current site, without trailing slash.

    You only need to call this function to format links for emails. Links that get
    shown in HTML pages can start with a `/` and not include the host and they will
    still work correctly.

    Will use the environment variable BASE_URL if set, otherwise will guess using
    the current Flask request.
    """
    from_env = os.getenv("BASE_URL")
    if from_env:
        return from_env.rstrip("/")
    return request.host_url


def create_recover_link(username, token):
    email = email_base_url() + "/reset?username="
    email += urllib.parse.quote_plus(username) + "&token=" + urllib.parse.quote_plus(token)
    return email
