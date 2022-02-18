# coding=utf-8
import sys

import hedy_translation
from website.yaml_file import YamlFile

if (sys.version_info.major < 3 or sys.version_info.minor < 7):
    print('Hedy requires Python 3.7 or newer to run. However, your version of Python is',
          '.'.join([str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro)]))
    quit()

import datetime
import collections
import hedy
import json
import logging
import os
from os import path
import re
import traceback
from flask_commonmark import Commonmark
from werkzeug.urls import url_encode
from config import config
from website.auth import auth_templates, current_user, login_user_from_token_cookie, requires_login, is_admin, \
    is_teacher, update_is_teacher
from utils import timems, load_yaml_rt, dump_yaml_rt, version, is_debug_mode
import utils
import textwrap

# app.py
from flask import Flask, request, jsonify, session, abort, g, redirect, Response, make_response, Markup
from flask_helpers import render_template
from flask_compress import Compress
from flask_babel import Babel
from flask_babel import gettext

# Hedy-specific modules
import hedy_content
import hedyweb
from website import querylog, aws_helpers, jsonbin, translating, ab_proxying, cdn, database, achievements
from website.log_fetcher import log_fetcher

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

# Define and load all available language content
ALL_LANGUAGES = {
    'en': 'English',
    'nl': 'Nederlands',
    'es': 'Español',
    'fr': 'Français',
    'pt_pt': 'Português(pt)',
    'pt_br': 'Português(br)',
    'de': 'Deutsch',
    'it': 'Italiano',
    'sw': 'Swahili',
    'hu': 'Magyar',
    'el': 'Ελληνικά',
    'zh': "简体中文",
    'cs': 'Čeština',
    'bg': 'Български',
    'bn': 'বাংলা',
    'hi': 'हिंदी',
    'id': 'Bahasa Indonesia',
    'fy': 'Frysk',
    'ar': 'عربى'
}
# Define fall back languages for adventures
FALL_BACK_ADVENTURE = {
    'fy': 'nl',
    'pt_br': 'pt_pt'
}

ALL_KEYWORD_LANGUAGES = {
    'en': 'EN',
    'nl': 'NL',
    'es': 'ES'
}

LEVEL_DEFAULTS = collections.defaultdict(hedy_content.NoSuchDefaults)
for lang in ALL_LANGUAGES.keys():
    LEVEL_DEFAULTS[lang] = hedy_content.LevelDefaults(lang)

ADVENTURES = collections.defaultdict(hedy_content.NoSuchAdventure)
for lang in ALL_LANGUAGES.keys():
    ADVENTURES[lang] = hedy_content.Adventures(lang)

TRANSLATIONS = hedyweb.Translations()
ACHIEVEMENTS_TRANSLATIONS = hedyweb.AchievementTranslations()
ACHIEVEMENTS = achievements.Achievements()
DATABASE = database.Database()

# Define code that will be used if some turtle command is present
TURTLE_PREFIX_CODE = textwrap.dedent("""\
    # coding=utf8
    import random, time, turtle
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.goto(50,100)
    t.showturtle()
    t.pendown()
    t.speed(3)
""")

# Preamble that will be used for non-Turtle programs
NORMAL_PREFIX_CODE = textwrap.dedent("""\
    # coding=utf8
    import random, time
""")


def load_adventure_for_language(lang):
    adventures_for_lang = ADVENTURES[lang]

    if not adventures_for_lang.has_adventures():
        # The default fall back language is English
        fall_back = FALL_BACK_ADVENTURE.get(lang, "en")
        adventures_for_lang = ADVENTURES[fall_back]
    return adventures_for_lang.adventures_file['adventures']


def load_adventures_per_level(lang, level):
    loaded_programs = {}
    # If user is logged in, we iterate their programs that belong to the current level. Out of these, we keep the latest created program for both the level mode(no adventure) and for each of the adventures.
    if current_user()['username']:
        user_programs = DATABASE.programs_for_user(current_user()['username'])
        for program in user_programs:
            if program['level'] != level:
                continue
            program_key = 'level' if not program.get('adventure_name') else program['adventure_name']
            if not program_key in loaded_programs:
                loaded_programs[program_key] = program
            elif loaded_programs[program_key]['date'] < program['date']:
                loaded_programs[program_key] = program

    all_adventures = []

    adventures = load_adventure_for_language(lang)

    for short_name, adventure in adventures.items():
        if not level in adventure['levels']:
            continue
        # end adventure is the quiz
        # if quizzes are not enabled, do not load it
        if short_name == 'end' and not config['quiz-enabled']:
            continue
        current_adventure = {
            'short_name': short_name,
            'name': adventure['name'],
            'image': adventure.get('image', None),
            'default_save_name': adventure['default_save_name'],
            'text': adventure['levels'][level].get('story_text', 'No Story Text'),
            'example_code': adventure['levels'][level].get('example_code'),
            'start_code': adventure['levels'][level].get('start_code', ''),
            'loaded_program': '' if not loaded_programs.get(short_name) else {
                'name': loaded_programs.get(short_name)['name'],
                'code': loaded_programs.get(short_name)['code']
            }
        }
        #Sometimes we have multiple text and example_code -> iterate these and add as well!
        extra_stories = []
        for i in range(2, 10):
            extra_story = {}
            if adventure['levels'][level].get('story_text_' + str(i)):
                extra_story['text'] = adventure['levels'][level].get('story_text_' + str(i))
                if adventure['levels'][level].get('example_code_' + str(i)):
                    extra_story['example_code'] = adventure['levels'][level].get('example_code_' + str(i))
                extra_stories.append(extra_story)
            else:
                break
        current_adventure['extra_stories'] = extra_stories
        all_adventures.append(current_adventure)
    # We create a 'level' pseudo assignment to store the loaded program for level mode, if any.
    all_adventures.append({
        'short_name': 'level',
        'loaded_program': '' if not loaded_programs.get('level') else {
            'name': loaded_programs.get('level')['name'],
            'code': loaded_programs.get('level')['code']
        }
    })
    return all_adventures


# Load main menu(do it once, can be cached)
with open(f'menu.json', 'r', encoding='utf-8') as f:
    main_menu_json = json.load(f)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)-8s: %(message)s')

app = Flask(__name__, static_url_path='')
# Ignore trailing slashes in URLs
app.url_map.strict_slashes = False

babel = Babel(app)


# Return the session language, if not: return best match
@babel.localeselector
def get_locale():
    return session.get("lang", request.accept_languages.best_match(ALL_LANGUAGES.keys(), 'en'))


"""
    Some important notes relates to Flask-Babel usage:
    
    -   We can always get a translation using gettext(u'english string')
        NOTE: We can shorten this notation by simply using _('english string')
    -   We can insert some variable like this: gettext(u'some string %(value)s', value=42)
    -   More interesting for us might be the 'lazy string' the can be defined outside requests, like this:
    -       lazy_gettext(u'Account successfully saved')
    -   This will be really useful when wanting to return translated error messages
    
    - We have to mark ALL translatable string (in english!) with gettext() -> then create a .pot file
    - We create the file as follows: 
        pybabel extract -F babel.cfg -o messages.pot .
    - To add a translation (for dutch): 
        pybabel init -i messages.pot -d translations -l nl
    - To update your files (when adding new strings):
        FIRST create new file:  pybabel extract -F babel.cfg -o messages.pot . 
        THEN:                   pybabel update -i messages.pot -d translations
"""


cdn.Cdn(app, os.getenv('CDN_PREFIX'), os.getenv('HEROKU_SLUG_COMMIT', 'dev'))


@app.before_request
def before_request_begin_logging():
    """Initialize the query logging.

    This needs to happen as one of the first things, as the database calls
    etc. depend on it.
    """
    path = (str(request.path) + '?' + str(request.query_string)) if request.query_string else str(request.path)
    querylog.begin_global_log_record(path=path, method=request.method)


@app.after_request
def after_request_log_status(response):
    querylog.log_value(http_code=response.status_code)
    return response


@app.before_request
def initialize_session():
    """Make sure the session is initialized.

    - Each session gets a unique session ID, so we can tell user sessions apart
      and know what programs get submitted after each other.
    - If the user has a cookie with a long-lived login token, log them in from
      that cookie (copy the user info into the session for efficient access
      later on).
    """
    # Invoke session_id() for its side effect
    utils.session_id()
    login_user_from_token_cookie()


if os.getenv('IS_PRODUCTION'):
    @app.before_request
    def reject_e2e_requests():
        if utils.is_testing_request(request):
            return 'No E2E tests are allowed in production', 400


@app.before_request
def before_request_proxy_testing():
    if utils.is_testing_request(request):
        if os.getenv('IS_TEST_ENV'):
            session['test_session'] = 'test'


# HTTP -> HTTPS redirect
# https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http/32238093
if os.getenv('REDIRECT_HTTP_TO_HTTPS'):
    @app.before_request
    def before_request_https():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            # We use a 302 in case we need to revert the redirect.
            return redirect(url, code=302)

# Unique random key for sessions.
# For settings with multiple workers, an environment variable is required, otherwise cookies will be constantly removed and re-set by different workers.
if utils.is_production():
    if not os.getenv('SECRET_KEY'):
        raise RuntimeError('The SECRET KEY must be provided for non-dev environments.')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

else:
    # The value doesn't matter for dev environments, but it needs to be a constant
    # so that our cookies don't get invalidated every time we restart the server.
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'WeAreDeveloping')

if utils.is_heroku():
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

# Set security attributes for cookies in a central place - but not when running locally, so that session cookies work well without HTTPS

Compress(app)
Commonmark(app)
parse_logger = jsonbin.MultiParseLogger(
    jsonbin.JsonBinLogger.from_env_vars(),
    jsonbin.S3ParseLogger.from_env_vars())
querylog.LOG_QUEUE.set_transmitter(aws_helpers.s3_querylog_transmitter_from_env())


@app.before_request
def setup_language():
    # Determine the user's requested language code.
    #
    # If not in the request parameters, use the browser's accept-languages
    # header to do language negotiation.
    if 'lang' not in session:
        session['lang'] = request.accept_languages.best_match(ALL_LANGUAGES.keys(), 'en')
    g.lang = session['lang']


    # Always set the keyword languages to English when starting
    g.keyword_lang = "en"

    # Set the page direction -> automatically set it to "left-to-right"
    # Switch to "right-to-left" if one of the language in the list is selected
    # This is the only place to expand / shrink the list of RTL languages -> front-end is fixed based on this value
    g.dir = "ltr"
    if g.lang in ['ar', 'he', 'ur']:
        g.dir = "rtl"


    # Check that requested language is supported, otherwise return 404
    if g.lang not in ALL_LANGUAGES.keys():
        return "Language " + g.lang + " not supported", 404
    # Also get the 'ui' translations into a global object for this language, these
    # are used a lot so we can clean up a fair bit by initializing here.
    g.ui_texts = TRANSLATIONS.get_translations(g.lang, 'ui')
    g.auth_texts = TRANSLATIONS.get_translations(g.lang, 'Auth')


if utils.is_heroku() and not os.getenv('HEROKU_RELEASE_CREATED_AT'):
    logging.warning(
        'Cannot determine release; enable Dyno metadata by running "heroku labs:enable runtime-dyno-metadata -a <APP_NAME>"')


# A context processor injects variables in the context that are available to all templates.
@app.context_processor
def enrich_context_with_user_info():
    user = current_user()
    data = {'username': user.get('username', ''), 'is_teacher': is_teacher(user), 'is_admin': is_admin(user)}
    if len(data['username']) > 0: #If so, there is a user -> Retrieve all relevant info
        user_data = DATABASE.user_by_username(user.get('username'))
        data['user_messages'] = 0
        if 'language' in user_data:
            if user_data['language'] in ALL_LANGUAGES.keys():
                g.lang = session['lang'] = user_data['language']
        data['user_data'] = user_data
        if 'classes' in user_data:
            data['user_classes'] = DATABASE.get_student_classes(user.get('username'))
        user_achievements = DATABASE.achievements_by_username(user.get('username'))
        if user_achievements:
            data['user_achievements'] = user_achievements
        user_invites = DATABASE.get_username_invite(user.get('username'))
        if user_invites:
            Class = DATABASE.get_class(user_invites['class_id'])
            if Class:
                invite_data = user_invites.copy()
                invite_data['class_name'] = Class.get('name')
                invite_data['teacher'] = Class.get('teacher')
                invite_data['join_link'] = Class.get('link')
                data['invite_data'] = invite_data
                data['user_messages'] += 1
    return data

@app.context_processor
def enricht_context_with_translations():
    """Adds dicts with translations to the global template context.

    For some reason these are held in various different sections in the YAMLs.
    """
    texts = TRANSLATIONS.get_translations(g.lang, 'Programs')
    ui = TRANSLATIONS.get_translations(g.lang, 'ui')
    auth = TRANSLATIONS.get_translations(g.lang, 'Auth')
    achievements = ACHIEVEMENTS_TRANSLATIONS.get_translations(g.lang)
    return dict(texts=texts, ui=ui, auth=auth, achievements=achievements)

@app.after_request
def set_security_headers(response):
    security_headers = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-XSS-Protection': '1; mode=block',
    }
    # Not X-Frame-Options on purpose -- we are being embedded by Online Masters
    # and that's okay.
    response.headers.update(security_headers)
    return response

@app.teardown_request
def teardown_request_finish_logging(exc):
    querylog.finish_global_log_record(exc)


# If present, PROXY_TO_TEST_HOST should be the 'http[s]://hostname[:port]' of the target environment
if os.getenv('PROXY_TO_TEST_HOST') and not os.getenv('IS_TEST_ENV'):
    ab_proxying.ABProxying(app, os.getenv('PROXY_TO_TEST_HOST'), app.config['SECRET_KEY'])


@app.route('/session_test', methods=['GET'])
def echo_session_vars_test():
    if not utils.is_testing_request(request):
        return 'This endpoint is only meant for E2E tests', 400
    return jsonify({'session': dict(session)})


@app.route('/session_main', methods=['GET'])
def echo_session_vars_main():
    if not utils.is_testing_request(request):
        return 'This endpoint is only meant for E2E tests', 400
    return jsonify({'session': dict(session), 'proxy_enabled': bool(os.getenv('PROXY_TO_TEST_HOST'))})


@app.route('/fix-code', methods=['POST'])
def fix_code():
    body = request.json
    if not body:
        return "body must be an object", 400
    if 'code' not in body:
        return "body.code must be a string", 400
    if 'level' not in body:
        return "body.level must be a string", 400
    if 'adventure_name' in body and not isinstance(body['adventure_name'], str):
        return "if present, body.adventure_name must be a string", 400

    code = body['code']
    level = int(body['level'])

    # Language should come principally from the request body,
    # but we'll fall back to browser default if it's missing for whatever
    # reason.
    lang = body.get('lang', g.lang)

    # true if kid enabled the read aloud option
    read_aloud = body.get('read_aloud', False)

    response = {}
    username = current_user()['username'] or None
    exception = None

    querylog.log_value(level=level, lang=lang, session_id=utils.session_id(), username=username)

    try:
        hedy_errors = TRANSLATIONS.get_translations(lang, 'HedyErrorMessages')
        with querylog.log_time('transpile'):

            try:
                transpile_result = hedy.transpile(code, level)
                response = "OK"
            except hedy.exceptions.FtfyException as ex:
                # The code was fixed with a warning
                response['Error'] = translate_error(ex.error_code, hedy_errors, ex.arguments)
                response['FixedCode'] = ex.fixed_code
                response['Location'] = ex.error_location
                transpile_result = ex.fixed_result
                exception = ex

    except hedy.exceptions.HedyException as ex:
        traceback.print_exc()
        response = hedy_error_to_response(ex, hedy_errors)
        exception = ex

    except Exception as E:
        traceback.print_exc()
        print(f"error transpiling {code}")
        response["Error"] = str(E)
        exception = ex

    querylog.log_value(server_error=response.get('Error'))
    parse_logger.log({
        'session': utils.session_id(),
        'date': str(datetime.datetime.now()),
        'level': level,
        'lang': lang,
        'code': code,
        'server_error': response.get('Error'),
        'exception': get_class_name(exception),
        'version': version(),
        'username': username,
        'read_aloud': read_aloud,
        'is_test': 1 if os.getenv('IS_TEST_ENV') else None,
        'adventure_name': body.get('adventure_name', None)
    })

    return jsonify(response)


@app.route('/parse', methods=['POST'])
def parse():
    body = request.json
    if not body:
        return "body must be an object", 400
    if 'code' not in body:
        return "body.code must be a string", 400
    if 'level' not in body:
        return "body.level must be a string", 400
    if 'adventure_name' in body and not isinstance(body['adventure_name'], str):
        return "if present, body.adventure_name must be a string", 400

    code = body['code']
    level = int(body['level'])

    # Language should come principally from the request body,
    # but we'll fall back to browser default if it's missing for whatever
    # reason.
    lang = body.get('lang', g.lang)

    # true if kid enabled the read aloud option
    read_aloud = body.get('read_aloud', False)

    response = {}
    username = current_user()['username'] or None
    exception = None

    querylog.log_value(level=level, lang=lang, session_id=utils.session_id(), username=username)

    try:
        hedy_errors = TRANSLATIONS.get_translations(lang, 'HedyErrorMessages')
        with querylog.log_time('transpile'):

            try:
                transpile_result = transpile_add_stats(code, level, lang)
                if username:
                    DATABASE.increase_user_run_count(username)
                    ACHIEVEMENTS.increase_count("run")
            except hedy.exceptions.InvalidSpaceException as ex:
                response['Warning'] = translate_error(ex.error_code, hedy_errors, ex.arguments)
                response['Location'] = ex.error_location
                transpile_result = ex.fixed_result
                exception = ex
            except hedy.exceptions.InvalidCommandException as ex:
                response['Error'] = translate_error(ex.error_code, hedy_errors, ex.arguments)
                response['Location'] = ex.error_location
                transpile_result = ex.fixed_result
                exception = ex
            except hedy.exceptions.FtfyException as ex:
                response['Error'] = translate_error(ex.error_code, hedy_errors, ex.arguments)
                response['Location'] = ex.error_location
                transpile_result = ex.fixed_result
                exception = ex
            except hedy.exceptions.UnquotedEqualityCheck as ex:
                response['Error'] = translate_error(ex.error_code, hedy_errors, ex.arguments)
                response['Location'] = ex.error_location
                exception = ex
        try:
            if transpile_result.has_turtle:
                response['Code'] = TURTLE_PREFIX_CODE + transpile_result.code
                response['has_turtle'] = True
            else:
                response['Code'] = NORMAL_PREFIX_CODE + transpile_result.code
        except:
            pass
        try:
            if 'sleep' in hedy.all_commands(code, level, lang):
                response['has_sleep'] = True
        except:
            pass
        try:
            if username and ACHIEVEMENTS.verify_run_achievements(username, code, level, response):
                response['achievements'] = ACHIEVEMENTS.get_earned_achievements()
        except Exception as E:
            print(f"error determining achievements for {code} with {E}")
    except hedy.exceptions.HedyException as ex:
        traceback.print_exc()
        response = hedy_error_to_response(ex, hedy_errors)
        exception = ex

    except Exception as E:
        traceback.print_exc()
        print(f"error transpiling {code}")
        response["Error"] = str(E)
        exception = E

    querylog.log_value(server_error=response.get('Error'))
    parse_logger.log({
        'session': utils.session_id(),
        'date': str(datetime.datetime.now()),
        'level': level,
        'lang': lang,
        'code': code,
        'server_error': response.get('Error'),
        'exception': get_class_name(exception),
        'version': version(),
        'username': username,
        'read_aloud': read_aloud,
        'is_test': 1 if os.getenv('IS_TEST_ENV') else None,
        'adventure_name': body.get('adventure_name', None)
    })

    return jsonify(response)


@app.route('/parse-by-id', methods=['POST'])
@requires_login
def parse_by_id(user):
    body = request.json
    #Validations
    if not isinstance(body, dict):
        return 'body must be an object', 400
    if not isinstance(body.get('id'), str):
        return 'class id must be a string', 400

    program = DATABASE.program_by_id(body.get('id'))
    if program and program.get('username') == user['username']:
        try:
            hedy.transpile(program.get('code'), program.get('level'), program.get('lang'))
            return {}, 200
        except:
            return {"error": "parsing error"}, 200
    else:
        return 'this is not your program!', 400


def transpile_add_stats(code, level, lang_):
    username = current_user()['username'] or None
    try:
        result = hedy.transpile(code, level, lang_)
        statistics.add(username, lambda id_: DATABASE.add_program_stats(id_, level, None))
        return result
    except Exception as ex:
        statistics.add(username, lambda id_: DATABASE.add_program_stats(id_, level, get_class_name(ex)))
        raise


def get_class_name(i):
    if i is not None:
        return str(i.__class__.__name__)
    return i


def hedy_error_to_response(ex, translations):
    return {
        "Error": translate_error(ex.error_code, translations, ex.arguments),
        "Location": ex.error_location
    }


def translate_error(code, translations, arguments):
    arguments_that_require_translation = ['allowed_types', 'invalid_type', 'invalid_type_2', 'character_found',
                                          'concept', 'tip']
    arguments_that_require_highlighting = ['command', 'guessed_command', 'invalid_argument', 'invalid_argument_2',
                                           'variable']
    # fetch the error template
    error_template = translations[code]

    # some arguments like allowed types or characters need to be translated in the error message
    for k, v in arguments.items():
        if k in arguments_that_require_highlighting:
            arguments[k] = hedy.style_closest_command(v)

        if k in arguments_that_require_translation:
            if isinstance(v, list):
                arguments[k] = translate_list(translations, v)
            else:
                arguments[k] = translations.get(v, v)

    return error_template.format(**arguments)


def translate_list(translations, args):
    translated_args = [translations.get(a, a) for a in args]
    # Deduplication is needed because diff values could be translated to the same value, e.g. int and float => a number
    translated_args = list(dict.fromkeys(translated_args))

    if len(translated_args) > 1:
        return f"{', '.join(translated_args[0:-1])}" \
               f" {translations.get('or', 'or')} " \
               f"{translated_args[-1]}"
    return ''.join(translated_args)


@app.route('/report_error', methods=['POST'])
def report_error():
    post_body = request.json

    parse_logger.log({
        'session': utils.session_id(),
        'date': str(datetime.datetime.now()),
        'level': post_body.get('level'),
        'code': post_body.get('code'),
        'client_error': post_body.get('client_error'),
        'version': version(),
        'username': current_user()['username'] or None,
        'is_test': 1 if os.getenv('IS_TEST_ENV') else None
    })

    return 'logged'


@app.route('/client_exception', methods=['POST'])
def report_client_exception():
    post_body = request.json

    querylog.log_value(
        session=utils.session_id(),
        date=str(datetime.datetime.now()),
        client_error=post_body,
        version=version(),
        username=current_user()['username'] or None,
        is_test=1 if os.getenv('IS_TEST_ENV') else None
    )

    # Return a 500 so the HTTP status codes will stand out in our monitoring/logging
    return 'logged', 500


@app.route('/version', methods=['GET'])
def version_page():
    """
    Generate a page with some diagnostic information and a useful GitHub URL on upcoming changes.

    This is an admin-only page, it does not need to be linked.
   (Also does not have any sensitive information so it's fine to be unauthenticated).
    """
    app_name = os.getenv('HEROKU_APP_NAME')

    vrz = os.getenv('HEROKU_RELEASE_CREATED_AT')
    the_date = datetime.date.fromisoformat(vrz[:10]) if vrz else datetime.date.today()

    commit = os.getenv('HEROKU_SLUG_COMMIT', '????')[0:6]

    return render_template('version-page.html',
                           app_name=app_name,
                           heroku_release_time=the_date,
                           commit=commit)


def achievements_page():
    user = current_user()
    username = user['username']
    if not username:
        # redirect users to /login if they are not logged in
        # Todo: TB -> I wrote this once, but wouldn't it make more sense to simply throw a 302 error?
        url = request.url.replace('/my-achievements', '/login')
        return redirect(url, code=302)

    achievement_translations = hedyweb.PageTranslations('achievements').get_page_translations(g.lang)

    return render_template('achievements.html', page_title=hedyweb.get_page_title('achievements'),
                           template_achievements=achievement_translations, current_page='my-profile')


@app.route('/programs', methods=['GET'])
@requires_login
def programs_page(user):
    username = user['username']
    if not username:
        # redirect users to /login if they are not logged in
        url = request.url.replace('/programs', '/login')
        return redirect(url, code=302)

    from_user = request.args.get('user') or None
    # If from_user -> A teacher is trying to view the user programs
    if from_user and not is_admin(user):
        if not is_teacher(user):
            return utils.error_page(error=403, ui_message='not_teacher')
        students = DATABASE.get_teacher_students(username)
        if from_user not in students:
            return utils.error_page(error=403, ui_message='not_enrolled')

    adventures = load_adventure_for_language(g.lang)
    if hedy_content.Adventures(session['lang']).has_adventures():
        adventures_names = hedy_content.Adventures(session['lang']).get_adventure_keyname_name_levels()
    else:
        adventures_names = hedy_content.Adventures("en").get_adventure_keyname_name_levels()

    # We request our own page -> also get the public_profile settings
    public_profile = None
    if not from_user:
        public_profile = DATABASE.get_public_profile_settings(username)

    level = request.args.get('level', default=None, type=str)
    adventure = request.args.get('adventure', default=None, type=str)
    level = None if level == "null" else level
    adventure = None if adventure == "null" else adventure

    if level or adventure:
        result = DATABASE.filtered_programs_for_user(from_user or username, level, adventure)
    else:
        result = DATABASE.programs_for_user(from_user or username)

    programs = []
    now = timems()
    for item in result:
        date = get_user_formatted_age(now, item['date'])
        programs.append(
            {'id': item['id'], 'code': item['code'], 'date': date, 'level': item['level'], 'name': item['name'],
             'adventure_name': item.get('adventure_name'), 'submitted': item.get('submitted'),
             'public': item.get('public')})

    return render_template('programs.html', programs=programs, page_title=hedyweb.get_page_title('programs'),
                           current_page='programs', from_user=from_user, adventures=adventures,
                           filtered_level=level, filtered_adventure=adventure, adventure_names=adventures_names,
                           public_profile=public_profile, max_level=hedy.HEDY_MAX_LEVEL)


@app.route('/logs/query', methods=['POST'])
def query_logs():
    user = current_user()
    if not is_admin(user) and not is_teacher(user):
        return 'unauthorized', 403

    body = request.json
    if body is not None and not isinstance(body, dict):
        return 'body must be an object', 400

    class_id = body.get('class_id')
    if not is_admin(user):
        username_filter = body.get('username')
        if not class_id or not username_filter:
            return 'unauthorized', 403

        class_ = DATABASE.get_class(class_id)
        if not class_ or class_['teacher'] != user['username'] or username_filter not in class_.get('students', []):
            return 'unauthorized', 403

    (exec_id, status) = log_fetcher.query(body)
    response = {'query_status': status, 'query_execution_id': exec_id}
    return jsonify(response)


@app.route('/logs/results', methods=['GET'])
def get_log_results():
    query_execution_id = request.args.get('query_execution_id', default=None, type=str)
    next_token = request.args.get('next_token', default=None, type=str)

    user = current_user()
    if not is_admin(user) and not is_teacher(user):
        return 'unauthorized', 403

    data, next_token = log_fetcher.get_query_results(query_execution_id, next_token)
    response = {'data': data, 'next_token': next_token}
    return jsonify(response)


def get_user_formatted_age(now, date):
    texts = TRANSLATIONS.get_translations(g.lang, 'Programs')
    program_age = now - date
    if program_age < 1000 * 60 * 60:
        measure = texts['minutes']
        date = round(program_age / (1000 * 60))
    elif program_age < 1000 * 60 * 60 * 24:
        measure = texts['hours']
        date = round(program_age / (1000 * 60 * 60))
    else:
        measure = texts['days']
        date = round(program_age / (1000 * 60 * 60 * 24))

    return f"{texts['ago-1']} {date} {measure} {texts['ago-2']}"


# routing to index.html
@app.route('/ontrack', methods=['GET'], defaults={'level': '1', 'step': 1})
@app.route('/onlinemasters', methods=['GET'], defaults={'level': '1', 'step': 1})
@app.route('/onlinemasters/<int:level>', methods=['GET'], defaults={'step': 1})
@app.route('/space_eu', methods=['GET'], defaults={'level': '1', 'step': 1})
@app.route('/hedy', methods=['GET'], defaults={'level': '1', 'step': 1})
@app.route('/hedy/<level>', methods=['GET'], defaults={'step': 1})
@app.route('/hedy/<level>/<step>', methods=['GET'])
def index(level, step):
    if re.match('\\d', level):
        try:
            g.level = level = int(level)
        except:
            return utils.error_page(error=404, ui_message='no_such_level')
    else:
        return utils.error_page(error=404, ui_message='no_such_level')

    g.prefix = '/hedy'

    loaded_program = ''
    adventure_name = ''

    # If step is a string that has more than two characters, it must be an id of a program
    if step and isinstance(step, str) and len(step) > 2:
        result = DATABASE.program_by_id(step)
        if not result:
            return utils.error_page(error=404, ui_message='no_such_program')

        user = current_user()
        public_program = 'public' in result and result['public']
        if not public_program and user['username'] != result['username'] and not is_admin(user) and not is_teacher(
                user):
            return utils.error_page(error=404, ui_message='no_such_program')
        loaded_program = {'code': result['code'], 'name': result['name'],
                          'adventure_name': result.get('adventure_name')}
        if 'adventure_name' in result:
            adventure_name = result['adventure_name']

    adventures = load_adventures_per_level(g.lang, level)
    customizations = {}
    if current_user()['username']:
        customizations = DATABASE.get_student_class_customizations(current_user()['username'])
    level_defaults_for_lang = LEVEL_DEFAULTS[g.lang]

    if level not in level_defaults_for_lang.levels or ('levels' in customizations and level not in customizations['levels']):
        return utils.error_page(error=404, ui_message='no_such_level')
    defaults = level_defaults_for_lang.get_defaults_for_level(level)
    max_level = level_defaults_for_lang.max_level()

    teacher_adventures = []
    for adventure in customizations.get('teacher_adventures', []):
        teacher_adventures.append(DATABASE.get_adventure(adventure))

    return hedyweb.render_code_editor_with_tabs(
        level_defaults=defaults,
        max_level=max_level,
        level_number=level,
        version=version(),
        adventures=adventures,
        customizations=customizations,
        teacher_adventures=teacher_adventures,
        loaded_program=loaded_program,
        adventure_name=adventure_name)


@app.route('/hedy/<id>/view', methods=['GET'])
def view_program(id):
    g.prefix = '/hedy'

    user = current_user()

    result = DATABASE.program_by_id(id)
    if not result:
        return utils.error_page(error=404, ui_message='no_such_program')

    # If we asked for a specific language, use that, otherwise use the language
    # of the program's author.
    # Default to the language of the program's author(but still respect)
    # the switch if given.
    g.lang = request.args.get('lang', result['lang'])

    arguments_dict = {}
    arguments_dict['program_id'] = id
    arguments_dict['page_title'] = f'{result["name"]} – Hedy'
    arguments_dict['level'] = result['level']  # Necessary for running
    arguments_dict['loaded_program'] = result
    arguments_dict['editor_readonly'] = True

    if "submitted" in result and result['submitted']:
        arguments_dict['show_edit_button'] = False
        now = timems()
        arguments_dict['program_age'] = get_user_formatted_age(now, result['date'])
        arguments_dict[
            'program_timestamp'] = f"{datetime.datetime.fromtimestamp(result['date'] / 1000.0).strftime('%d-%m-%Y, %H:%M:%S')} GMT"
    else:
        arguments_dict['show_edit_button'] = True

    # Everything below this line has nothing to do with this page and it's silly
    # that every page needs to put in so much effort to re-set it
    arguments_dict['menu'] = True
    arguments_dict['username'] = user.get('username', None)
    arguments_dict['is_teacher'] = is_teacher(user)

    return render_template("view-program-page.html", **arguments_dict)


@app.route('/client_messages.js', methods=['GET'])
def client_messages():
    error_messages = TRANSLATIONS.get_translations(g.lang, "ClientErrorMessages")
    ui_messages = TRANSLATIONS.get_translations(g.lang, "ui")
    auth_messages = TRANSLATIONS.get_translations(g.lang, "Auth")

    response = make_response(render_template("client_messages.js",
                                             error_messages=json.dumps(error_messages),
                                             ui_messages=json.dumps(ui_messages),
                                             auth_messages=json.dumps(auth_messages)))

    if not is_debug_mode():
        # Cache for longer when not devving
        response.cache_control.max_age = 60 * 60  # Seconds

    return response


@app.errorhandler(404)
def not_found(exception):
    return utils.error_page(error=404, ui_message='page_not_found')


@app.errorhandler(500)
def internal_error(exception):
    import traceback
    print(traceback.format_exc())
    return utils.error_page(error=500)


@app.route('/index.html')
@app.route('/')
def default_landing_page():
    return main_page('start')


@app.route('/<page>')
def main_page(page):
    if page == 'favicon.ico':
        abort(404)

    if page in ['signup', 'login', 'my-profile', 'recover', 'reset']:
        return auth_templates(page, hedyweb.get_page_title(page))

    if page == "my-achievements":
        return achievements_page()

    if page == 'learn-more':
        learn_more_translations = hedyweb.PageTranslations(page).get_page_translations(g.lang)
        return render_template('learn-more.html', page_title=hedyweb.get_page_title(page),
                               content=learn_more_translations)

    user = current_user()

    if page == 'landing-page':
        if user['username']:
            return render_template('landing-page.html', page_title=hedyweb.get_page_title(page),
                                   text=TRANSLATIONS.get_translations(g.lang, 'Landing_page'))
        else:
            return utils.error_page(error=403, ui_message='not_user')

    if page == 'for-teachers':
        for_teacher_translations = hedyweb.PageTranslations(page).get_page_translations(g.lang)
        if is_teacher(user):
            welcome_teacher = session.get('welcome-teacher') or False
            session.pop('welcome-teacher', None)
            teacher_classes = [] if not current_user()['username'] else DATABASE.get_teacher_classes(current_user()['username'], True)
            adventures = []
            for adventure in DATABASE.get_teacher_adventures(current_user()['username']):
                adventures.append({'id': adventure.get('id'), 'name': adventure.get('name'),
                                   'date': utils.datetotimeordate(utils.mstoisostring(adventure.get('date'))),
                                   'level': adventure.get('level')})

            return render_template('for-teachers.html', current_page='my-profile',
                                   page_title=hedyweb.get_page_title(page),
                                   content=for_teacher_translations, teacher_classes=teacher_classes,
                                   teacher_adventures=adventures, welcome_teacher=welcome_teacher)
        else:
            return utils.error_page(error=403, ui_message='not_teacher')

    requested_page = hedyweb.PageTranslations(page)
    if not requested_page.exists():
        abort(404)

    main_page_translations = requested_page.get_page_translations(g.lang)
    return render_template('main-page.html', page_title=hedyweb.get_page_title('start'),
                           content=main_page_translations)


@app.route('/explore', methods=['GET'])
def explore():
    if not current_user()['username']:
        return redirect('/login')

    level = request.args.get('level', default=None, type=str)
    adventure = request.args.get('adventure', default=None, type=str)

    level = None if level == "null" else level
    adventure = None if adventure == "null" else adventure

    achievement = None
    if level or adventure:
        programs = DATABASE.get_filtered_explore_programs(level, adventure)
        achievement = ACHIEVEMENTS.add_single_achievement(current_user()['username'], "indiana_jones")
    else:
        programs = DATABASE.get_all_explore_programs()

    filtered_programs = []
    for program in programs:
        # If program does not have an error value set -> parse it and set value
        if 'error' not in program:
            try:
                hedy.transpile(program.get('code'), program.get('level'), program.get('lang'))
                program['error'] = False
            except:
                program['error'] = True
            DATABASE.store_program(program)
        filtered_programs.append({
            'username': program['username'],
            'name': program['name'],
            'level': program['level'],
            'id': program['id'],
            'error': program['error'],
            'code': "\n".join(program['code'].split("\n")[:4])
        })

    if hedy_content.Adventures(session['lang']).has_adventures():
        adventures = hedy_content.Adventures(session['lang']).get_adventure_keyname_name_levels()
    else:
        adventures = hedy_content.Adventures("en").get_adventure_keyname_name_levels()

    return render_template('explore.html', programs=filtered_programs,
                           filtered_level=level,
                           achievement=achievement,
                           filtered_adventure=adventure,
                           max_level=hedy.HEDY_MAX_LEVEL,
                           adventures=adventures,
                           page_title=hedyweb.get_page_title('explore'),
                           current_page='explore')


@app.route('/change_language', methods=['POST'])
def change_language():
    body = request.json
    session['lang'] = body.get('lang')
    return jsonify({'succes': 200})

@app.route('/translate_keywords', methods=['POST'])
def translate_keywords():
    body = request.json
    translated_code = hedy_translation.translate_keywords(body.get('code'), body.get('start_lang'), body.get('goal_lang'), level=int(body.get('level', 1)))
    if translated_code:
        return jsonify({'success': 200, 'code': translated_code})
    else:
        return g.auth_texts.get('translate_error'), 400

@app.template_global()
def current_language():
    return make_lang_obj(g.lang)

@app.template_global()
def current_keyword_language():
    return make_keyword_lang_obj(g.keyword_lang)

@app.template_global()
def other_keyword_language():
    if session['lang'] in ALL_KEYWORD_LANGUAGES.keys() and g.keyword_lang != session['lang']:
        return make_keyword_lang_obj(g.lang)
    if g.keyword_lang != "en": #Always return English as an option!
        return make_keyword_lang_obj("en")
    return None

@app.template_global()
def main_menu_entries():
    """Return the entries that make up the main menu.

    Calls render_main_menu() to do it, and assume the first part of the current
    request's path is the "current page".
    """
    # path starts with '/', in case of empty call it 'start'
    first_path_component = request.path[1:].split('/')[0] or 'start'
    return render_main_menu(first_path_component)


@app.template_filter()
def nl2br(x):
    """Turn newlines into <br>"""
    # The input to this object will either be a literal string or a 'Markup' object.
    # In case of a literal string, we need to escape it first, because we have
    # to be able to make a distinction between safe and unsafe characters.
    #
    # In case of a Markup object, make sure to tell it the <br> we're adding is safe
    if not isinstance(x, Markup):
        x = Markup.escape(x)
    return x.replace('\n', Markup('<br />'))


@app.template_global()
def hedy_link(level_nr, assignment_nr, subpage=None):
    """Make a link to a Hedy page."""
    parts = [g.prefix]
    parts.append('/' + str(level_nr))
    if str(assignment_nr) != '1' or subpage:
        parts.append('/' + str(assignment_nr if assignment_nr else '1'))
    if subpage and subpage != 'code':
        parts.append('/' + subpage)
    return ''.join(parts)


@app.template_global()
def other_languages():
    cl = g.lang
    return [make_lang_obj(l) for l in ALL_LANGUAGES.keys() if l != cl]


def make_lang_obj(lang):
    """Make a language object for a given language."""
    return {
        'sym': ALL_LANGUAGES[lang],
        'lang': lang
    }

def make_keyword_lang_obj(lang):
    """Make a language object for a given language."""
    return {
        'sym': ALL_KEYWORD_LANGUAGES[lang],
        'lang': lang
    }


@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, url_encode(args))


def render_main_menu(current_page):
    """Render a list of(caption, href, selected, color) from the main menu."""
    return [dict(
        caption=item.get(g.lang, item.get('en', '???')),
        href='/' + item['_'],
        selected=(current_page == item['_']),
        accent_color=item.get('accent_color', 'white'),
        short_name=item['_']
    ) for item in main_menu_json['nav']]


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

    achievement = None
    current_profile = DATABASE.get_public_profile_settings(user['username'])
    if current_profile:
        if current_profile.get('image') != body.get('image'):
            achievement = ACHIEVEMENTS.add_single_achievement(current_user()['username'], "fresh_look")
    else:
        achievement = ACHIEVEMENTS.add_single_achievement(current_user()['username'], "go_live")
    DATABASE.update_public_profile(user['username'], body)
    if achievement:
        return {'achievement': achievement}, 200
    return '', 200

@app.route('/translate/<source>/<target>')
def translate_fromto(source, target):
    source_file = f'{source}.yaml'
    source_adventures = YamlFile.for_file(utils.construct_content_path('adventures', source_file)).to_dict()
    source_levels = YamlFile.for_file(utils.construct_content_path('level-defaults', source_file)).to_dict()
    source_texts = YamlFile.for_file(utils.construct_content_path('texts', source_file)).to_dict()
    source_keywords = YamlFile.for_file(utils.construct_content_path('keywords', source_file)).to_dict()

    target_file = f'{target}.yaml'
    target_adventures = YamlFile.for_file(utils.construct_content_path('adventures', target_file)).to_dict()
    target_levels = YamlFile.for_file(utils.construct_content_path('level-defaults', target_file)).to_dict()
    target_texts = YamlFile.for_file(utils.construct_content_path('texts', target_file)).to_dict()
    target_keywords = YamlFile.for_file(utils.construct_content_path('keywords', target_file)).to_dict()

    files = []

    files.append(translating.TranslatableFile(
        'Levels',
        f'level-defaults/{target}.yaml',
        translating.struct_to_sections(source_levels, target_levels)))

    files.append(translating.TranslatableFile(
        'Messages',
        f'texts/{target}.yaml',
        translating.struct_to_sections(source_texts, target_texts)))

    files.append(translating.TranslatableFile(
        'Adventures',
        f'adventures/{target}.yaml',
        translating.struct_to_sections(source_adventures, target_adventures)))

    files.append(translating.TranslatableFile(
        'Keywords (make sure there are no duplicate translations of keywords)',
        f'keywords/{target}.yaml',
        translating.struct_to_sections(source_keywords, target_keywords)))

    return render_template('translate-fromto.html',
                           source_lang=source,
                           target_lang=target,
                           files=files)


@app.route('/update_yaml', methods=['POST'])
def update_yaml():
    filename = utils.construct_content_path(request.form['file'])
    # The file MUST point to something inside our 'content' directory
    filepath = path.abspath(filename)
    expected_path = utils.construct_content_path()
    if not filepath.startswith(expected_path):
        raise RuntimeError('Invalid path given')

    data = load_yaml_rt(filepath)
    for key, value in request.form.items():
        if key.startswith('c:'):
            translating.apply_form_change(data, key[2:], translating.normalize_newlines(value))

    data = translating.normalize_yaml_blocks(data)

    return Response(dump_yaml_rt(data),
                    mimetype='application/x-yaml',
                    headers={'Content-disposition': 'attachment; filename=' + request.form['file'].replace('/', '-')})


@app.route('/user/<username>')
def public_user_page(username):
    if not current_user()['username']:
        return utils.error_page(error=403, ui_message='unauthorized')
    username = username.lower()
    user = DATABASE.user_by_username(username)
    if not user:
        return utils.error_page(error=404, ui_message='user_not_private')
    user_public_info = DATABASE.get_public_profile_settings(username)
    if user_public_info:
        user_programs = DATABASE.public_programs_for_user(username)
        user_achievements = DATABASE.progress_by_username(username)

        favourite_program = None
        if 'favourite_program' in user_public_info and user_public_info['favourite_program']:
            favourite_program = DATABASE.program_by_id(user_public_info['favourite_program'])
        if len(user_programs) >= 5:
            user_programs = user_programs[:5]

        last_achieved = None
        if 'achieved' in user_achievements:
            last_achieved = user_achievements['achieved'][-1]

        # Todo: TB -> In the near future: add achievement for user visiting their own profile

        return render_template('public-page.html', user_info=user_public_info,
                               favourite_program=favourite_program,
                               programs=user_programs,
                               last_achieved=last_achieved,
                               user_achievements=user_achievements)
    return utils.error_page(error=404, ui_message='user_not_private')


@app.route('/invite/<code>', methods=['GET'])
def teacher_invitation(code):
    user = current_user()
    lang = g.lang

    if os.getenv('TEACHER_INVITE_CODE') != code:
        return utils.error_page(error=404, ui_message='invalid_teacher_invitation_code')
    if not user['username']:
        return render_template('teacher-invitation.html')

    update_is_teacher(user)

    session['welcome-teacher'] = True
    url = request.url.replace(f'/invite/{code}', '/for-teachers')
    return redirect(url)

# *** AUTH ***

from website import auth
auth.routes(app, DATABASE)

# *** PROGRAMS BACKEND ***

from website import programs
programs.routes(app, DATABASE, ACHIEVEMENTS)

# *** TEACHER BACKEND ***

from website import teacher
teacher.routes(app, DATABASE, ACHIEVEMENTS)

# *** ADMIN BACKEND ***

from website import admin
admin.routes(app, DATABASE)

# *** ACHIEVEMENTS BACKEND ***

ACHIEVEMENTS.routes(app, DATABASE)

# *** QUIZ BACKEND ***

from website import quiz
quiz.routes(app, DATABASE, ACHIEVEMENTS)

# *** STATISTICS ***

from website import statistics
statistics.routes(app, DATABASE)

# *** START SERVER ***

def on_server_start():
    """Called just before the server is started, both in developer mode and on Heroku.

    Use this to initialize objects, dependencies and connections.
    """
    pass


if __name__ == '__main__':
    # Start the server on a developer machine. Flask is initialized in DEBUG mode, so it
    # hot-reloads files. We also flip our own internal "debug mode" flag to True, so our
    # own file loading routines also hot-reload.
    utils.set_debug_mode(not os.getenv('NO_DEBUG_MODE'))

    # If we are running in a Python debugger, don't use flasks reload mode. It creates
    # subprocesses which make debugging harder.
    is_in_debugger = sys.gettrace() is not None

    on_server_start()

    # Threaded option enables multiple instances for multiple user access support
    app.run(threaded=True, debug=not is_in_debugger, port=config['port'], host="0.0.0.0")

    # See `Procfile` for how the server is started on Heroku.
