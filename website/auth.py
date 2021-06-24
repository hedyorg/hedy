import os
import bcrypt
import re
import urllib
from flask import request, make_response, jsonify, redirect
from flask_helpers import render_template
from utils import type_check, object_check, timems, times, db_get, db_create, db_update, db_del, db_del_many, db_scan, db_describe, db_get_many, extract_bcrypt_rounds, is_testing_request, is_debug_mode, valid_email
import datetime
from functools import wraps
from config import config
import boto3
from botocore.exceptions import ClientError as email_error
import json
import requests
from website import querylog

cookie_name     = config ['session'] ['cookie_name']
session_length  = config ['session'] ['session_length'] * 60

env = os.getenv ('HEROKU_APP_NAME')

@querylog.timed
def check_password (password, hash):
    return bcrypt.checkpw (bytes (password, 'utf-8'), bytes (hash, 'utf-8'))

def make_salt ():
    return bcrypt.gensalt (rounds=config ['bcrypt_rounds']).decode ('utf-8')

@querylog.timed
def hash (password, salt):
    return bcrypt.hashpw (bytes (password, 'utf-8'), bytes (salt, 'utf-8')).decode ('utf-8')

countries = {'AF':'Afghanistan','AX':'Åland Islands','AL':'Albania','DZ':'Algeria','AS':'American Samoa','AD':'Andorra','AO':'Angola','AI':'Anguilla','AQ':'Antarctica','AG':'Antigua and Barbuda','AR':'Argentina','AM':'Armenia','AW':'Aruba','AU':'Australia','AT':'Austria','AZ':'Azerbaijan','BS':'Bahamas','BH':'Bahrain','BD':'Bangladesh','BB':'Barbados','BY':'Belarus','BE':'Belgium','BZ':'Belize','BJ':'Benin','BM':'Bermuda','BT':'Bhutan','BO':'Bolivia, Plurinational State of','BQ':'Bonaire, Sint Eustatius and Saba','BA':'Bosnia and Herzegovina','BW':'Botswana','BV':'Bouvet Island','BR':'Brazil','IO':'British Indian Ocean Territory','BN':'Brunei Darussalam','BG':'Bulgaria','BF':'Burkina Faso','BI':'Burundi','KH':'Cambodia','CM':'Cameroon','CA':'Canada','CV':'Cape Verde','KY':'Cayman Islands','CF':'Central African Republic','TD':'Chad','CL':'Chile','CN':'China','CX':'Christmas Island','CC':'Cocos (Keeling) Islands','CO':'Colombia','KM':'Comoros','CG':'Congo','CD':'Congo, the Democratic Republic of the','CK':'Cook Islands','CR':'Costa Rica','CI':'Côte d\'Ivoire','HR':'Croatia','CU':'Cuba','CW':'Curaçao','CY':'Cyprus','CZ':'Czech Republic','DK':'Denmark','DJ':'Djibouti','DM':'Dominica','DO':'Dominican Republic','EC':'Ecuador','EG':'Egypt','SV':'El Salvador','GQ':'Equatorial Guinea','ER':'Eritrea','EE':'Estonia','ET':'Ethiopia','FK':'Falkland Islands (Malvinas)','FO':'Faroe Islands','FJ':'Fiji','FI':'Finland','FR':'France','GF':'French Guiana','PF':'French Polynesia','TF':'French Southern Territories','GA':'Gabon','GM':'Gambia','GE':'Georgia','DE':'Germany','GH':'Ghana','GI':'Gibraltar','GR':'Greece','GL':'Greenland','GD':'Grenada','GP':'Guadeloupe','GU':'Guam','GT':'Guatemala','GG':'Guernsey','GN':'Guinea','GW':'Guinea-Bissau','GY':'Guyana','HT':'Haiti','HM':'Heard Island and McDonald Islands','VA':'Holy See (Vatican City State)','HN':'Honduras','HK':'Hong Kong','HU':'Hungary','IS':'Iceland','IN':'India','ID':'Indonesia','IR':'Iran, Islamic Republic of','IQ':'Iraq','IE':'Ireland','IM':'Isle of Man','IL':'Israel','IT':'Italy','JM':'Jamaica','JP':'Japan','JE':'Jersey','JO':'Jordan','KZ':'Kazakhstan','KE':'Kenya','KI':'Kiribati','KP':'Korea, Democratic People\'s Republic of','KR':'Korea, Republic of','KW':'Kuwait','KG':'Kyrgyzstan','LA':'Lao People\'s Democratic Republic','LV':'Latvia','LB':'Lebanon','LS':'Lesotho','LR':'Liberia','LY':'Libya','LI':'Liechtenstein','LT':'Lithuania','LU':'Luxembourg','MO':'Macao','MK':'Macedonia, the Former Yugoslav Republic of','MG':'Madagascar','MW':'Malawi','MY':'Malaysia','MV':'Maldives','ML':'Mali','MT':'Malta','MH':'Marshall Islands','MQ':'Martinique','MR':'Mauritania','MU':'Mauritius','YT':'Mayotte','MX':'Mexico','FM':'Micronesia, Federated States of','MD':'Moldova, Republic of','MC':'Monaco','MN':'Mongolia','ME':'Montenegro','MS':'Montserrat','MA':'Morocco','MZ':'Mozambique','MM':'Myanmar','NA':'Namibia','NR':'Nauru','NP':'Nepal','NL':'Netherlands','NC':'New Caledonia','NZ':'New Zealand','NI':'Nicaragua','NE':'Niger','NG':'Nigeria','NU':'Niue','NF':'Norfolk Island','MP':'Northern Mariana Islands','NO':'Norway','OM':'Oman','PK':'Pakistan','PW':'Palau','PS':'Palestine, State of','PA':'Panama','PG':'Papua New Guinea','PY':'Paraguay','PE':'Peru','PH':'Philippines','PN':'Pitcairn','PL':'Poland','PT':'Portugal','PR':'Puerto Rico','QA':'Qatar','RE':'Réunion','RO':'Romania','RU':'Russian Federation','RW':'Rwanda','BL':'Saint Barthélemy','SH':'Saint Helena, Ascension and Tristan da Cunha','KN':'Saint Kitts and Nevis','LC':'Saint Lucia','MF':'Saint Martin (French part)','PM':'Saint Pierre and Miquelon','VC':'Saint Vincent and the Grenadines','WS':'Samoa','SM':'San Marino','ST':'Sao Tome and Principe','SA':'Saudi Arabia','SN':'Senegal','RS':'Serbia','SC':'Seychelles','SL':'Sierra Leone','SG':'Singapore','SX':'Sint Maarten (Dutch part)','SK':'Slovakia','SI':'Slovenia','SB':'Solomon Islands','SO':'Somalia','ZA':'South Africa','GS':'South Georgia and the South Sandwich Islands','SS':'South Sudan','ES':'Spain','LK':'Sri Lanka','SD':'Sudan','SR':'Suriname','SJ':'Svalbard and Jan Mayen','SZ':'Swaziland','SE':'Sweden','CH':'Switzerland','SY':'Syrian Arab Republic','TW':'Taiwan, Province of China','TJ':'Tajikistan','TZ':'Tanzania, United Republic of','TH':'Thailand','TL':'Timor-Leste','TG':'Togo','TK':'Tokelau','TO':'Tonga','TT':'Trinidad and Tobago','TN':'Tunisia','TR':'Turkey','TM':'Turkmenistan','TC':'Turks and Caicos Islands','TV':'Tuvalu','UG':'Uganda','UA':'Ukraine','AE':'United Arab Emirates','GB':'United Kingdom','US':'United States','UM':'United States Minor Outlying Islands','UY':'Uruguay','UZ':'Uzbekistan','VU':'Vanuatu','VE':'Venezuela, Bolivarian Republic of','VN':'Viet Nam','VG':'Virgin Islands, British','VI':'Virgin Islands, U.S.','WF':'Wallis and Futuna','EH':'Western Sahara','YE':'Yemen','ZM':'Zambia','ZW':'Zimbabwe'};

@querylog.timed
def current_user (request):
    if request.cookies.get (cookie_name):
        token = db_get ('tokens', {'id': request.cookies.get (cookie_name)})
        if token:
            user = db_get ('users',  {'username': token ['username']})
            if user:
                return user
    return {'username': '', 'email': ''}

def is_admin (request):
    user = current_user (request)
    return user ['username'] == os.getenv ('ADMIN_USER') or user ['email'] == os.getenv ('ADMIN_USER')

def is_teacher (request):
    user = current_user (request)
    return bool ('is_teacher' in user and user ['is_teacher'])

# The translations are imported here because current_user above is used by hedyweb.py and we need to avoid circular dependencies
import hedyweb
TRANSLATIONS = hedyweb.Translations ()

# Thanks to https://stackoverflow.com/a/34499643
def requires_login (f):
    @wraps (f)
    def inner (*args, **kws):
        User = None
        if request.cookies.get (cookie_name):
            token = db_get ('tokens', {'id': request.cookies.get (cookie_name)})
            if not token:
                return 'unauthorized', 403
            user = db_get ('users', {'username': token ['username']})
            if not user:
                return 'unauthorized', 403
        else:
            return 'unauthorized', 403

        return f (user, *args, **kws)
    return inner

# Note: translations are used only for texts that will be seen by a GUI user.
def routes (app, requested_lang):

    @app.route('/auth/texts', methods=['GET'])
    def auth_texts():
        response = make_response(jsonify(TRANSLATIONS.data [requested_lang ()] ['Auth']))
        if not is_debug_mode():
            # Cache for longer when not devving
            response.cache_control.max_age = 60 * 60  # Seconds
        return response

    @app.route ('/auth/login', methods=['POST'])
    def login ():
        body = request.json
        # Validations
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'username must be a string', 400
        if not object_check (body, 'password', 'str'):
            return 'password must be a string', 400

        # If username has an @-sign, then it's an email
        if '@' in body ['username']:
            user = db_get ('users', {'email': body ['username'].strip ().lower ()}, True)
        else:
            user = db_get ('users', {'username': body ['username'].strip ().lower ()})

        if not user:
            return 'invalid username/password', 403
        if not check_password (body ['password'], user ['password']):
            return 'invalid username/password', 403

        # If the number of bcrypt rounds has changed, create a new hash.
        new_hash = None
        if config ['bcrypt_rounds'] != extract_bcrypt_rounds (user ['password']):
            new_hash = hash (body ['password'], make_salt ())

        cookie = make_salt ()
        db_create ('tokens', {'id': cookie, 'username': user ['username'], 'ttl': times () + session_length})
        if new_hash:
            db_update ('users', {'username': user ['username'], 'password': new_hash, 'last_login': timems ()})
        else:
            db_update ('users', {'username': user ['username'], 'last_login': timems ()})
        resp = make_response ({})
        # We set the cookie to expire in a year, just so that the browser won't invalidate it if the same cookie gets renewed by constant use.
        # The server will decide whether the cookie expires.
        resp.set_cookie (cookie_name, value=cookie, httponly=True, secure=True, samesite='Lax', path='/', max_age=365 * 24 * 60 * 60)
        return resp

    @app.route ('/auth/signup', methods=['POST'])
    def signup ():
        body = request.json
        # Validations, mandatory fields
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'username must be a string', 400
        if '@' in body ['username']:
            return 'username cannot contain an @-sign', 400
        if ':' in body ['username']:
            return 'username cannot contain a colon', 400
        if len (body ['username'].strip ()) < 3:
            return 'username must be at least three characters long', 400
        if not object_check (body, 'password', 'str'):
            return 'password must be a string', 400
        if len (body ['password']) < 6:
            return 'password must be at least six characters long', 400
        if not object_check (body, 'email', 'str'):
            return 'email must be a string', 400
        if not valid_email (body ['email']):
            return 'email must be a valid email', 400
        # Validations, optional fields
        if 'country' in body:
            if not body ['country'] in countries:
                return 'country must be a valid country', 400
        if 'birth_year' in body:
            if not object_check (body, 'birth_year', 'int') or body ['birth_year'] <= 1900 or body ['birth_year'] > datetime.datetime.now ().year:
                return 'birth_year must be a year between 1900 and ' + datetime.datetime.now ().year, 400
        if 'gender' in body:
            if body ['gender'] != 'm' and body ['gender'] != 'f' and body ['gender'] != 'o':
                return 'gender must be m/f/o', 400

        user = db_get ('users', {'username': body ['username'].strip ().lower ()})
        if user:
            return 'username exists', 403
        email = db_get ('users', {'email': body ['email'].strip ().lower ()}, True)
        if email:
            return 'email exists', 403

        hashed = hash (body ['password'], make_salt ())

        token = make_salt ()
        hashed_token = hash (token, make_salt ())
        username = body ['username'].strip ().lower ()
        email = body ['email'].strip ().lower ()

        if not is_testing_request (request) and 'subscribe' in body and body ['subscribe'] == True:
            # If we have a Mailchimp API key, we use it to add the subscriber through the API
            if os.getenv ('MAILCHIMP_API_KEY') and os.getenv ('MAILCHIMP_AUDIENCE_ID'):
                # The first domain in the path is the server name, which is contained in the Mailchimp API key
                request_path = 'https://' + os.getenv ('MAILCHIMP_API_KEY').split ('-') [1] + '.api.mailchimp.com/3.0/lists/' + os.getenv ('MAILCHIMP_AUDIENCE_ID') + '/members'
                request_headers = {'Content-Type': 'application/json', 'Authorization': 'apikey ' + os.getenv ('MAILCHIMP_API_KEY')}
                request_body = {'email_address': email, 'status': 'subscribed'}
                r = requests.post (request_path, headers=request_headers, data=json.dumps (request_body))

                subscription_error = None
                if r.status_code != 200 and r.status_code != 400:
                   subscription_error = True
                # We can get a 400 if the email is already subscribed to the list. We should ignore this error.
                if r.status_code == 400 and not re.match ('.*already a list member', r.text):
                   subscription_error = True
                # If there's an error in subscription through the API, we report it to the main email address
                if subscription_error:
                    send_email (config ['email'] ['sender'], 'ERROR - Subscription to Hedy newsletter on signup', email, '<p>' + email + '</p><pre>Status:' + str (r.status_code) + '    Body:' + r.text + '</pre>')
            # Otherwise, we send an email to notify about this to the main email address
            else:
                send_email (config ['email'] ['sender'], 'Subscription to Hedy newsletter on signup', email, '<p>' + email + '</p>')

        user = {
            'username': username,
            'password': hashed,
            'email':    email,
            'created':  timems (),
            'verification_pending': hashed_token,
            'last_login': timems ()
        }

        if 'country' in body:
            user ['country'] = body ['country']
        if 'birth_year' in body:
            user ['birth_year'] = body ['birth_year']
        if 'gender' in body:
            user ['gender'] = body ['gender']

        db_create ('users', user)

        # We automatically login the user
        cookie = make_salt ()
        db_create ('tokens', {'id': cookie, 'username': user ['username'], 'ttl': times () + session_length})

        # If this is an e2e test, we return the email verification token directly instead of emailing it.
        if is_testing_request (request):
            resp = make_response ({'username': username, 'token': hashed_token})
        # Otherwise, we send an email with a verification link and we return an empty body
        else:
            send_email_template ('welcome_verify', email, requested_lang (), os.getenv ('BASE_URL') + '/auth/verify?username=' + urllib.parse.quote_plus (username) + '&token=' + urllib.parse.quote_plus (hashed_token))
            resp = make_response ({})

        # We set the cookie to expire in a year, just so that the browser won't invalidate it if the same cookie gets renewed by constant use.
        # The server will decide whether the cookie expires.
        resp.set_cookie (cookie_name, value=cookie, httponly=True, secure=True, samesite='Lax', path='/', max_age=365 * 24 * 60 * 60)
        return resp

    @app.route ('/auth/verify', methods=['GET'])
    def verify_email ():
        username = request.args.get ('username', None)
        token = request.args.get ('token', None)
        if not token:
            return 'no token', 400
        if not username:
            return 'no username', 400

        user = db_get ('users', {'username': username})

        if not user:
            return 'invalid username/token', 403

        # If user is verified, succeed anyway
        if not 'verification_pending' in user:
            return redirect ('/')

        if token != user ['verification_pending']:
            return 'invalid username/token', 403

        db_update ('users', {'username': username, 'verification_pending': None})
        return redirect ('/')

    @app.route ('/auth/logout', methods=['POST'])
    def logout ():
        if request.cookies.get (cookie_name):
            db_del ('tokens', {'id': request.cookies.get (cookie_name)})
        return '', 200

    @app.route ('/auth/destroy', methods=['POST'])
    @requires_login
    def destroy (user):
        db_del ('tokens', {'id': request.cookies.get (cookie_name)})
        db_del ('users', {'username': user ['username']})
        # The recover password token may exist, so we delete it
        db_del ('tokens', {'id': user ['username']})
        db_del_many ('programs', {'username': user ['username']}, True)
        return '', 200

    @app.route ('/auth/change_password', methods=['POST'])
    @requires_login
    def change_password (user):

        body = request.json
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'old_password', 'str'):
            return 'body.old_password must be a string', 400
        if not object_check (body, 'new_password', 'str'):
            return 'body.new_password must be a string', 400

        if len (body ['new_password']) < 6:
            return 'password must be at least six characters long', 400

        if not check_password (body ['old_password'], user ['password']):
            return 'invalid username/password', 403

        hashed = hash (body ['new_password'], make_salt ())

        db_update ('users', {'username': user ['username'], 'password': hashed})
        if not is_testing_request (request):
            send_email_template ('change_password', user ['email'], requested_lang (), None)

        return '', 200

    @app.route ('/profile', methods=['POST'])
    @requires_login
    def update_profile (user):

        body = request.json
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if 'email' in body:
            if not object_check (body, 'email', 'str'):
                return 'body.email must be a string', 400
            if not valid_email (body ['email']):
                return 'body.email must be a valid email', 400
        if 'country' in body:
            if not body ['country'] in countries:
                return 'body.country must be a valid country', 400
        if 'birth_year' in body:
            if not object_check (body, 'birth_year', 'int') or body ['birth_year'] <= 1900 or body ['birth_year'] > datetime.datetime.now ().year:
                return 'birth_year must be a year between 1900 and ' + str (datetime.datetime.now ().year), 400
        if 'gender' in body:
            if body ['gender'] != 'm' and body ['gender'] != 'f' and body ['gender'] != 'o':
                return 'body.gender must be m/f/o', 400

        resp = {}
        if 'email' in body:
            email = body ['email'].strip ().lower ()
            if email != user ['email']:
                exists = db_get ('users', {'email': email}, True)
                if exists:
                    return 'email exists', 403
                token = make_salt ()
                hashed_token = hash (token, make_salt ())
                db_update ('users', {'username': user ['username'], 'email': email, 'verification_pending': hashed_token})
                # If this is an e2e test, we return the email verification token directly instead of emailing it.
                if is_testing_request (request):
                   resp = {'username': user ['username'], 'token': hashed_token}
                else:
                    send_email_template ('welcome_verify', email, requested_lang (), os.getenv ('BASE_URL') + '/auth/verify?username=' + urllib.parse.quote_plus (user['username']) + '&token=' + urllib.parse.quote_plus (hashed_token))

        if 'country' in body:
            db_update ('users', {'username': user ['username'], 'country': body ['country']})
        if 'birth_year' in body:
            db_update ('users', {'username': user ['username'], 'birth_year': body ['birth_year']})
        if 'gender' in body:
            db_update ('users', {'username': user ['username'], 'gender': body ['gender']})

        return jsonify (resp)

    @app.route ('/profile', methods=['GET'])
    @requires_login
    def get_profile (user):
        output = {'username': user ['username'], 'email': user ['email']}
        if 'birth_year' in user:
            output ['birth_year'] = user ['birth_year']
        if 'country' in user:
            output ['country'] = user ['country']
        if 'gender' in user:
            output ['gender'] = user ['gender']
        if 'verification_pending' in user:
            output ['verification_pending'] = True
        output ['session_expires_at'] = timems () + session_length * 1000

        return jsonify (output), 200

    @app.route ('/auth/recover', methods=['POST'])
    def recover ():
        body = request.json
        # Validations
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'body.username must be a string', 400

        # If username has an @-sign, then it's an email
        if '@' in body ['username']:
            user = db_get ('users', {'email': body ['username'].strip ().lower ()}, True)
        else:
            user = db_get ('users', {'username': body ['username'].strip ().lower ()})

        if not user:
            return 'invalid username', 403

        token = make_salt ()
        hashed = hash (token, make_salt ())

        db_create ('tokens', {'id': user ['username'], 'token': hashed, 'ttl': times () + session_length})

        if is_testing_request (request):
            # If this is an e2e test, we return the email verification token directly instead of emailing it.
            return jsonify ({'username': user ['username'], 'token': token}), 200
        else:
            send_email_template ('recover_password', user ['email'], requested_lang (), os.getenv ('BASE_URL') + '/reset?username=' + urllib.parse.quote_plus (user ['username']) + '&token=' + urllib.parse.quote_plus (token))
            return '', 200

    @app.route ('/auth/reset', methods=['POST'])
    def reset ():
        body = request.json
        # Validations
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'body.username must be a string', 400
        if not object_check (body, 'token', 'str'):
            return 'body.token must be a string', 400
        if not object_check (body, 'password', 'str'):
            return 'body.password be a string', 400

        if len (body ['password']) < 6:
            return 'password must be at least six characters long', 400

        # There's no need to trim or lowercase username, because it should come within a link prepared by the app itself and not inputted manually by the user.
        token = db_get ('tokens', {'id': body ['username']})
        if not token:
            return 'invalid username/token', 403
        if not check_password (body ['token'], token ['token']):
            return 'invalid username/token', 403

        hashed = hash (body ['password'], make_salt ())
        token = db_del ('tokens', {'id': body ['username']})
        db_update ('users', {'username': body ['username'], 'password': hashed})
        user = db_get ('users', {'username': body ['username']})

        if not is_testing_request (request):
            send_email_template ('reset_password', user ['email'], requested_lang (), None)

        return '', 200

    # *** ADMIN ROUTES ***

    @app.route ('/admin/markAsTeacher', methods=['POST'])
    def mark_as_teacher ():
        if not is_admin (request):
            return 'unauthorized', 403

        body = request.json

        # Validations
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'body.username must be a string', 400
        if not object_check (body, 'is_teacher', 'bool'):
            return 'body.is_teacher must be boolean', 400

        user = db_get ('users', {'username': body ['username'].strip ().lower ()})

        if not user:
            return 'invalid username', 400

        db_update ('users', {'username': user ['username'], 'is_teacher': 1 if body ['is_teacher'] else 0})

        return '', 200

    @app.route ('/admin/changeUserEmail', methods=['POST'])
    def change_user_email():
        if not is_admin (request):
            return 'unauthorized', 403

        body = request.json

        # Validations
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'body.username must be a string', 400
        if not object_check (body, 'email', 'str'):
            return 'body.email must be a string', 400
        if not valid_email (body ['email']):
            return 'email must be a valid email', 400

        user = db_get ('users', {'username': body ['username'].strip ().lower ()})

        if not user:
            return 'invalid username', 400

        token = make_salt ()
        hashed_token = hash (token, make_salt ())

        # We assume that this email is not in use by any other users. In other words, we trust the admin to enter a valid, not yet used email address.
        db_update ('users', {'username': user ['username'], 'email': body ['email'], 'verification_pending': hashed_token})

        # If this is an e2e test, we return the email verification token directly instead of emailing it.
        if is_testing_request (request):
           resp = {'username': user ['username'], 'token': hashed_token}
        else:
            send_email_template ('welcome_verify', body ['email'], requested_lang (), os.getenv ('BASE_URL') + '/auth/verify?username=' + urllib.parse.quote_plus (user ['username']) + '&token=' + urllib.parse.quote_plus (hashed_token))

        return '', 200


# Turn off verbose logs from boto/SES, thanks to https://github.com/boto/boto3/issues/521
import logging
for name in logging.Logger.manager.loggerDict.keys ():
    if ('boto' in name) or ('urllib3' in name) or ('s3transfer' in name) or ('boto3' in name) or ('botocore' in name) or ('nose' in name):
        logging.getLogger (name).setLevel (logging.CRITICAL)

# https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
email_client = boto3.client ('ses', region_name = config ['email'] ['region'], aws_access_key_id = os.getenv ('AWS_SES_ACCESS_KEY'), aws_secret_access_key = os.getenv ('AWS_SES_SECRET_KEY'))

@querylog.timed
def send_email (recipient, subject, body_plain, body_html):
    try:
        result = email_client.send_email (
            Source = config ['email'] ['sender'],
            Destination = {'ToAddresses': [recipient]},
            Message = {
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {'Data': body_plain, 'Charset': 'UTF-8'},
                    'Html': {'Data': body_html,  'Charset': 'UTF-8'},
                }
            }
        )
    except email_error as error:
        print ('Email send error', error.response ['Error'] ['Message'])
    else:
        print ('Email sent to ' + recipient)

def send_email_template (template, email, lang, link):
    texts = TRANSLATIONS.data [lang] ['Auth']
    subject = texts ['email_' + template + '_subject']
    body = texts ['email_' + template + '_body'].split ('\n')
    body = [texts ['email_hello']] + body
    if link:
        body [len (body) - 1] = body [len (body ) - 1] + ' @@LINK@@'
    body = body + texts ['email_goodbye'].split ('\n')

    body_plain = '\n'.join (body)
    body_html = '<p>' + '</p><p>'.join (body) + '</p>'
    if link:
        body_plain = body_plain.replace ('@@LINK@@', 'Please copy and paste this link into a new tab: ' + link)
        body_html = body_html.replace ('@@LINK@@', '<a href="' + link + '">Link</a>')
    body_html += '<br><img style="max-width: 100px" src="http://www.hedycode.com/images/Hedy-logo.png">'

    send_email (email, subject, body_plain, body_html)

def auth_templates (page, lang, menu, request):
    if page == 'my-profile':
        return render_template ('profile.html', lang=lang, auth=TRANSLATIONS.data [lang] ['Auth'], menu=menu, username=current_user (request) ['username'], current_page='my-profile')
    if page in ['signup', 'login', 'recover', 'reset']:
        return render_template (page + '.html',  lang=lang, auth=TRANSLATIONS.data [lang] ['Auth'], menu=menu, username=current_user (request) ['username'], current_page='login')
    if page == 'admin':
        if not is_admin (request):
            return 'unauthorized', 403

        # After hitting 1k users, it'd be wise to add pagination.
        users = db_scan ('users')
        userdata = []
        fields = ['username', 'email', 'birth_year', 'country', 'gender', 'created', 'last_login', 'verification_pending', 'is_teacher', 'program_count']

        for user in users:
            data = {}
            for field in fields:
                if field in user:
                    data [field] = user [field]
                else:
                    data [field] = None
            data ['email_verified'] = not bool (data ['verification_pending'])
            data ['is_teacher']     = bool (data ['is_teacher'])
            data ['created'] = datetime.datetime.fromtimestamp (int (str (data ['created']) [:-3])).isoformat ()
            if data ['last_login']:
                data ['last_login'] = datetime.datetime.fromtimestamp (int (str (data ['last_login']) [:-3])).isoformat ()
            userdata.append (data)

        userdata.sort(key=lambda user: user ['created'], reverse=True)
        counter = 1
        for user in userdata:
            user ['index'] = counter
            counter = counter + 1

        return render_template ('admin.html', users=userdata, program_count=db_describe ('programs') ['Table'] ['ItemCount'], user_count=db_describe ('users') ['Table'] ['ItemCount'])
