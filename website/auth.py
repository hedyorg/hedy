import collections
import os
from flask_babel import gettext
import utils
from hedy_content import COUNTRIES, ALL_LANGUAGES, ALL_KEYWORD_LANGUAGES
from website.yaml_file import YamlFile
import bcrypt
import re
import urllib
from flask import request, session, make_response, jsonify, redirect
from utils import timems, times, extract_bcrypt_rounds, is_testing_request, is_debug_mode, valid_email, is_heroku
import datetime
from functools import wraps
from config import config
import boto3
from botocore.exceptions import ClientError as email_error, NoCredentialsError
import json
import requests
from website import querylog, database
import hashlib

TOKEN_COOKIE_NAME = config['session']['cookie_name']
# The session_length in the session is set to 60 * 24 * 14 (in minutes) config.py#13
# The reset_length in the session is set to 60 * 4 (in minutes) config.py#14
# We multiply this by 60 to set the session_length to 14 days and reset_length to 4 hours
session_length = config['session']['session_length'] * 60
reset_length = config['session']['reset_length'] * 60

env = os.getenv('HEROKU_APP_NAME')

DATABASE: database.Database = None

MAILCHIMP_API_URL = None
if os.getenv('MAILCHIMP_API_KEY') and os.getenv('MAILCHIMP_AUDIENCE_ID'):
    # The domain in the path is the server name, which is contained in the Mailchimp API key
    MAILCHIMP_API_URL = 'https://' + os.getenv('MAILCHIMP_API_KEY').split('-')[
        1] + '.api.mailchimp.com/3.0/lists/' + os.getenv('MAILCHIMP_AUDIENCE_ID')
    MAILCHIMP_API_HEADERS = {'Content-Type': 'application/json',
                             'Authorization': 'apikey ' + os.getenv('MAILCHIMP_API_KEY')}


def mailchimp_subscribe_user(email):
    request_body = {'email_address': email, 'status': 'subscribed'}
    r = requests.post(MAILCHIMP_API_URL + '/members', headers=MAILCHIMP_API_HEADERS, data=json.dumps(request_body))

    subscription_error = None
    if r.status_code != 200 and r.status_code != 400:
        subscription_error = True
    # We can get a 400 if the email is already subscribed to the list. We should ignore this error.
    if r.status_code == 400 and not re.match('.*already a list member', r.text):
        subscription_error = True
    # If there's an error in subscription through the API, we report it to the main email address
    if subscription_error:
        send_email(config['email']['sender'], 'ERROR - Subscription to Hedy newsletter on signup', email,
                   '<p>' + email + '</p><pre>Status:' + str(r.status_code) + '    Body:' + r.text + '</pre>')


@querylog.timed
def check_password(password, hash):
    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(hash, 'utf-8'))


def make_salt():
    return bcrypt.gensalt(rounds=config['bcrypt_rounds']).decode('utf-8')


@querylog.timed
def hash(password, salt):
    return bcrypt.hashpw(bytes(password, 'utf-8'), bytes(salt, 'utf-8')).decode('utf-8')


# The current user is a slice of the user information from the database and placed on the Flask session.
# The main purpose of the current user is to provide a convenient container for
# * username
# * email
# * is_teacher
#
# Since the is_teacher can be changed during a session we also store a time-to-live. When retrieving the current user, we can check if we need to reload data from the database.
#
# The current user should be retrieved with `current_user` function since it will return a sane default.
# You can remove the current user from the Flask session with the `forget_current_user`.
def remember_current_user(db_user):
    session['user-ttl'] = times() + 5 * 60
    session['user'] = pick(db_user, 'username', 'email', 'is_teacher')
    session['lang'] = db_user.get('language', 'en')
    session['keyword_lang'] = db_user.get('keyword_language', 'en')


def pick(d, *requested_keys):
    return {key: d.get(key, None) for key in requested_keys}


# Retrieve the current user from the Flask session.
#
# If the current user is to old, as determined by the time-to-live, we repopulate from the database.
def current_user():
    now = times()
    user = session.get('user', {'username': '', 'email': ''})
    ttl = session.get('user-ttl', None)
    if ttl == None or now >= ttl:
        username = user['username']
        if username:
            db_user = DATABASE.user_by_username(username)
            remember_current_user(db_user)

    return user


def is_user_logged_in():
    """Return whether or not a user is currently logged in."""
    return bool(current_user()['username'])


# Remove the current info from the Flask session.
def forget_current_user():
    session.pop('user', None)  # We are not interested in the value of the use key.
    session.pop('achieved', None)  # Delete session achievements if existing
    session.pop('keyword_lang', None)  # Delete session keyword language if existing


def is_admin(user):
    admin_user = os.getenv('ADMIN_USER')
    return user.get('username') == admin_user or user.get('email') == admin_user


def is_teacher(user):
    # the `is_teacher` field is either `0`, `1` or not present.
    return bool(user.get('is_teacher', False))


def update_is_teacher(user, is_teacher_value=1):
    user_is_teacher = is_teacher(user)
    user_becomes_teacher = is_teacher_value and not user_is_teacher

    DATABASE.update_user(user['username'], {'is_teacher': is_teacher_value})

    if user_becomes_teacher and not is_testing_request(request):
        send_email_template(template='welcome_teacher', email=user['email'], username=user['username'])


# Thanks to https://stackoverflow.com/a/34499643
def requires_login(f):
    @wraps(f)
    def inner(*args, **kws):
        if not is_user_logged_in():
            return utils.error_page(error=403)
        return f(current_user(), *args, **kws)

    return inner


def login_user_from_token_cookie():
    """Use the long-term token cookie in the user's request to try and look them up, if not already logged in."""
    if is_user_logged_in():
        return

    if not request.cookies.get(TOKEN_COOKIE_NAME):
        return

    token = DATABASE.get_token(request.cookies.get(TOKEN_COOKIE_NAME))
    if not token:
        return

    # We update the login record with the current time -> this way the last login is closer to correct
    DATABASE.record_login(token['username'])
    user = DATABASE.user_by_username(token['username'])
    if user:
        remember_current_user(user)


def prepare_user_db(username, password):
    hashed = hash(password, make_salt())

    token = make_salt()
    hashed_token = hash(token, make_salt())
    username = username.strip().lower()

    return username, hashed, hashed_token

def validate_student_signup_data(account):
    if not isinstance(account.get('username'), str):
        return gettext('username_invalid')
    if '@' in account.get('username') or ':' in account.get('username'):
        return gettext('username_special')
    if len(account.get('username').strip()) < 3:
        return gettext('username_three')
    if not isinstance(account.get('password'), str):
        return gettext('password_invalid')
    if len(account.get('password')) < 6:
        return gettext('passwords_six')
    return None

def validate_signup_data(account):
    if not isinstance(account.get('username'), str):
        return gettext('username_invalid')
    if '@' in account.get('username') or ':' in account.get('username'):
        return gettext('username_special')
    if len(account.get('username').strip()) < 3:
        return gettext('username_three')
    if not isinstance(account.get('email'), str) or not utils.valid_email(account.get('email')):
        return gettext('email_invalid')
    if not isinstance(account.get('password'), str):
        return gettext('password_invalid')
    if len(account.get('password')) < 6:
        return gettext('passwords_six')
    return None


def store_new_student_account(account, teacher_username):
    username, hashed, hashed_token = prepare_user_db(account['username'], account['password'])
    user = {
        'username': username,
        'password': hashed,
        'language': account['language'],
        'keyword_language': account['keyword_language'],
        'created': timems(),
        'teacher': teacher_username,
        'verification_pending': hashed_token,
        'last_login': timems()
    }
    DATABASE.store_user(user)
    return user


def store_new_account(account, email):
    username, hashed, hashed_token = prepare_user_db(account['username'], account['password'])
    user = {
        'username': username,
        'password': hashed,
        'email': email,
        'language': account['language'],
        'keyword_language': account['keyword_language'],
        'created': timems(),
        'verification_pending': hashed_token,
        'last_login': timems()
    }

    for field in ['country', 'birth_year', 'gender', 'language', 'prog_experience', 'experience_languages']:
        if field in account:
            if field == 'experience_languages' and len(account[field]) == 0:
                continue
            user[field] = account[field]

    DATABASE.store_user(user)

    # If this is an e2e test, we return the email verification token directly instead of emailing it.
    if is_testing_request(request):
        resp = make_response({'username': username, 'token': hashed_token})
    # Otherwise, we send an email with a verification link and we return an empty body
    else:
        send_email_template(template='welcome_verify', email=email,
                            link=create_verify_link(username, hashed_token), username=user['username'])
        resp = make_response({})
    return user, resp


def create_recover_link(username, token):
    email = email_base_url() + '/reset?username='
    email += urllib.parse.quote_plus(username) + '&token=' + urllib.parse.quote_plus(token)
    return email


def create_verify_link(username, token):
    email = email_base_url() + '/auth/verify?username='
    email += urllib.parse.quote_plus(username) + '&token=' + urllib.parse.quote_plus(token)
    return email

# Note: translations are used only for texts that will be seen by a GUI user.
def routes(app, database):
    global DATABASE
    DATABASE = database

    @app.route('/auth/login', methods=['POST'])
    def login():
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return gettext('username_invalid'), 400
        if not isinstance(body.get('password'), str):
            return gettext('password_invalid'), 400

        # If username has an @-sign, then it's an email
        if '@' in body['username']:
            user = DATABASE.user_by_email(body['username'])
        else:
            user = DATABASE.user_by_username(body['username'])

        if not user or not check_password(body['password'], user['password']):
            return gettext('invalid_username_password') + " " + gettext('no_account'), 403

        # If the number of bcrypt rounds has changed, create a new hash.
        new_hash = None
        if config['bcrypt_rounds'] != extract_bcrypt_rounds(user['password']):
            new_hash = hash(body['password'], make_salt())

        cookie = make_salt()
        DATABASE.store_token({'id': cookie, 'username': user['username'], 'ttl': times() + session_length})
        if new_hash:
            DATABASE.record_login(user['username'], new_hash)
        else:
            DATABASE.record_login(user['username'])

        if is_admin(user):
            resp = make_response({'admin': True})
        elif user.get('is_teacher'):
            resp = make_response({'teacher': True})
        else:
            resp = make_response({'teacher': False})

        # We set the cookie to expire in a year, just so that the browser won't invalidate it if the same cookie gets renewed by constant use.
        # The server will decide whether the cookie expires.
        resp.set_cookie(TOKEN_COOKIE_NAME, value=cookie, httponly=True, secure=is_heroku(), samesite='Lax', path='/',
                        max_age=365 * 24 * 60 * 60)

        # Remember the current user on the session. This is "new style" logins, which should ultimately
        # replace "old style" logins (with the cookie above), as it requires fewer database calls.
        remember_current_user(user)
        return resp

    @app.route('/auth/signup', methods=['POST'])
    def signup():
        body = request.json
        # Validations, mandatory fields
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400

        # Validate the essential data using a function -> also used for multiple account creation
        validation = validate_signup_data(body)
        if validation:
            return validation, 400

        # Validate fields only relevant when creating a single user account
        if not isinstance(body.get('mail_repeat'), str) or not valid_email(body['mail_repeat']):
            return gettext('repeat_match_email'), 400
        if body['email'] != body['mail_repeat']:
            return gettext('repeat_match_email'), 400
        if not isinstance(body.get('password_repeat'), str) or body['password'] != body['password_repeat']:
            return gettext('repeat_match_password'), 400
        if not isinstance(body.get('language'), str) or body.get('language') not in ALL_LANGUAGES.keys():
            return gettext('language_invalid'), 400
        if not isinstance(body.get('agree_terms'), bool) or not body.get('agree_terms'):
            return gettext('agree_invalid'), 400
        if not isinstance(body.get('keyword_language'), str) or body.get('keyword_language') not in ['en', body.get('language')]:
            return gettext('keyword_language_invalid'), 400

        # Validations, optional fields
        if 'birth_year' in body:
            if not isinstance(body.get('birth_year'), int) or body['birth_year'] <= 1900 or body['birth_year'] > datetime.datetime.now().year:
                return (gettext('year_invalid') + str(datetime.datetime.now().year)), 400
        if 'gender' in body:
            if body['gender'] != 'm' and body['gender'] != 'f' and body['gender'] != 'o':
                return gettext('gender_invalid'), 400
        if 'country' in body:
            if not body['country'] in COUNTRIES:
                return gettext('country_invalid'), 400
        if 'prog_experience' in body and body['prog_experience'] not in ['yes', 'no']:
            return gettext('experience_invalid'), 400
        if 'experience_languages' in body:
            if not isinstance(body['experience_languages'], list):
                return gettext('experience_invalid'), 400
            for language in body['experience_languages']:
                if language not in['scratch', 'other_block', 'python', 'other_text']:
                    return gettext('programming_invalid'), 400

        if DATABASE.user_by_username(body['username'].strip().lower()):
            return gettext('exists_username'), 403
        if DATABASE.user_by_email(body['email'].strip().lower()):
            return gettext('exists_email'), 403

        # We receive the pre-processed user and response package from the function
        user, resp = store_new_account(body, body['email'].strip().lower())

        if not is_testing_request(request) and 'subscribe' in body and body['subscribe'] is True:
            # If we have a Mailchimp API key, we use it to add the subscriber through the API
            if MAILCHIMP_API_URL:
                mailchimp_subscribe_user(user['email'])
            # Otherwise, we send an email to notify about the subscription to the main email address
            else:
                send_email(config['email']['sender'], 'Subscription to Hedy newsletter on signup', user['email'],
                           '<p>' + user['email'] + '</p>')

        # If someone wants to be a Teacher -> sent a mail to manually set it
        if not is_testing_request(request) and 'is_teacher' in body and body['is_teacher'] is True:
            send_email(config['email']['sender'], 'Request for teacher\'s interface on signup', user['email'],
                       '<p>' + user['email'] + '</p>')

        # If someone agrees to the third party contacts -> sent a mail to manually write down
        if not is_testing_request(request) and 'agree_third_party' in body and body['agree_third_party'] is True:
            send_email(config['email']['sender'], 'Agreement to Third party offers on signup', user['email'],
                       '<p>' + user['email'] + '</p>')

        # We automatically login the user
        cookie = make_salt()
        DATABASE.store_token({'id': cookie, 'username': user['username'], 'ttl': times() + session_length})
        # We set the cookie to expire in a year, just so that the browser won't invalidate it if the same cookie gets renewed by constant use.
        # The server will decide whether the cookie expires.
        resp.set_cookie(TOKEN_COOKIE_NAME, value=cookie, httponly=True, secure=is_heroku(), samesite='Lax', path='/',
                        max_age=365 * 24 * 60 * 60)

        remember_current_user(user)
        return resp

    @app.route('/auth/verify', methods=['GET'])
    def verify_email():
        username = request.args.get('username', None)
        token = request.args.get('token', None)
        if not token:
            return gettext('token_invalid'), 400
        if not username:
            return gettext('username_invalid'), 400

        # Verify that user actually exists
        user = DATABASE.user_by_username(username)
        if not user:
            return gettext('username_invalid'), 403

        # If user is already verified -> re-direct to landing-page anyway
        if not 'verification_pending' in user:
            return redirect('/landing-page')

        # Verify the token
        if token != user['verification_pending']:
            return gettext('token_invalid'), 403

        # Remove the token from the user
        DATABASE.update_user(username, {'verification_pending': None})

        # We automatically login the user
        cookie = make_salt()
        DATABASE.store_token({'id': cookie, 'username': user['username'], 'ttl': times() + session_length})
        remember_current_user(user)

        return redirect('/landing-page')

    @app.route('/auth/logout', methods=['POST'])
    def logout():
        forget_current_user()
        if request.cookies.get(TOKEN_COOKIE_NAME):
            DATABASE.forget_token(request.cookies.get(TOKEN_COOKIE_NAME))
        return '', 200

    @app.route('/auth/destroy', methods=['POST'])
    @requires_login
    def destroy(user):
        forget_current_user()
        DATABASE.forget_token(request.cookies.get(TOKEN_COOKIE_NAME))
        DATABASE.forget_user(user['username'])
        return '', 200

    @app.route('/auth/destroy_public', methods=['POST'])
    @requires_login
    def destroy_public(user):
        DATABASE.forget_public_profile(user['username'])
        return '', 200

    @app.route('/auth/change_student_password', methods=['POST'])
    @requires_login
    def change_student_password(user):
        body = request.json
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return gettext('username_invalid'), 400
        if not isinstance(body.get('password'), str):
            return gettext('password_invalid'), 400
        if len(body['password']) < 6:
            return gettext('password_six'), 400

        if not is_teacher(user):
            return gettext("password_change_not_allowed"), 400
        students = DATABASE.get_teacher_students(user['username'])
        if body['username'] not in students:
            return gettext("password_change_not_allowed"), 400

        hashed = hash(body['password'], make_salt())
        DATABASE.update_user(body['username'], {'password': hashed})

        return {'success': gettext("password_change_success")}, 200

    @app.route('/auth/change_password', methods=['POST'])
    @requires_login
    def change_password(user):
        body = request.json

        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('old_password'), str) or not isinstance(body.get('password'), str):
            return gettext('password_invalid'), 400
        if not isinstance(body.get( 'password_repeat'), str):
            return gettext('repeat_match_password'), 400
        if len(body['password']) < 6:
            return gettext('password_six'), 400
        if body['password'] != body['password_repeat']:
            return gettext('repeat_match_password'), 400

        # The user object we got from 'requires_login' doesn't have the password, so look that up in the database
        user = DATABASE.user_by_username(user['username'])

        if not check_password(body['old_password'], user['password']):
            return gettext('password_invalid'), 403

        hashed = hash(body['password'], make_salt())

        DATABASE.update_user(user['username'], {'password': hashed})
        # We are not updating the user in the Flask session, because we should not rely on the password in anyway.
        if not is_testing_request(request):
            send_email_template(template='change_password', email=user['email'], username=user['username'])

        return gettext('password_updated'), 200

    @app.route('/profile', methods=['POST'])
    @requires_login
    def update_profile(user):
        body = request.json
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('language'), str) or body.get('language') not in ALL_LANGUAGES.keys():
            return gettext('language_invalid'), 400
        if not isinstance(body.get('keyword_language'), str) or body.get('keyword_language') not in ['en', body.get(
                'language')] or body.get('keyword_language') not in ALL_KEYWORD_LANGUAGES.keys():
            return gettext('keyword_language_invalid'), 400

        # Mail is a unique field, only mandatory if the user doesn't have a related teacher (and no mail adress)
        user = DATABASE.user_by_username(user['username'])
        if user.get('email') and not user.get('teacher'):
            if not isinstance(body.get('email'), str) or not valid_email(body['email']):
                return gettext('email_invalid'), 400

        # Validations, optional fields
        if 'birth_year' in body:
            if not isinstance(body.get('birth_year'), int) or body['birth_year'] <= 1900 or body['birth_year'] > datetime.datetime.now().year:
                return gettext('year_invalid') + str(datetime.datetime.now().year), 400
        if 'gender' in body:
            if body['gender'] != 'm' and body['gender'] != 'f' and body['gender'] != 'o':
                return gettext('gender_invalid'), 400
        if 'country' in body:
            if not body['country'] in COUNTRIES:
                return gettext('country_invalid'), 400
        if 'prog_experience' in body and body['prog_experience'] not in ['yes', 'no']:
            return gettext('experience_invalid'), 400
        if 'experience_languages' in body:
            if not isinstance(body['experience_languages'], list):
                return gettext('experience_invalid'), 400
            for language in body['experience_languages']:
                if language not in['scratch', 'other_block', 'python', 'other_text']:
                    return gettext('programming_invalid'), 400

        resp = {}
        if 'email' in body:
            email = body['email'].strip().lower()
            if email != user.get('email'):
                exists = DATABASE.user_by_email(email)
                if exists:
                    return gettext('exists_email'), 403
                token = make_salt()
                hashed_token = hash(token, make_salt())
                DATABASE.update_user(user['username'], {'email': email, 'verification_pending': hashed_token})
                # If this is an e2e test, we return the email verification token directly instead of emailing it.
                if is_testing_request(request):
                    resp = {'username': user['username'], 'token': hashed_token}
                else:
                    send_email_template(template='welcome_verify', email=email,
                                        link=create_verify_link(user['username'], hashed_token),
                                        username=user['username'])

                # We check whether the user is in the Mailchimp list.
                if not is_testing_request(request) and MAILCHIMP_API_URL:
                    # We hash the email with md5 to avoid emails with unescaped characters triggering errors
                    request_path = MAILCHIMP_API_URL + '/members/' + hashlib.md5(
                        user['email'].encode('utf-8')).hexdigest()
                    r = requests.get(request_path, headers=MAILCHIMP_API_HEADERS)
                    # If user is subscribed, we remove the old email from the list and add the new one
                    if r.status_code == 200:
                        r = requests.delete(request_path, headers=MAILCHIMP_API_HEADERS)
                        mailchimp_subscribe_user(email)

        username = user['username']

        updates = {}
        for field in ['country', 'birth_year', 'gender', 'language', 'keyword_language']:
            if field in body:
                updates[field] = body[field]
            else:
                updates[field] = None

        if updates:
            DATABASE.update_user(username, updates)

        # We want to check if the user choose a new language, if so -> reload
        # We can use g.lang for this to reduce the db calls
        resp['reload'] = False
        if session['lang'] != body['language'] or session['keyword_lang'] != body['keyword_language']:
            resp['message'] = gettext('profile_updated')
            resp['reload'] = True
        else:
            resp['message'] = gettext('profile_updated_reload')

        remember_current_user(DATABASE.user_by_username(user['username']))
        return jsonify(resp)

    @app.route('/profile', methods=['GET'])
    @requires_login
    def get_profile(user):
        # The user object we got from 'requires_login' is not fully hydrated yet. Look up the database user.
        user = DATABASE.user_by_username(user['username'])

        output = {'username': user['username'], 'email': user['email'], 'language': user.get('language', 'en')}
        for field in ['birth_year', 'country', 'gender', 'prog_experience', 'experience_languages']:
            if field in user:
                output[field] = user[field]
        if 'verification_pending' in user:
            output['verification_pending'] = True

        output['student_classes'] = DATABASE.get_student_classes(user['username'])

        output['session_expires_at'] = timems() + session_length * 1000

        return jsonify(output), 200

    @app.route('/auth/recover', methods=['POST'])
    def recover():
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return gettext('username_invalid'), 400

        # If username has an @-sign, then it's an email
        if '@' in body['username']:
            user = DATABASE.user_by_email(body['username'].strip().lower())
        else:
            user = DATABASE.user_by_username(body['username'].strip().lower())

        if not user:
            return gettext('username_invalid'), 403

        # In this case -> account has a related teacher (and is a student)
        # We still store the token, but sent the mail to the teacher instead
        if user.get('teacher') and not user.get('email'):
            email = DATABASE.user_by_username(user.get('teacher')).get('email')
        else:
            email = user['email']

        # Create a token -> use the reset_length value as we don't want the token to live as long as a login one
        token = make_salt()
        # Todo TB -> Don't we want to use a hashed token here as well?
        DATABASE.store_token({'id': token, 'username': user['username'], 'ttl': times() + reset_length})

        if is_testing_request(request):
            # If this is an e2e test, we return the email verification token directly instead of emailing it.
            return jsonify({'username': user['username'], 'token': token}), 200
        else:
            send_email_template(template='recover_password', email=email,
                                link=create_recover_link(user['username'], token), username=user['username'])
            return jsonify({'message':gettext('sent_password_recovery')}), 200

    @app.route('/auth/reset', methods=['POST'])
    def reset():
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return gettext('username_invalid'), 400
        if not isinstance(body.get('token'), str):
            return gettext('token_invalid'), 400
        if not isinstance(body.get('password'), str):
            return gettext('password_invalid'), 400
        if len(body['password']) < 6:
            return gettext('password_six'), 400
        if not isinstance(body.get('password_repeat'), str) or body['password'] != body['password_repeat']:
            return gettext('repeat_match_password'), 400

        token = DATABASE.get_token(body['token'])
        if not token or body['token'] != token.get('id'):
            return gettext('token_invalid'), 403

        hashed = hash(body['password'], make_salt())
        DATABASE.update_user(body['username'], {'password': hashed})
        user = DATABASE.user_by_username(body['username'])

        # Delete all tokens of the user -> automatically logout all long-lived sessions
        DATABASE.delete_all_tokens(body['username'])

        # In this case -> account has a related teacher (and is a student)
        # We mail the teacher instead
        if user.get('teacher') and not user.get('email'):
            email = DATABASE.user_by_username(user.get('teacher')).get('email')
        else:
            email = user['email']

        if not is_testing_request(request):
            send_email_template(template='reset_password', email=email, username=user['username'])

        return jsonify({'message':gettext('password_resetted')}), 200

    # *** ADMIN ROUTES ***

    @app.route('/admin/markAsTeacher', methods=['POST'])
    def mark_as_teacher():
        user = current_user()
        if not is_admin(user) and not is_testing_request(request):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        body = request.json

        # Validations
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return gettext('username_invalid'), 400
        if not isinstance(body.get('is_teacher'), bool):
            return gettext('teacher_invalid'), 400

        user = DATABASE.user_by_username(body['username'].strip().lower())

        if not user:
            return gettext('username_invalid'), 400

        is_teacher_value = 1 if body['is_teacher'] else 0
        update_is_teacher(user, is_teacher_value)

        # Todo TB feb 2022 -> Return the success message here instead of fixing in the front-end
        return '', 200

    @app.route('/admin/changeUserEmail', methods=['POST'])
    def change_user_email():
        user = current_user()
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        body = request.json

        # Validations
        if not isinstance(body, dict):
            return gettext('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return gettext('username_invalid'), 400
        if not isinstance(body.get('email'), str) or not valid_email(body['email']):
            return gettext('email_invalid'), 400

        user = DATABASE.user_by_username(body['username'].strip().lower())

        if not user:
            return gettext('email_invalid'), 400

        token = make_salt()
        hashed_token = hash(token, make_salt())

        # We assume that this email is not in use by any other users. In other words, we trust the admin to enter a valid, not yet used email address.
        DATABASE.update_user(user['username'], {'email': body['email'], 'verification_pending': hashed_token})

        # If this is an e2e test, we return the email verification token directly instead of emailing it.
        if is_testing_request(request):
            resp = {'username': user['username'], 'token': hashed_token}
        else:
            send_email_template(template='welcome_verify', email=body['email'],
                                link=create_verify_link(user['username'], hashed_token),
                                username=user['username'])

        return {}, 200


# Turn off verbose logs from boto/SES, thanks to https://github.com/boto/boto3/issues/521
import logging

for name in logging.Logger.manager.loggerDict.keys():
    if ('boto' in name) or ('urllib3' in name) or ('s3transfer' in name) or ('boto3' in name) or (
            'botocore' in name) or ('nose' in name):
        logging.getLogger(name).setLevel(logging.CRITICAL)

# https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
email_client = boto3.client('ses', region_name=config['email']['region'])


@querylog.timed
def send_email(recipient, subject, body_plain, body_html):
    try:
        result = email_client.send_email(
            Source=config['email']['sender'],
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {'Data': body_plain, 'Charset': 'UTF-8'},
                    'Html': {'Data': body_html, 'Charset': 'UTF-8'},
                }
            }
        )
    except email_error as error:
        print('Email send error', error.response['Error']['Message'])
    except NoCredentialsError as e:
        if not is_debug_mode():
            raise e
    else:
        print('Email sent to ' + recipient)


def get_template_translation(template):
    if template == 'welcome_verify':
        return gettext('mail_welcome_verify_body')
    elif template == 'change_password':
        return gettext('mail_change_password_body')
    elif template == 'recover_password':
        return gettext('mail_recover_password_body')
    elif template == 'reset_password':
        return gettext('mail_reset_password_body')
    elif template == 'welcome_teacher':
        return gettext('mail_welcome_teacher_body')
    return None


def get_subject_translation(template):
    if template == 'welcome_verify':
        return gettext('mail_welcome_verify_subject')
    elif template == 'change_password':
        return gettext('mail_change_password_subject')
    elif template == 'recover_password':
        return gettext('mail_recover_password_subject')
    elif template == 'reset_password':
        return gettext('mail_reset_password_subject')
    elif template == 'welcome_teacher':
        return gettext('mail_welcome_teacher_subject')
    return None


def send_email_template(template, email, link=None, username=gettext('user')):
    subject = get_subject_translation(template)
    if not subject:
        print("Something went wrong, mail template could not be found...")
        return
    body = gettext('mail_hello').format(username=username) + "\n\n"
    body += get_template_translation(template) + "\n\n"
    body += gettext('mail_goodbye')

    with open('templates/base_email.html', 'r', encoding='utf-8') as f:
        body_html = f.read()

    body_html = body_html.format(content=body)
    body_plain = body
    if link:
        body_plain = body_plain.format(link=gettext('copy_mail_link') + " " + link)
        body_html = body_html.format(link='<a href="' + link + '">{link}</a>').format(link=gettext('link'))

    send_email(email, subject, body_plain, body_html)


def email_base_url():
    """Return the base URL for the current site, without trailing slash.

    You only need to call this function to format links for emails. Links that get
    shown in HTML pages can start with a `/` and not include the host and they will
    still work correctly.

    Will use the environment variable BASE_URL if set, otherwise will guess using
    the current Flask request.
    """
    from_env = os.getenv('BASE_URL')
    if from_env:
        return from_env.rstrip('/')
    return request.host_url
