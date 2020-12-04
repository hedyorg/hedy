import bcrypt
import redis
import re
from flask import request, make_response, jsonify
from utils import type_check, object_check, timems
from functools import wraps
# TODO: set up config in config file
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def check_password(password, hash):
    return bcrypt.checkpw(bytes (password, 'utf-8'), bytes (hash, 'utf-8'))

def make_salt():
    return bcrypt.gensalt().decode ('utf-8')

def hash(password, salt):
    return bcrypt.hashpw(bytes (password, 'utf-8'), bytes (salt, 'utf-8')).decode('utf-8')

countries = {'AF':'Afghanistan','AX':'Åland Islands','AL':'Albania','DZ':'Algeria','AS':'American Samoa','AD':'Andorra','AO':'Angola','AI':'Anguilla','AQ':'Antarctica','AG':'Antigua and Barbuda','AR':'Argentina','AM':'Armenia','AW':'Aruba','AU':'Australia','AT':'Austria','AZ':'Azerbaijan','BS':'Bahamas','BH':'Bahrain','BD':'Bangladesh','BB':'Barbados','BY':'Belarus','BE':'Belgium','BZ':'Belize','BJ':'Benin','BM':'Bermuda','BT':'Bhutan','BO':'Bolivia, Plurinational State of','BQ':'Bonaire, Sint Eustatius and Saba','BA':'Bosnia and Herzegovina','BW':'Botswana','BV':'Bouvet Island','BR':'Brazil','IO':'British Indian Ocean Territory','BN':'Brunei Darussalam','BG':'Bulgaria','BF':'Burkina Faso','BI':'Burundi','KH':'Cambodia','CM':'Cameroon','CA':'Canada','CV':'Cape Verde','KY':'Cayman Islands','CF':'Central African Republic','TD':'Chad','CL':'Chile','CN':'China','CX':'Christmas Island','CC':'Cocos (Keeling) Islands','CO':'Colombia','KM':'Comoros','CG':'Congo','CD':'Congo, the Democratic Republic of the','CK':'Cook Islands','CR':'Costa Rica','CI':'Côte d\'Ivoire','HR':'Croatia','CU':'Cuba','CW':'Curaçao','CY':'Cyprus','CZ':'Czech Republic','DK':'Denmark','DJ':'Djibouti','DM':'Dominica','DO':'Dominican Republic','EC':'Ecuador','EG':'Egypt','SV':'El Salvador','GQ':'Equatorial Guinea','ER':'Eritrea','EE':'Estonia','ET':'Ethiopia','FK':'Falkland Islands (Malvinas)','FO':'Faroe Islands','FJ':'Fiji','FI':'Finland','FR':'France','GF':'French Guiana','PF':'French Polynesia','TF':'French Southern Territories','GA':'Gabon','GM':'Gambia','GE':'Georgia','DE':'Germany','GH':'Ghana','GI':'Gibraltar','GR':'Greece','GL':'Greenland','GD':'Grenada','GP':'Guadeloupe','GU':'Guam','GT':'Guatemala','GG':'Guernsey','GN':'Guinea','GW':'Guinea-Bissau','GY':'Guyana','HT':'Haiti','HM':'Heard Island and McDonald Islands','VA':'Holy See (Vatican City State)','HN':'Honduras','HK':'Hong Kong','HU':'Hungary','IS':'Iceland','IN':'India','ID':'Indonesia','IR':'Iran, Islamic Republic of','IQ':'Iraq','IE':'Ireland','IM':'Isle of Man','IL':'Israel','IT':'Italy','JM':'Jamaica','JP':'Japan','JE':'Jersey','JO':'Jordan','KZ':'Kazakhstan','KE':'Kenya','KI':'Kiribati','KP':'Korea, Democratic People\'s Republic of','KR':'Korea, Republic of','KW':'Kuwait','KG':'Kyrgyzstan','LA':'Lao People\'s Democratic Republic','LV':'Latvia','LB':'Lebanon','LS':'Lesotho','LR':'Liberia','LY':'Libya','LI':'Liechtenstein','LT':'Lithuania','LU':'Luxembourg','MO':'Macao','MK':'Macedonia, the Former Yugoslav Republic of','MG':'Madagascar','MW':'Malawi','MY':'Malaysia','MV':'Maldives','ML':'Mali','MT':'Malta','MH':'Marshall Islands','MQ':'Martinique','MR':'Mauritania','MU':'Mauritius','YT':'Mayotte','MX':'Mexico','FM':'Micronesia, Federated States of','MD':'Moldova, Republic of','MC':'Monaco','MN':'Mongolia','ME':'Montenegro','MS':'Montserrat','MA':'Morocco','MZ':'Mozambique','MM':'Myanmar','NA':'Namibia','NR':'Nauru','NP':'Nepal','NL':'Netherlands','NC':'New Caledonia','NZ':'New Zealand','NI':'Nicaragua','NE':'Niger','NG':'Nigeria','NU':'Niue','NF':'Norfolk Island','MP':'Northern Mariana Islands','NO':'Norway','OM':'Oman','PK':'Pakistan','PW':'Palau','PS':'Palestine, State of','PA':'Panama','PG':'Papua New Guinea','PY':'Paraguay','PE':'Peru','PH':'Philippines','PN':'Pitcairn','PL':'Poland','PT':'Portugal','PR':'Puerto Rico','QA':'Qatar','RE':'Réunion','RO':'Romania','RU':'Russian Federation','RW':'Rwanda','BL':'Saint Barthélemy','SH':'Saint Helena, Ascension and Tristan da Cunha','KN':'Saint Kitts and Nevis','LC':'Saint Lucia','MF':'Saint Martin (French part)','PM':'Saint Pierre and Miquelon','VC':'Saint Vincent and the Grenadines','WS':'Samoa','SM':'San Marino','ST':'Sao Tome and Principe','SA':'Saudi Arabia','SN':'Senegal','RS':'Serbia','SC':'Seychelles','SL':'Sierra Leone','SG':'Singapore','SX':'Sint Maarten (Dutch part)','SK':'Slovakia','SI':'Slovenia','SB':'Solomon Islands','SO':'Somalia','ZA':'South Africa','GS':'South Georgia and the South Sandwich Islands','SS':'South Sudan','ES':'Spain','LK':'Sri Lanka','SD':'Sudan','SR':'Suriname','SJ':'Svalbard and Jan Mayen','SZ':'Swaziland','SE':'Sweden','CH':'Switzerland','SY':'Syrian Arab Republic','TW':'Taiwan, Province of China','TJ':'Tajikistan','TZ':'Tanzania, United Republic of','TH':'Thailand','TL':'Timor-Leste','TG':'Togo','TK':'Tokelau','TO':'Tonga','TT':'Trinidad and Tobago','TN':'Tunisia','TR':'Turkey','TM':'Turkmenistan','TC':'Turks and Caicos Islands','TV':'Tuvalu','UG':'Uganda','UA':'Ukraine','AE':'United Arab Emirates','GB':'United Kingdom','US':'United States','UM':'United States Minor Outlying Islands','UY':'Uruguay','UZ':'Uzbekistan','VU':'Vanuatu','VE':'Venezuela, Bolivarian Republic of','VN':'Viet Nam','VG':'Virgin Islands, British','VI':'Virgin Islands, U.S.','WF':'Wallis and Futuna','EH':'Western Sahara','YE':'Yemen','ZM':'Zambia','ZW':'Zimbabwe'};

# Thanks to https://stackoverflow.com/a/34499643
def requires_login(f):
    @wraps(f)
    def inner(*args, **kws):
        User = None
        # TODO: change cookie name to config
        if request.cookies.get('hedy'):
            username = r.get ('sess:' + request.cookies.get ('hedy'))
            if not username:
                return 'unauthorized', 403
            user = r.hgetall ('user:' + username)
            if not user:
                return 'unauthorized', 403
        else:
            return 'unauthorized', 403

        return f(user, *args, **kws)
    return inner

def routes(app):
    @app.route('/auth/login', methods=['POST'])
    def login():
        body = request.json
        # Validations
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'username must be a string', 400
        if not object_check (body, 'password', 'str'):
            return 'password must be a string', 400

        # If username has an @-sign, then it's an email
        if re.match ('@', body ['username']):
           username = r.hget ('emails', body ['username'])
           if not username:
              return 'invalid username/password', 403
        else:
           username = body ['username']

        username = username.strip ().lower ()

        user = r.hgetall ('user:' + username)
        if not user:
            return 'invalid username/password', 403
        if not check_password (body ['password'], user ['password']):
            return 'invalid username/password', 403

        cookie = make_salt ()
        # Set session for one day
        # TODO: move duration to config
        r.setex ('sess:' + cookie, 1000 * 60 * 60 * 24, body ['username'])
        r.hset ('user:' + body ['username'], 'lastAccess', timems ())
        # TODO: move cookie name to config
        resp = make_response({})
        resp.set_cookie('hedy', value=cookie, httponly=True, path='/')
        return resp

    @app.route('/auth/signup', methods=['POST'])
    def signup():
        body = request.json
        # Validations, mandatory fields
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'username must be a string', 400
        if re.match ('@', body ['username']):
            return 'username cannot contain an @-sign', 400
        if re.match (':', body ['username']):
            return 'username cannot contain a colon', 400
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
        if 'age' in body:
            if not object_check (body, 'age', 'int') or body ['age'] <= 0:
                return 'age must be an integer larger than 0', 400
        if 'gender' in body:
            if body ['gender'] != 'm' and body ['gender'] != 'f':
                return 'gender must be m/f', 400

        user = r.hgetall ('user:' + body ['username'])
        if user:
            return 'username exists', 403
        email = r.hget ('emails', body ['email'])
        if email:
            return 'email exists', 403

        hashed = hash(body ['password'], make_salt ())

        user = {
           'username': body ['username'].strip ().lower (),
           'password': hashed,
           'email':    body ['email'].strip ().lower (),
           'created':  timems ()
        }

        if 'country' in body:
           user ['country'] = body ['country']
        if 'age' in body:
           user ['age'] = body ['age']
        if 'gender' in body:
           user ['gender'] = body ['gender']

        r.hmset ('user:' + body ['username'], user);
        r.hset ('emails', body ['email'], body ['username'])

        return '', 200

    @app.route('/auth/logout', methods=['POST'])
    def logout():
        if request.cookies.get('hedy'):
            r.delete ('sess:' + request.cookies.get('hedy'))
        return '', 200

    @app.route('/auth/destroy', methods=['POST'])
    @requires_login
    def destroy(user):
        r.delete ('sess:' + request.cookies.get('hedy'))
        r.delete ('user:' + user ['username'])
        r.hdel ('emails', user ['email'])
        return '', 200

    @app.route('/auth/changePassword', methods=['POST'])
    @requires_login
    def change_password(user):

        body = request.json
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'oldPassword', 'str'):
            return 'body.oldPassword must be a string', 400
        if not object_check (body, 'newPassword', 'str'):
            return 'body.newPassword must be a string', 400

        if not check_password (body ['oldPassword'], user ['password']):
            return 'invalid username/password', 403

        hashed = hash(body ['newPassword'], make_salt ())

        r.hset ('user:' + user ['username'], 'password', hashed)
        return '', 200

    @app.route('/profile', methods=['POST'])
    @requires_login
    def update_profile(user):

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
        if 'age' in body:
            if not object_check (body, 'age', 'int') or body ['age'] <= 0:
                return 'body.age must be an integer larger than 0', 400
        if 'gender' in body:
            if body ['gender'] != 'm' and body ['gender'] != 'f':
                return 'body.gender must be m/f', 400

        if 'email' in body:
            r.hdel ('emails', user ['email'])
            r.hset ('emails', body ['email'], user ['username'])
            r.hset ('user:' + user ['username'], 'email', body ['email'])

        if 'country' in body:
            r.hset ('user:' + user ['username'], 'country', body ['country'])
        if 'age' in body:
            r.hset ('user:' + user ['username'], 'age', body ['age'])
        if 'gender' in body:
            r.hset ('user:' + user ['username'], 'gender', body ['gender'])
        return '', 200

    @app.route('/profile', methods=['GET'])
    @requires_login
    def get_profile(user):
        user = r.hmget ('user:' + user ['username'], 'username', 'email', 'age', 'country', 'gender')
        output = {'username': user [0], 'email': user [1]}
        if user [2]:
            output ['age'] = user [2]
        if user [3]:
            output ['country'] = user [3]
        if user [4]:
            output ['gender'] = user [4]

        return jsonify(output), 200

    @app.route('/auth/recover', methods=['POST'])
    def recover():
        body = request.json
        # Validations
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'username', 'str'):
            return 'body.username must be a string', 400

        # If username has an @-sign, then it's an email
        if re.match ('@', body ['username']):
           username = r.hget ('emails', body ['username'])
           if not username:
              return 'invalid username/password', 403
        else:
           username = body ['username']

        username = username.strip ().lower ()

        user = r.hgetall ('user:' + username)

        if not user:
            return 'invalid username', 403

        token = make_salt ()
        hashed = hash(token, make_salt ())

        # TODO: move duration to config
        r.setex ('token:' + hashed, 1000 * 60 * 60 * 24, body ['username'])
        # TODO: when in non-local environment, email the token instead of returning it
        return token

    @app.route('/auth/reset', methods=['POST'])
    def reset():
        body = request.json
        # Validations
        if not type_check (body, 'dict'):
            return 'body must be an object', 400
        if not object_check (body, 'token', 'str'):
            return 'body.token must be a string', 400
        if not object_check (body, 'password', 'str'):
            return 'body.password be a string', 400

        username = r.get ('token:' + body ['token'])
        if not username:
           return 'invalid token', 403

        hashed = hash(body ['password'], make_salt ())
        r.delete ('token:' + body ['token'])
        r ['hset'] ('user:' + username, 'password', hashed)
        return {}, 200
