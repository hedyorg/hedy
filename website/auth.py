import os

import utils
from website.yaml_file import YamlFile
import bcrypt
import re
import urllib
from flask import request, session, make_response, jsonify, redirect, g
from flask_helpers import render_template
from utils import timems, times, extract_bcrypt_rounds, is_testing_request, is_debug_mode, valid_email, is_heroku, mstoisostring
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
session_length    = config['session']['session_length'] * 60

env = os.getenv('HEROKU_APP_NAME')

DATABASE: database.Database = None

MAILCHIMP_API_URL = None
if os.getenv('MAILCHIMP_API_KEY') and os.getenv('MAILCHIMP_AUDIENCE_ID'):
    # The domain in the path is the server name, which is contained in the Mailchimp API key
    MAILCHIMP_API_URL = 'https://' + os.getenv('MAILCHIMP_API_KEY').split('-')[1] + '.api.mailchimp.com/3.0/lists/' + os.getenv('MAILCHIMP_AUDIENCE_ID')
    MAILCHIMP_API_HEADERS = {'Content-Type': 'application/json', 'Authorization': 'apikey ' + os.getenv('MAILCHIMP_API_KEY')}

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
        send_email(config['email']['sender'], 'ERROR - Subscription to Hedy newsletter on signup', email, '<p>' + email + '</p><pre>Status:' + str(r.status_code) + '    Body:' + r.text + '</pre>')

@querylog.timed
def check_password(password, hash):
    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(hash, 'utf-8'))

def make_salt():
    return bcrypt.gensalt(rounds=config['bcrypt_rounds']).decode('utf-8')

@querylog.timed
def hash(password, salt):
    return bcrypt.hashpw(bytes(password, 'utf-8'), bytes(salt, 'utf-8')).decode('utf-8')

countries = {'AF':'Afghanistan','AX':'Åland Islands','AL':'Albania','DZ':'Algeria','AS':'American Samoa','AD':'Andorra','AO':'Angola','AI':'Anguilla','AQ':'Antarctica','AG':'Antigua and Barbuda','AR':'Argentina','AM':'Armenia','AW':'Aruba','AU':'Australia','AT':'Austria','AZ':'Azerbaijan','BS':'Bahamas','BH':'Bahrain','BD':'Bangladesh','BB':'Barbados','BY':'Belarus','BE':'Belgium','BZ':'Belize','BJ':'Benin','BM':'Bermuda','BT':'Bhutan','BO':'Bolivia, Plurinational State of','BQ':'Bonaire, Sint Eustatius and Saba','BA':'Bosnia and Herzegovina','BW':'Botswana','BV':'Bouvet Island','BR':'Brazil','IO':'British Indian Ocean Territory','BN':'Brunei Darussalam','BG':'Bulgaria','BF':'Burkina Faso','BI':'Burundi','KH':'Cambodia','CM':'Cameroon','CA':'Canada','CV':'Cape Verde','KY':'Cayman Islands','CF':'Central African Republic','TD':'Chad','CL':'Chile','CN':'China','CX':'Christmas Island','CC':'Cocos(Keeling) Islands','CO':'Colombia','KM':'Comoros','CG':'Congo','CD':'Congo, the Democratic Republic of the','CK':'Cook Islands','CR':'Costa Rica','CI':'Côte d\'Ivoire','HR':'Croatia','CU':'Cuba','CW':'Curaçao','CY':'Cyprus','CZ':'Czech Republic','DK':'Denmark','DJ':'Djibouti','DM':'Dominica','DO':'Dominican Republic','EC':'Ecuador','EG':'Egypt','SV':'El Salvador','GQ':'Equatorial Guinea','ER':'Eritrea','EE':'Estonia','ET':'Ethiopia','FK':'Falkland Islands(Malvinas)','FO':'Faroe Islands','FJ':'Fiji','FI':'Finland','FR':'France','GF':'French Guiana','PF':'French Polynesia','TF':'French Southern Territories','GA':'Gabon','GM':'Gambia','GE':'Georgia','DE':'Germany','GH':'Ghana','GI':'Gibraltar','GR':'Greece','GL':'Greenland','GD':'Grenada','GP':'Guadeloupe','GU':'Guam','GT':'Guatemala','GG':'Guernsey','GN':'Guinea','GW':'Guinea-Bissau','GY':'Guyana','HT':'Haiti','HM':'Heard Island and McDonald Islands','VA':'Holy See(Vatican City State)','HN':'Honduras','HK':'Hong Kong','HU':'Hungary','IS':'Iceland','IN':'India','ID':'Indonesia','IR':'Iran, Islamic Republic of','IQ':'Iraq','IE':'Ireland','IM':'Isle of Man','IL':'Israel','IT':'Italy','JM':'Jamaica','JP':'Japan','JE':'Jersey','JO':'Jordan','KZ':'Kazakhstan','KE':'Kenya','KI':'Kiribati','KP':'Korea, Democratic People\'s Republic of','KR':'Korea, Republic of','KW':'Kuwait','KG':'Kyrgyzstan','LA':'Lao People\'s Democratic Republic','LV':'Latvia','LB':'Lebanon','LS':'Lesotho','LR':'Liberia','LY':'Libya','LI':'Liechtenstein','LT':'Lithuania','LU':'Luxembourg','MO':'Macao','MK':'Macedonia, the Former Yugoslav Republic of','MG':'Madagascar','MW':'Malawi','MY':'Malaysia','MV':'Maldives','ML':'Mali','MT':'Malta','MH':'Marshall Islands','MQ':'Martinique','MR':'Mauritania','MU':'Mauritius','YT':'Mayotte','MX':'Mexico','FM':'Micronesia, Federated States of','MD':'Moldova, Republic of','MC':'Monaco','MN':'Mongolia','ME':'Montenegro','MS':'Montserrat','MA':'Morocco','MZ':'Mozambique','MM':'Myanmar','NA':'Namibia','NR':'Nauru','NP':'Nepal','NL':'Netherlands','NC':'New Caledonia','NZ':'New Zealand','NI':'Nicaragua','NE':'Niger','NG':'Nigeria','NU':'Niue','NF':'Norfolk Island','MP':'Northern Mariana Islands','NO':'Norway','OM':'Oman','PK':'Pakistan','PW':'Palau','PS':'Palestine, State of','PA':'Panama','PG':'Papua New Guinea','PY':'Paraguay','PE':'Peru','PH':'Philippines','PN':'Pitcairn','PL':'Poland','PT':'Portugal','PR':'Puerto Rico','QA':'Qatar','RE':'Réunion','RO':'Romania','RU':'Russian Federation','RW':'Rwanda','BL':'Saint Barthélemy','SH':'Saint Helena, Ascension and Tristan da Cunha','KN':'Saint Kitts and Nevis','LC':'Saint Lucia','MF':'Saint Martin(French part)','PM':'Saint Pierre and Miquelon','VC':'Saint Vincent and the Grenadines','WS':'Samoa','SM':'San Marino','ST':'Sao Tome and Principe','SA':'Saudi Arabia','SN':'Senegal','RS':'Serbia','SC':'Seychelles','SL':'Sierra Leone','SG':'Singapore','SX':'Sint Maarten(Dutch part)','SK':'Slovakia','SI':'Slovenia','SB':'Solomon Islands','SO':'Somalia','ZA':'South Africa','GS':'South Georgia and the South Sandwich Islands','SS':'South Sudan','ES':'Spain','LK':'Sri Lanka','SD':'Sudan','SR':'Suriname','SJ':'Svalbard and Jan Mayen','SZ':'Swaziland','SE':'Sweden','CH':'Switzerland','SY':'Syrian Arab Republic','TW':'Taiwan, Province of China','TJ':'Tajikistan','TZ':'Tanzania, United Republic of','TH':'Thailand','TL':'Timor-Leste','TG':'Togo','TK':'Tokelau','TO':'Tonga','TT':'Trinidad and Tobago','TN':'Tunisia','TR':'Turkey','TM':'Turkmenistan','TC':'Turks and Caicos Islands','TV':'Tuvalu','UG':'Uganda','UA':'Ukraine','AE':'United Arab Emirates','GB':'United Kingdom','US':'United States','UM':'United States Minor Outlying Islands','UY':'Uruguay','UZ':'Uzbekistan','VU':'Vanuatu','VE':'Venezuela, Bolivarian Republic of','VN':'Viet Nam','VG':'Virgin Islands, British','VI':'Virgin Islands, U.S.','WF':'Wallis and Futuna','EH':'Western Sahara','YE':'Yemen','ZM':'Zambia','ZW':'Zimbabwe'};

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

def pick(d, *requested_keys):
    return { key : d.get(key, None) for key in requested_keys }

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
    session.pop('user', None) # We are not interested in the value of the use key.
    session.pop('achieved', None) # Delete session achievements if existing


def is_admin(user):
    admin_user = os.getenv('ADMIN_USER')
    return user['username'] == admin_user or user['email'] == admin_user

def is_teacher(user):
    # the `is_teacher` field is either `0`, `1` or not present.
    return bool(user.get('is_teacher', False))

def update_is_teacher(user, is_teacher_value=1):
    user_is_teacher = is_teacher(user)
    user_becomes_teacher = is_teacher_value and not user_is_teacher

    DATABASE.update_user(user['username'], {'is_teacher': is_teacher_value})

    if user_becomes_teacher and not is_testing_request(request):
        send_email_template('welcome_teacher', user['email'], '')


EMAILS = YamlFile.for_file('website/emails.yaml')

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

    user = DATABASE.user_by_username(token['username'])
    if user:
        remember_current_user(user)

# Note: translations are used only for texts that will be seen by a GUI user.
def routes(app, database):
    global DATABASE
    DATABASE = database

    @app.route('/auth/login', methods=['POST'])
    def login():
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return g.auth_texts.get('username_invalid'), 400
        if not isinstance(body.get('password'), str):
            return g.auth_texts.get('password_invalid'), 400

        # If username has an @-sign, then it's an email
        if '@' in body['username']:
            user = DATABASE.user_by_email(body['username'])
        else:
            user = DATABASE.user_by_username(body['username'])

        if not user or not check_password(body['password'], user['password']):
            return g.auth_texts.get('invalid_username_password') + " " + g.auth_texts.get('no_account'), 403

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
        resp = make_response({})

        # We set the cookie to expire in a year, just so that the browser won't invalidate it if the same cookie gets renewed by constant use.
        # The server will decide whether the cookie expires.
        resp.set_cookie(TOKEN_COOKIE_NAME, value=cookie, httponly=True, secure=is_heroku(), samesite='Lax', path='/', max_age=365 * 24 * 60 * 60)

        # Remember the current user on the session. This is "new style" logins, which should ultimately
        # replace "old style" logins (with the cookie above), as it requires fewer database calls.
        remember_current_user(user)

        return resp

    @app.route('/auth/signup', methods=['POST'])
    def signup():
        body = request.json
        # Validations, mandatory fields
        if not isinstance(body, dict):
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return g.auth_texts.get('username_invalid'), 400
        if '@' in body['username'] or ':' in body['username']:
            return g.auth_texts.get('username_special'), 400
        if len(body['username'].strip()) < 3:
            return g.auth_texts.get('username_three'), 400
        if not isinstance(body.get('email'), str) or not valid_email(body['email']):
            return g.auth_texts.get('email_invalid'), 400
        if not isinstance(body.get('mail_repeat'), str) or not valid_email(body['mail_repeat']):
            return g.auth_texts.get('repeat_match_email'), 400
        if body['email'] != body['mail_repeat']:
            return g.auth_texts.get('repeat_match_email'), 400
        if not isinstance(body.get('password'), str):
            return g.auth_texts.get('password_invalid'), 400
        if len(body['password']) < 6:
            return g.auth_texts.get('password_six'), 400
        if not isinstance(body.get('password_repeat'), str) or body['password'] != body['password_repeat']:
            return g.auth_texts.get('repeat_match_password'), 400
        if not isinstance(body.get('language'), str):
            return g.auth_texts.get('language_invalid'), 400

        # Validations, optional fields
        if 'birth_year' in body:
            if not isinstance(body.get('birth_year'), int) or body['birth_year'] <= 1900 or body['birth_year'] > datetime.datetime.now().year:
                return (g.auth_texts.get('year_invalid') + str(datetime.datetime.now().year)), 400
        if 'gender' in body:
            if body['gender'] != 'm' and body['gender'] != 'f' and body['gender'] != 'o':
                return g.auth_texts.get('gender_invalid'), 400
        if 'country' in body:
            if not body['country'] in countries:
                return g.auth_texts.get('country_invalid'), 400
        if 'prog_experience' in body and body['prog_experience'] not in ['yes', 'no']:
            return g.auth_texts.get('experience_invalid'), 400
        if 'experience_languages' in body:
            if not isinstance(body['experience_languages'], list):
                return g.auth_texts.get('experience_invalid'), 400
            for language in body['experience_languages']:
                if language not in['scratch', 'other_block', 'python', 'other_text']:
                    return g.auth_texts.get('programming_invalid'), 400

        user = DATABASE.user_by_username(body['username'].strip().lower())
        if user:
            return g.auth_texts.get('exists_username'), 403
        email = DATABASE.user_by_email(body['email'].strip().lower())
        if email:
            return g.auth_texts.get('exists_email'), 403

        hashed = hash(body['password'], make_salt())

        token = make_salt()
        hashed_token = hash(token, make_salt())
        username = body['username'].strip().lower()
        email = body['email'].strip().lower()

        if not is_testing_request(request) and 'subscribe' in body and body['subscribe'] == True:
            # If we have a Mailchimp API key, we use it to add the subscriber through the API
            if MAILCHIMP_API_URL:
                mailchimp_subscribe_user(email)
            # Otherwise, we send an email to notify about the subscription to the main email address
            else:
                send_email(config['email']['sender'], 'Subscription to Hedy newsletter on signup', email, '<p>' + email + '</p>')

        if not is_testing_request(request) and 'is_teacher' in body and body['is_teacher'] is True:
            send_email(config['email']['sender'], 'Request for teacher\'s interface on signup', email, f'<p>{email}</p>')

        user = {
            'username': username,
            'password': hashed,
            'email':    email,
            'created':  timems(),
            'verification_pending': hashed_token,
            'last_login': timems()
        }

        for field in['country', 'birth_year', 'gender', 'language', 'prog_experience', 'experience_languages']:
           if field in body:
               if field == 'experience_languages' and len(body[field]) == 0:
                   continue
               user[field] = body[field]

        DATABASE.store_user(user)

        # We automatically login the user
        cookie = make_salt()
        DATABASE.store_token({'id': cookie, 'username': user['username'], 'ttl': times() + session_length})

        # If this is an e2e test, we return the email verification token directly instead of emailing it.
        if is_testing_request(request):
            resp = make_response({'username': username, 'token': hashed_token})
        # Otherwise, we send an email with a verification link and we return an empty body
        else:
            send_email_template('welcome_verify', email, email_base_url() + '/auth/verify?username=' + urllib.parse.quote_plus(username) + '&token=' + urllib.parse.quote_plus(hashed_token))
            resp = make_response({})

        # We set the cookie to expire in a year, just so that the browser won't invalidate it if the same cookie gets renewed by constant use.
        # The server will decide whether the cookie expires.
        resp.set_cookie(TOKEN_COOKIE_NAME, value=cookie, httponly=True, secure=is_heroku(), samesite='Lax', path='/', max_age=365 * 24 * 60 * 60)
        remember_current_user(user)

        return resp

    @app.route('/auth/verify', methods=['GET'])
    def verify_email():
        username = request.args.get('username', None)
        token = request.args.get('token', None)
        if not token:
            return 'no token', 400
        if not username:
            return 'no username', 400

        user = DATABASE.user_by_username(username)

        if not user:
            return 'invalid username/token', 403

        # If user is verified, succeed anyway
        if not 'verification_pending' in user:
            return redirect('/landing-page')

        if token != user['verification_pending']:
            return 'invalid username/token', 403

        DATABASE.update_user(username, {'verification_pending': None})
        return redirect('/')

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

    @app.route('/auth/change_password', methods=['POST'])
    @requires_login
    def change_password(user):
        body = request.json

        if not isinstance(body, dict):
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('old_password'), str) or not isinstance(body.get('password'), str):
            return g.auth_texts.get('password_invalid'), 400
        if not isinstance(body.get( 'password_repeat'), str):
            return g.auth_texts.get('repeat_match_password'), 400
        if len(body['password']) < 6:
            return g.auth_texts.get('password_six'), 400
        if body['password'] != body['password_repeat']:
            return g.auth_texts.get('repeat_match_password'), 400

        # The user object we got from 'requires_login' doesn't have the password, so look that up in the database
        user = DATABASE.user_by_username(user['username'])

        if not check_password(body['old_password'], user['password']):
            return g.auth_texts.get('password_invalid'), 403

        hashed = hash(body['password'], make_salt())

        DATABASE.update_user(user['username'], {'password': hashed})
        # We are not updating the user in the Flask session, because we should not rely on the password in anyway.
        if not is_testing_request(request):
            send_email_template('change_password', user['email'], None)

        return '', 200

    @app.route('/profile', methods=['POST'])
    @requires_login
    def update_profile(user):
        body = request.json
        if not isinstance(body, dict):
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('email'), str) or not valid_email(body['email']):
            return g.auth_texts.get('email_invalid'), 400
        if not isinstance(body.get('language'), str):
            return g.auth_texts.get('language_invalid'), 400

        # Validations, optional fields
        if 'birth_year' in body:
            if not isinstance(body.get('birth_year'), int) or body['birth_year'] <= 1900 or body['birth_year'] > datetime.datetime.now().year:
                return g.auth_texts.get('year_invalid') + str(datetime.datetime.now().year), 400
        if 'gender' in body:
            if body['gender'] != 'm' and body['gender'] != 'f' and body['gender'] != 'o':
                return g.auth_texts.get('gender_invalid'), 400
        if 'country' in body:
            if not body['country'] in countries:
                return g.auth_texts.get('country_invalid'), 400
        if 'prog_experience' in body and body['prog_experience'] not in ['yes', 'no']:
            return g.auth_texts.get('experience_invalid'), 400
        if 'experience_languages' in body:
            if not isinstance(body['experience_languages'], list):
                return g.auth_texts.get('experience_invalid'), 400
            for language in body['experience_languages']:
                if language not in['scratch', 'other_block', 'python', 'other_text']:
                    return g.auth_texts.get('programming_invalid'), 400

        resp = {}
        if 'email' in body:
            email = body['email'].strip().lower()
            if email != user['email']:
                exists = DATABASE.user_by_email(email)
                if exists:
                    return g.auth_texts.get('exists_email'), 403
                token = make_salt()
                hashed_token = hash(token, make_salt())
                DATABASE.update_user(user['username'], {'email': email, 'verification_pending': hashed_token})
                # If this is an e2e test, we return the email verification token directly instead of emailing it.
                if is_testing_request(request):
                   resp = {'username': user['username'], 'token': hashed_token}
                else:
                    send_email_template('welcome_verify', email, email_base_url() + '/auth/verify?username=' + urllib.parse.quote_plus(user['username']) + '&token=' + urllib.parse.quote_plus(hashed_token))

                # We check whether the user is in the Mailchimp list.
                if not is_testing_request(request) and MAILCHIMP_API_URL:
                    # We hash the email with md5 to avoid emails with unescaped characters triggering errors
                    request_path = MAILCHIMP_API_URL + '/members/' + hashlib.md5(user['email'].encode('utf-8')).hexdigest()
                    r = requests.get(request_path, headers=MAILCHIMP_API_HEADERS)
                    # If user is subscribed, we remove the old email from the list and add the new one
                    if r.status_code == 200:
                        r = requests.delete(request_path, headers=MAILCHIMP_API_HEADERS)
                        mailchimp_subscribe_user(email)

        username = user['username']

        updates = {}
        for field in['country', 'birth_year', 'gender', 'language', 'prog_experience', 'experience_languages']:
           if field in body:
               if field == 'experience_languages' and len(body[field]) == 0:
                   updates[field] = None
               else:
                   updates[field] = body[field]
           else:
               updates[field] = None

        if updates:
            DATABASE.update_user(username, updates)
        remember_current_user(DATABASE.user_by_username(user['username']))
        return jsonify(resp)

    @app.route('/profile', methods=['GET'])
    @requires_login
    def get_profile(user):
        # The user object we got from 'requires_login' is not fully hydrated yet. Look up the database user.
        user = DATABASE.user_by_username(user['username'])

        output = {'username': user['username'], 'email': user['email']}
        for field in['birth_year', 'country', 'gender', 'prog_experience', 'experience_languages']:
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
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return g.auth_texts.get('username_invalid'), 400

        # If username has an @-sign, then it's an email
        if '@' in body['username']:
            user = DATABASE.user_by_email(body['username'].strip().lower())
        else:
            user = DATABASE.user_by_username(body['username'].strip().lower())

        if not user:
            return g.auth_texts.get('username_invalid'), 403

        token = make_salt()
        hashed = hash(token, make_salt())

        DATABASE.store_token({'id': user['username'], 'token': hashed, 'ttl': times() + session_length})

        if is_testing_request(request):
            # If this is an e2e test, we return the email verification token directly instead of emailing it.
            return jsonify({'username': user['username'], 'token': token}), 200
        else:
            send_email_template('recover_password', user['email'], email_base_url() + '/reset?username=' + urllib.parse.quote_plus(user['username']) + '&token=' + urllib.parse.quote_plus(token))
            return '', 200

    @app.route('/auth/reset', methods=['POST'])
    def reset():
        body = request.json
        # Validations
        if not isinstance(body, dict):
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return g.auth_texts.get('username_invalid'), 400
        if not isinstance(body.get('token'), str):
            return g.auth_texts.get('token_invalid'), 400
        if not isinstance(body.get('password'), str):
            return g.auth_texts.get('password_invalid'), 400
        if len(body['password']) < 6:
            return g.auth_texts.get('password_six'), 400
        if not isinstance(body.get('password_repeat'), str) or body['password'] != body['password_repeat']:
            return g.auth_texts.get('repeat_match_password'), 400

        # There's no need to trim or lowercase username, because it should come within a link prepared by the app itself and not inputted manually by the user.
        token = DATABASE.get_token(body['username'])
        if not token:
            return g.auth_texts.get('token_invalid'), 403
        if not check_password(body['token'], token['token']):
            return g.auth_texts.get('token_invalid'), 403

        hashed = hash(body['password'], make_salt())
        token = DATABASE.forget_token(body['username'])
        DATABASE.update_user(body['username'], {'password': hashed})
        user = DATABASE.user_by_username(body['username'])

        if not is_testing_request(request):
            send_email_template('reset_password', user['email'], None)

        return '', 200

    @app.route('/auth/public_profile', methods=['POST'])
    @requires_login
    def update_public_profile(user):
        body = request.json

        # Validations
        if not isinstance(body, dict):
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('image'), str):
            return g.auth_texts.get('image_invalid'), 400
        if not isinstance(body.get('personal_text'), str):
            return g.auth_texts.get('personal_text_invalid'), 400
        if 'favourite_program' in body and not isinstance(body.get('favourite_program'), str):
            return g.auth_texts.get('favourite_program_invalid'), 400

        DATABASE.update_public_profile(user['username'], body);
        return '', 200

    # *** ADMIN ROUTES ***

    @app.route('/admin/markAsTeacher', methods=['POST'])
    def mark_as_teacher():
        user = current_user()
        if not is_admin(user) and not is_testing_request(request):
            return 'unauthorized', 403

        body = request.json

        # Validations
        if not isinstance(body, dict):
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return g.auth_texts.get('username_invalid'), 400
        if not isinstance(body.get('is_teacher'), bool):
            return g.auth_texts.get('teacher_invalid'), 400

        user = DATABASE.user_by_username(body['username'].strip().lower())

        if not user:
            return g.auth_texts.get('username_invalid'), 400

        is_teacher_value = 1 if body['is_teacher'] else 0
        update_is_teacher(user, is_teacher_value)

        return '', 200

    @app.route('/admin/changeUserEmail', methods=['POST'])
    def change_user_email():
        user = current_user()
        if not is_admin(user):
            return 'unauthorized', 403

        body = request.json

        # Validations
        if not isinstance(body, dict):
            return g.auth_texts.get('ajax_error'), 400
        if not isinstance(body.get('username'), str):
            return g.auth_texts.get('username_invalid'), 400
        if not isinstance(body.get('email'), str) or not valid_email(body['email']):
            return g.auth_texts.get('email_invalid'), 400

        user = DATABASE.user_by_username(body['username'].strip().lower())

        if not user:
            return g.auth_texts.get('email_invalid'), 400

        token = make_salt()
        hashed_token = hash(token, make_salt())

        # We assume that this email is not in use by any other users. In other words, we trust the admin to enter a valid, not yet used email address.
        DATABASE.update_user(user['username'], {'email': body['email'], 'verification_pending': hashed_token})

        # If this is an e2e test, we return the email verification token directly instead of emailing it.
        if is_testing_request(request):
           resp = {'username': user['username'], 'token': hashed_token}
        else:
            send_email_template('welcome_verify', body['email'], email_base_url() + '/auth/verify?username=' + urllib.parse.quote_plus(user['username']) + '&token=' + urllib.parse.quote_plus(hashed_token))

        return '', 200


# Turn off verbose logs from boto/SES, thanks to https://github.com/boto/boto3/issues/521
import logging
for name in logging.Logger.manager.loggerDict.keys():
    if('boto' in name) or('urllib3' in name) or('s3transfer' in name) or('boto3' in name) or('botocore' in name) or('nose' in name):
        logging.getLogger(name).setLevel(logging.CRITICAL)

# https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
email_client = boto3.client('ses', region_name = config['email']['region'])

@querylog.timed
def send_email(recipient, subject, body_plain, body_html):
    try:
        result = email_client.send_email(
            Source = config['email']['sender'],
            Destination = {'ToAddresses':[recipient]},
            Message = {
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {'Data': body_plain, 'Charset': 'UTF-8'},
                    'Html': {'Data': body_html,  'Charset': 'UTF-8'},
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

def send_email_template(template, email, link):
    texts = EMAILS
    subject = texts['email_' + template + '_subject']
    body = texts['email_' + template + '_body'].split('\n')
    body =[texts['email_hello']] + body
    if link:
        body[len(body) - 1] = body[len(body ) - 1] + ' @@LINK@@'
    body = body + texts['email_goodbye'].split('\n')

    body_plain = '\n'.join(body)

    with open('templates/base_email.html', 'r', encoding='utf-8') as f:
        body_html = f.read()
    body_html += '<p>' + '</p><p>'.join(body) + '</p>'
    body_html += '</div>'
    if link:
        body_plain = body_plain.replace('@@LINK@@', 'Please copy and paste this link into a new tab: ' + link)
        body_html = body_html.replace('@@LINK@@', '<a href="' + link + '">Link</a>')

    send_email(email, subject, body_plain, body_html)

def auth_templates(page, page_title):
    if page == 'my-profile':
        programs = DATABASE.public_programs_for_user(current_user()['username'])
        public_profile_settings = DATABASE.get_public_profile_settings(current_user()['username'])
        return render_template('profile.html', page_title=page_title, programs=programs,
                               public_settings=public_profile_settings, current_page='my-profile')
    if page in['signup', 'login', 'recover', 'reset']:
        return render_template(page + '.html', page_title=page_title, is_teacher=False, current_page='login')


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
