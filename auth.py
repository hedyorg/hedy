import os
import bcrypt
import redis
import re
import urllib
from flask import request, make_response, jsonify, redirect, render_template
from utils import type_check, object_check, timems
import datetime
from functools import wraps
from config import config
import boto3
from botocore.exceptions import ClientError as email_error

import hedyweb
TRANSLATIONS = hedyweb.Translations()

# We set decode_responses to true to get strings instead of binary strings
r = redis.Redis (host=config ['redis'] ['host'], port=config ['redis'] ['port'], db= config ['redis'] ['db'], decode_responses=True)

cookie_name     = config ['session'] ['cookie_name']
session_length  = config ['session'] ['session_length'] * 60

env = os.getenv ('HEROKU_APP_NAME')

def redis_keyscan (match, cursor, keys):
    if not cursor:
        cursor = 0
    if not keys:
        keys = {}
    scan = r.scan (cursor, match)
    for key in scan [1]:
        keys [key] = True
    if scan [0] == 0:
        return list (keys.keys ())
    return redis_keyscan (match, scan [0], keys)

def check_password (password, hash):
    return bcrypt.checkpw (bytes (password, 'utf-8'), bytes (hash, 'utf-8'))

def make_salt ():
    return bcrypt.gensalt ().decode ('utf-8')

def hash (password, salt):
    return bcrypt.hashpw (bytes (password, 'utf-8'), bytes (salt, 'utf-8')).decode ('utf-8')

countries = {'AF':'Afghanistan','AX':'Åland Islands','AL':'Albania','DZ':'Algeria','AS':'American Samoa','AD':'Andorra','AO':'Angola','AI':'Anguilla','AQ':'Antarctica','AG':'Antigua and Barbuda','AR':'Argentina','AM':'Armenia','AW':'Aruba','AU':'Australia','AT':'Austria','AZ':'Azerbaijan','BS':'Bahamas','BH':'Bahrain','BD':'Bangladesh','BB':'Barbados','BY':'Belarus','BE':'Belgium','BZ':'Belize','BJ':'Benin','BM':'Bermuda','BT':'Bhutan','BO':'Bolivia, Plurinational State of','BQ':'Bonaire, Sint Eustatius and Saba','BA':'Bosnia and Herzegovina','BW':'Botswana','BV':'Bouvet Island','BR':'Brazil','IO':'British Indian Ocean Territory','BN':'Brunei Darussalam','BG':'Bulgaria','BF':'Burkina Faso','BI':'Burundi','KH':'Cambodia','CM':'Cameroon','CA':'Canada','CV':'Cape Verde','KY':'Cayman Islands','CF':'Central African Republic','TD':'Chad','CL':'Chile','CN':'China','CX':'Christmas Island','CC':'Cocos (Keeling) Islands','CO':'Colombia','KM':'Comoros','CG':'Congo','CD':'Congo, the Democratic Republic of the','CK':'Cook Islands','CR':'Costa Rica','CI':'Côte d\'Ivoire','HR':'Croatia','CU':'Cuba','CW':'Curaçao','CY':'Cyprus','CZ':'Czech Republic','DK':'Denmark','DJ':'Djibouti','DM':'Dominica','DO':'Dominican Republic','EC':'Ecuador','EG':'Egypt','SV':'El Salvador','GQ':'Equatorial Guinea','ER':'Eritrea','EE':'Estonia','ET':'Ethiopia','FK':'Falkland Islands (Malvinas)','FO':'Faroe Islands','FJ':'Fiji','FI':'Finland','FR':'France','GF':'French Guiana','PF':'French Polynesia','TF':'French Southern Territories','GA':'Gabon','GM':'Gambia','GE':'Georgia','DE':'Germany','GH':'Ghana','GI':'Gibraltar','GR':'Greece','GL':'Greenland','GD':'Grenada','GP':'Guadeloupe','GU':'Guam','GT':'Guatemala','GG':'Guernsey','GN':'Guinea','GW':'Guinea-Bissau','GY':'Guyana','HT':'Haiti','HM':'Heard Island and McDonald Islands','VA':'Holy See (Vatican City State)','HN':'Honduras','HK':'Hong Kong','HU':'Hungary','IS':'Iceland','IN':'India','ID':'Indonesia','IR':'Iran, Islamic Republic of','IQ':'Iraq','IE':'Ireland','IM':'Isle of Man','IL':'Israel','IT':'Italy','JM':'Jamaica','JP':'Japan','JE':'Jersey','JO':'Jordan','KZ':'Kazakhstan','KE':'Kenya','KI':'Kiribati','KP':'Korea, Democratic People\'s Republic of','KR':'Korea, Republic of','KW':'Kuwait','KG':'Kyrgyzstan','LA':'Lao People\'s Democratic Republic','LV':'Latvia','LB':'Lebanon','LS':'Lesotho','LR':'Liberia','LY':'Libya','LI':'Liechtenstein','LT':'Lithuania','LU':'Luxembourg','MO':'Macao','MK':'Macedonia, the Former Yugoslav Republic of','MG':'Madagascar','MW':'Malawi','MY':'Malaysia','MV':'Maldives','ML':'Mali','MT':'Malta','MH':'Marshall Islands','MQ':'Martinique','MR':'Mauritania','MU':'Mauritius','YT':'Mayotte','MX':'Mexico','FM':'Micronesia, Federated States of','MD':'Moldova, Republic of','MC':'Monaco','MN':'Mongolia','ME':'Montenegro','MS':'Montserrat','MA':'Morocco','MZ':'Mozambique','MM':'Myanmar','NA':'Namibia','NR':'Nauru','NP':'Nepal','NL':'Netherlands','NC':'New Caledonia','NZ':'New Zealand','NI':'Nicaragua','NE':'Niger','NG':'Nigeria','NU':'Niue','NF':'Norfolk Island','MP':'Northern Mariana Islands','NO':'Norway','OM':'Oman','PK':'Pakistan','PW':'Palau','PS':'Palestine, State of','PA':'Panama','PG':'Papua New Guinea','PY':'Paraguay','PE':'Peru','PH':'Philippines','PN':'Pitcairn','PL':'Poland','PT':'Portugal','PR':'Puerto Rico','QA':'Qatar','RE':'Réunion','RO':'Romania','RU':'Russian Federation','RW':'Rwanda','BL':'Saint Barthélemy','SH':'Saint Helena, Ascension and Tristan da Cunha','KN':'Saint Kitts and Nevis','LC':'Saint Lucia','MF':'Saint Martin (French part)','PM':'Saint Pierre and Miquelon','VC':'Saint Vincent and the Grenadines','WS':'Samoa','SM':'San Marino','ST':'Sao Tome and Principe','SA':'Saudi Arabia','SN':'Senegal','RS':'Serbia','SC':'Seychelles','SL':'Sierra Leone','SG':'Singapore','SX':'Sint Maarten (Dutch part)','SK':'Slovakia','SI':'Slovenia','SB':'Solomon Islands','SO':'Somalia','ZA':'South Africa','GS':'South Georgia and the South Sandwich Islands','SS':'South Sudan','ES':'Spain','LK':'Sri Lanka','SD':'Sudan','SR':'Suriname','SJ':'Svalbard and Jan Mayen','SZ':'Swaziland','SE':'Sweden','CH':'Switzerland','SY':'Syrian Arab Republic','TW':'Taiwan, Province of China','TJ':'Tajikistan','TZ':'Tanzania, United Republic of','TH':'Thailand','TL':'Timor-Leste','TG':'Togo','TK':'Tokelau','TO':'Tonga','TT':'Trinidad and Tobago','TN':'Tunisia','TR':'Turkey','TM':'Turkmenistan','TC':'Turks and Caicos Islands','TV':'Tuvalu','UG':'Uganda','UA':'Ukraine','AE':'United Arab Emirates','GB':'United Kingdom','US':'United States','UM':'United States Minor Outlying Islands','UY':'Uruguay','UZ':'Uzbekistan','VU':'Vanuatu','VE':'Venezuela, Bolivarian Republic of','VN':'Viet Nam','VG':'Virgin Islands, British','VI':'Virgin Islands, U.S.','WF':'Wallis and Futuna','EH':'Western Sahara','YE':'Yemen','ZM':'Zambia','ZW':'Zimbabwe'};

def current_user (request):
    if request.cookies.get (cookie_name):
        username = r.get ('sess:' + request.cookies.get (cookie_name))
        if username:
            return username
    return ""

# Thanks to https://stackoverflow.com/a/34499643
def requires_login (f):
    @wraps (f)
    def inner (*args, **kws):
        User = None
        if request.cookies.get (cookie_name):
            username = r.get ('sess:' + request.cookies.get (cookie_name))
            if not username:
                return 'unauthorized', 403
            user = r.hgetall ('user:' + username)
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
        return jsonify (TRANSLATIONS.data [requested_lang ()] ['Auth'])

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
            username = r.hget ('email', body ['username'].strip ().lower ())
            if not username:
                return 'invalid username/password', 403
        else:
            username = body ['username'].strip ().lower ()

        user = r.hgetall ('user:' + username)
        if not user:
            return 'invalid username/password', 403
        if not check_password (body ['password'], user ['password']):
            return 'invalid username/password', 403

        cookie = make_salt ()
        r.setex ('sess:' + cookie, session_length, username)
        r.hset ('user:' + username, 'last_login', timems ())
        resp = make_response ({})
        resp.set_cookie (cookie_name, value=cookie, httponly=True, path='/')
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
        if not re.match ('^(([a-zA-Z0-9_\.\-]+)@([\da-zA-Z\.\-]+)\.([a-zA-Z\.]{2,6})\s*)$', body ['email']):
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

        user = r.hgetall ('user:' + body ['username'].strip ().lower ())
        if user:
            return 'username exists', 403
        email = r.hget ('email', body ['email'].strip ().lower ())
        if email:
            return 'email exists', 403

        hashed = hash (body ['password'], make_salt ())

        token = make_salt ()
        hashed_token = hash (token, make_salt ())
        username = body ['username'].strip ().lower ()
        email = body ['email'].strip ().lower ()

        if env and 'subscribe' in body and body ['subscribe'] == True:
            send_email (config ['email'] ['sender'], 'Subscription to Hedy newsletter on signup', email, '<p>' + email + '</p>')

        user = {
            'username': username,
            'password': hashed,
            'email':    email,
            'created':  timems (),
            'verification_pending': hashed_token
        }

        if 'country' in body:
            user ['country'] = body ['country']
        if 'birth_year' in body:
            user ['birth_year'] = body ['birth_year']
        if 'gender' in body:
            user ['gender'] = body ['gender']

        r.hmset ('user:' + username, user);
        r.hset ('email', email, username)

        if not env:
            # If on local environment, we return email verification token directly instead of emailing it, for test purposes.
            return jsonify ({'username': username, 'token': hashed_token}), 200
        else:
            send_email_template ('welcome_verify', email, requested_lang (), os.getenv ('BASE_URL') + '/auth/verify?username=' + urllib.parse.quote_plus (username) + '&token=' + urllib.parse.quote_plus (hashed_token))
            return '', 200

    @app.route ('/auth/verify', methods=['GET'])
    def verify_email ():
        username = request.args.get ('username', None)
        token = request.args.get ('token', None)
        if not token:
            return 'no token', 400
        if not username:
            return 'no username', 400

        user = r.hgetall ('user:' + username)

        if not user:
            return 'invalid username/token', 403

        # If user is verified, succeed anyway
        if not 'verification_pending' in user:
            return redirect ('/')

        if token != user ['verification_pending']:
            return 'invalid username/token', 403

        r.hdel ('user:' + username, 'verification_pending')
        return redirect ('/')

    @app.route ('/auth/logout', methods=['POST'])
    def logout ():
        if request.cookies.get (cookie_name):
            r.delete ('sess:' + request.cookies.get (cookie_name))
        return '', 200

    @app.route ('/auth/destroy', methods=['POST'])
    @requires_login
    def destroy (user):
        r.delete ('sess:' + request.cookies.get (cookie_name))
        r.delete ('user:' + user ['username'])
        # The recover password token may exist, so we delete it
        r.delete ('token:' + user ['username'])
        r.hdel ('email', user ['email'])
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

        r.hset ('user:' + user ['username'], 'password', hashed)
        if env:
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
            if not re.match ('^(([a-zA-Z0-9_\.\-]+)@([\da-zA-Z\.\-]+)\.([a-zA-Z\.]{2,6})\s*)$', body ['email']):
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

        if 'email' in body:
            email = body ['email'].strip ().lower ()
            if email != user ['email']:
                exists = r.hget ('email', email)
                if exists:
                    return 'email exists', 403
                r.hdel ('email', user ['email'])
                r.hset ('email', email, user ['username'])
                r.hset ('user:' + user ['username'], 'email', email)

        if 'country' in body:
            r.hset ('user:' + user ['username'], 'country', body ['country'])
        if 'birth_year' in body:
            r.hset ('user:' + user ['username'], 'birth_year', body ['birth_year'])
        if 'gender' in body:
            r.hset ('user:' + user ['username'], 'gender', body ['gender'])
        return '', 200

    @app.route ('/profile', methods=['GET'])
    @requires_login
    def get_profile (user):
        user = r.hmget ('user:' + user ['username'], 'username', 'email', 'birth_year', 'country', 'gender')
        output = {'username': user [0], 'email': user [1]}
        if user [2]:
            output ['birth_year'] = user [2]
        if user [3]:
            output ['country'] = user [3]
        if user [4]:
            output ['gender'] = user [4]

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
            username = r.hget ('email', body ['username'].strip ().lower ())
            if not username:
                return 'invalid username', 403
        else:
            username = body ['username'].strip ().lower ()

        user = r.hgetall ('user:' + username)

        if not user:
            return 'invalid username', 403

        token = make_salt ()
        hashed = hash (token, make_salt ())

        r.setex ('token:' + username, session_length, hashed)

        if not env:
            # If on local environment, we return email verification token directly instead of emailing it, for test purposes.
            return jsonify ({'username': username, 'token': token}), 200
        else:
            send_email_template ('recover_password', user ['email'], requested_lang (), os.getenv ('BASE_URL') + '/reset?username=' + urllib.parse.quote_plus (username) + '&token=' + urllib.parse.quote_plus (token))
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

        # If username has an @-sign, then it's an email
        if '@' in body ['username']:
            username = r.hget ('email', body ['username'].strip ().lower ())
            if not username:
                return 'invalid username/password', 403
        else:
            username = body ['username'].strip ().lower ()

        hashed = r.get ('token:' + username)
        if not hashed:
            return 'invalid username/token', 403
        if not check_password (body ['token'], hashed):
            return 'invalid username/token', 403

        hashed = hash (body ['password'], make_salt ())
        r.delete ('token:' + username);
        r.hset ('user:' + username, 'password', hashed)
        email = r.hget ('user:' + username, 'email')

        if env:
            send_email_template ('reset_password', email, requested_lang (), None)

        return '', 200

# Turn off verbose logs from boto/SES, thanks to https://github.com/boto/boto3/issues/521
import logging
for name in logging.Logger.manager.loggerDict.keys ():
    if ('boto' in name) or ('urllib3' in name) or ('s3transfer' in name) or ('boto3' in name) or ('botocore' in name) or ('nose' in name):
        logging.getLogger (name).setLevel (logging.CRITICAL)

# https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
email_client = boto3.client ('ses', region_name = config ['email'] ['region'], aws_access_key_id = os.getenv ('AWS_SES_ACCESS_KEY'), aws_secret_access_key = os.getenv ('AWS_SES_SECRET_KEY'))

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
        body = body + ['@@LINK@@']
    body = body + texts ['email_goodbye'].split ('\n')

    body_plain = '\n'.join (body)
    body_html = '<p>' + '</p><p>'.join (body) + '</p>'
    if link:
        body_plain = body_plain.replace ('@@LINK@@', 'Please copy and paste this link into a new tab: ' + link)
        body_html = body_html.replace ('@@LINK@@', '<a href="' + link + '">Link</a>')

    send_email (email, subject, body_plain, body_html)

def auth_templates (page, lang, menu, request):
    if page == 'my-profile':
        return render_template ('profile.html', lang=lang, auth=TRANSLATIONS.data [lang] ['Auth'], menu=menu, username=current_user (request))
    if page in ['signup', 'login', 'recover', 'reset']:
        return render_template (page + '.html',  lang=lang, auth=TRANSLATIONS.data [lang] ['Auth'], menu=menu, username=current_user (request))
    if page == 'users':
        user = current_user (request)
        if current_user (request) != os.getenv ('ADMIN_USER'):
            if r.hget ('user:' + user, 'email') != os.getenv ('ADMIN_USER'):
                return 'unauthorized', 403

        # After hitting 1k users, it'd be wise to add pagination.
        users = redis_keyscan ('user:*', None, None)
        userdata = []
        fields = ['username', 'email', 'birth_year', 'country', 'gender', 'created', 'last_login', 'verification_pending']
        counter = 1
        for user in users:
            rawdata = r.hmget (user, fields)
            data = {}
            for index, field in enumerate (fields):
                data [field] = rawdata [index]
            data ['email_verified'] = not bool (data ['verification_pending'])
            data ['created'] = datetime.datetime.fromtimestamp (int (data ['created'] [:-3])).isoformat ()
            if data ['last_login']:
                data ['last_login'] = datetime.datetime.fromtimestamp (int (data ['last_login'] [:-3])).isoformat ()
            data ['index'] = counter
            counter = counter + 1
            userdata.append (data)

        userdata.sort(key=lambda user: user ['created'], reverse=True)

        return render_template ('users.html', users=userdata)
