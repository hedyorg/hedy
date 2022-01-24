# coding=utf-8
import sys
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
import uuid
from ruamel import yaml
from flask_commonmark import Commonmark
from werkzeug.urls import url_encode
from config import config
from website.auth import auth_templates, current_user, login_user_from_token_cookie, requires_login, is_admin, \
    is_teacher, update_is_teacher, pick
from utils import timems, load_yaml_rt, dump_yaml_rt, version, is_debug_mode
import utils
import textwrap

# app.py
from flask import Flask, request, jsonify, session, abort, g, redirect, Response, make_response, url_for, Markup
from flask_helpers import render_template
from flask_compress import Compress

# Hedy-specific modules
import hedy_content
import hedyweb
from website import querylog, aws_helpers, jsonbin, translating, ab_proxying, cdn, database, achievements
from website.log_fetcher import log_fetcher
import quiz

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

# Define and load all available language data
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
    'fy': 'Frysk'
}
# Define fall back languages for adventures
FALL_BACK_ADVENTURE = {
    'fy': 'nl',
    'pt_br': 'pt_pt'
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
        all_adventures.append({
            'short_name': short_name,
            'name': adventure['name'],
            'image': adventure.get('image', None),
            'default_save_name': adventure['default_save_name'],
            'text': adventure['levels'][level].get('story_text', 'No Story Text'),
            'start_code': adventure['levels'][level].get('start_code', ''),
            'loaded_program': '' if not loaded_programs.get(short_name) else {
                'name': loaded_programs.get(short_name)['name'],
                'code': loaded_programs.get(short_name)['code']
            }
        })
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
    session_id()
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
        if 'language' in user_data:
            if user_data['language'] in ALL_LANGUAGES.keys():
                g.lang = session['lang'] = user_data['language']
        data['user_data'] = user_data
        if 'classes' in user_data:
            data['user_classes'] = DATABASE.get_student_classes(user.get('username'))
        user_achievements = DATABASE.achievements_by_username(user.get('username'))
        if user_achievements:
            data['user_achievements'] = user_achievements
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

    querylog.log_value(level=level, lang=lang, session_id=session_id(), username=username)

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
        'session': session_id(),
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

    querylog.log_value(level=level, lang=lang, session_id=session_id(), username=username)

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
        'session': session_id(),
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


def transpile_add_stats(code, level, lang_):
    username = current_user()['username'] or None
    try:
        result = hedy.transpile(code, level, lang_)
        add_program_stats(username, level)
        return result
    except Exception as ex:
        add_program_stats(username, level, get_class_name(ex))
        raise


def get_class_name(i):
    if i is not None:
        return str(i.__class__.__name__)
    return i


def add_program_stats(username, level, ex=None):
    try:
        DATABASE.add_program_stats('@all', level, ex)
        if username:
            DATABASE.add_program_stats(username, level, ex)
    except Exception as ex:
        # Adding stats should not cause failure. Log and continue.
        querylog.log_value(server_error=ex)


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
        'session': session_id(),
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
        session=session_id(),
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
        url = request.url.replace('/my-achievements', '/login')
        return redirect(url, code=302)

    achievement_translations = hedyweb.PageTranslations('achievements').get_page_translations(g.lang)

    return render_template('achievements.html', page_title=hedyweb.get_page_title('achievements'),
                           template_achievements=achievement_translations, current_page='my-profile')

def programs_page(request):
    user = current_user()
    username = user['username']
    if not username:
        # redirect users to /login if they are not logged in
        url = request.url.replace('/programs', '/login')
        return redirect(url, code=302)

    from_user = request.args.get('user') or None
    if from_user and not is_admin(user):
        if not is_teacher(user):
            return utils.error_page(error=403, ui_message='not_teacher')
        students = DATABASE.get_teacher_students(username)
        if from_user not in students:
            return utils.error_page(error=403, ui_message='not_enrolled')

    adventures = load_adventure_for_language(g.lang)

    result = DATABASE.programs_for_user(from_user or username)
    public_profile = DATABASE.get_public_profile_settings(username)
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
                           public_profile=public_profile)


@app.route('/logs/query', methods=['POST'])
def query_logs():
    user = current_user()
    if not is_admin(user):
        return utils.error_page(error=403, ui_message='unauthorized')

    body = request.json
    if body is not None and not isinstance(body, dict):
        return 'body must be an object', 400

    (exec_id, status) = log_fetcher.query(body)
    response = {'query_status': status, 'query_execution_id': exec_id}
    return jsonify(response)


@app.route('/logs/results', methods=['GET'])
def get_log_results():
    query_execution_id = request.args.get('query_execution_id', default=None, type=str)
    next_token = request.args.get('next_token', default=None, type=str)

    user = current_user()
    if not is_admin(user):
        return utils.error_page(error=403, ui_message='unauthorized')

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


@app.route('/quiz/start/<int:level>', methods=['GET'])
def get_quiz_start(level):
    if not is_quiz_enabled():
        return quiz_disabled_error()

    g.prefix = '/hedy'

    # A unique identifier to record the answers under
    session['quiz-attempt-id'] = uuid.uuid4().hex

    # Sets the values of total_score and correct on the beginning of the quiz at 0
    session['total_score'] = 0
    session['correct_answer'] = 0

    return render_template('startquiz.html', level=level, next_assignment=1)


# Quiz mode
# Fill in the filename as source
@app.route('/quiz/quiz_questions/<int:level_source>/<int:question_nr>', methods=['GET'], defaults={'attempt': 1})
@app.route('/quiz/quiz_questions/<int:level_source>/<int:question_nr>/<int:attempt>', methods=['GET'])
def get_quiz(level_source, question_nr, attempt):
    if not is_quiz_enabled():
        return quiz_disabled_error()

    # If we don't have an attempt ID yet, redirect to the start page
    if not session.get('quiz-attempt-id'):
        return redirect(url_for('get_quiz_start', level=level_source, lang=g.lang))

    # Reading the yaml file
    questions = quiz.quiz_data_file_for(g.lang, level_source)
    if not questions:
        return no_quiz_data_error()

    # set globals
    g.prefix = '/hedy'

    question_status = 'start' if attempt == 1 else 'false'

    if question_nr > quiz.highest_question(questions):
        return redirect(url_for('quiz_finished', level=level_source, lang=g.lang))

    question = quiz.get_question(questions, question_nr)
    question_obj = quiz.question_options_for(question)

    # Read from session. Don't remove yet: If the user refreshes the
    # page here, we want to keep this same information in place (otherwise
    # if we removed from the session here it would be gone on page refresh).
    chosen_option = session.get('chosenOption', None)
    wrong_answer_hint = session.get('wrong_answer_hint', None)

    return render_template('quiz_question.html',
                           level_source=level_source,
                           questionStatus=question_status,
                           questions=questions,
                           question_options=question_obj,
                           chosen_option=chosen_option,
                           wrong_answer_hint=wrong_answer_hint,
                           question=question,
                           question_nr=question_nr,
                           correct=session.get('correct_answer'),
                           attempt=attempt,
                           is_last_attempt=attempt == quiz.MAX_ATTEMPTS,
                           lang=g.lang)


@app.route('/quiz/finished/<int:level>', methods=['GET'])
def quiz_finished(level):
    """Results page at the end of the quiz."""
    if not is_quiz_enabled():
        return quiz_disabled_error()

    # Reading the yaml file
    questions = quiz.quiz_data_file_for(g.lang, level)
    if not questions:
        return no_quiz_data_error()

    # set globals
    g.prefix = '/hedy'

    achievement = ACHIEVEMENTS.add_single_achievement(current_user()['username'], "next_question")
    if round(session.get('total_score', 0) / quiz.max_score(questions) * 100) == 100:
        if achievement:
            achievement.append(ACHIEVEMENTS.add_single_achievement(current_user()['username'], "quiz_master")[0])
        else:
            achievement = ACHIEVEMENTS.add_single_achievement(current_user()['username'], "quiz_master")
    if achievement:
        achievement = json.dumps(achievement)

    print(achievement)

    return render_template('endquiz.html', correct=session.get('correct_answer', 0),
                           total_score=round(session.get('total_score', 0) / quiz.max_score(questions) * 100),
                           level_source=level,
                           achievement=achievement,
                           level=int(level) + 1,
                           questions=questions,
                           next_assignment=1)


@app.route('/quiz/submit_answer/<int:level_source>/<int:question_nr>/<int:attempt>', methods=["POST"])
def submit_answer(level_source, question_nr, attempt):
    if not is_quiz_enabled():
        return quiz_disabled_error()

    # If we don't have an attempt ID yet, redirect to the start page
    if not session.get('quiz-attempt-id'):
        return redirect(url_for('get_quiz_start', level=level_source, lang=g.lang))

    # Get the chosen option from the request form with radio buttons
    # This looks like '1-B' or '5-C' or what have you.
    #
    # The number should always be the same as 'question_nr', or otherwise
    # be 'question_nr - 1', so is unnecessary. But we'll leave it here for now.
    chosen_option = request.form["radio_option"]
    chosen_option = chosen_option.split('-')[1]

    # Reading the yaml file
    questions = quiz.quiz_data_file_for(g.lang, level_source)
    if not questions:
        return no_quiz_data_error()

    # Convert question_nr to an integer
    q_nr = int(question_nr)

    # Convert the corresponding chosen option to the index of an option
    question = quiz.get_question(questions, q_nr)

    is_correct = quiz.is_correct_answer(question, chosen_option)

    session['chosenOption'] = chosen_option
    if not is_correct:
        session['wrong_answer_hint'] = quiz.get_hint(question, chosen_option)
    else:
        # Correct answer -- make sure there is no hint on the next display page
        session.pop('wrong_answer_hint', None)

    # Store the answer in the database. If we don't have a username,
    # use the session ID as a username.
    username = current_user()['username'] or f'anonymous:{session_id()}'

    DATABASE.record_quiz_answer(session['quiz-attempt-id'],
                                username=username,
                                level=level_source,
                                is_correct=is_correct,
                                question_number=question_nr,
                                answer=chosen_option)

    if is_correct:
        score = quiz.correct_answer_score(question)
        session['total_score'] = session.get('total_score', 0) + score
        session['correct_answer'] = session.get('correct_answer', 0) + 1

        return redirect(url_for('quiz_feedback', level_source=level_source, question_nr=question_nr, lang=g.lang))

    # Not a correct answer. You can try again if you haven't hit your max attempts yet.
    if attempt >= quiz.MAX_ATTEMPTS:
        return redirect(url_for('quiz_feedback', level_source=level_source, question_nr=question_nr, lang=g.lang))

    # Redirect to the display page to try again
    return redirect(url_for('get_quiz', chosen_option=chosen_option, level_source=level_source, question_nr=question_nr,
                            attempt=attempt + 1, lang=g.lang))


@app.route('/quiz/feedback/<int:level_source>/<int:question_nr>', methods=["GET"])
def quiz_feedback(level_source, question_nr):
    if not is_quiz_enabled():
        return quiz_disabled_error()

    # If we don't have an attempt ID yet, redirect to the start page
    if not session.get('quiz-attempt-id'):
        return redirect(url_for('get_quiz_start', level=level_source, lang=g.lang))

    # Reading the yaml file
    questions = quiz.quiz_data_file_for(g.lang, level_source)
    if not questions:
        return no_quiz_data_error()

    question = quiz.get_question(questions, question_nr)

    # Read from session and remove the variables from it (this is the
    # feedback page, the previous answers will never apply anymore).
    chosen_option = session.pop('chosenOption', None)
    wrong_answer_hint = session.pop('wrong_answer_hint', None)

    answer_was_correct = quiz.is_correct_answer(question, chosen_option)

    index_option = quiz.index_from_letter(chosen_option)
    correct_option = quiz.get_correct_answer(question)

    question_options = quiz.question_options_for(question)

    return render_template('feedback.html', question=question,
                           questions=questions,
                           question_options=question_options,
                           level_source=level_source,
                           question_nr=question_nr,
                           correct=session.get('correct_answer'),
                           answer_was_correct=answer_was_correct,
                           wrong_answer_hint=wrong_answer_hint,
                           index_option=index_option,
                           correct_option=correct_option,
                           lang=g.lang)


def is_quiz_enabled():
    return config.get('quiz-enabled')


def quiz_disabled_error():
    return utils.error_page(error=404, page_error='Hedy quiz disabled!', menu=False, iframe=True)


def no_quiz_data_error():
    return utils.error_page(error=404, page_error='No quiz data found for this level', menu=False, iframe=True)


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

    adventures, restrictions = DATABASE.get_student_restrictions(load_adventures_per_level(g.lang, level),
                                                                 current_user()['username'], level)
    level_defaults_for_lang = LEVEL_DEFAULTS[g.lang]

    if level not in level_defaults_for_lang.levels or restrictions['hide_level']:
        return utils.error_page(error=404, ui_message='no_such_level')
    defaults = level_defaults_for_lang.get_defaults_for_level(level)
    max_level = level_defaults_for_lang.max_level()

    return hedyweb.render_code_editor_with_tabs(
        level_defaults=defaults,
        max_level=max_level,
        level_number=level,
        version=version(),
        adventures=adventures,
        restrictions=restrictions,
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

    if page == 'programs':
        return programs_page(request)

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
        print(for_teacher_translations)
        if is_teacher(user):
            welcome_teacher = session.get('welcome-teacher') or False
            session.pop('welcome-teacher', None)
            teacher_classes = [] if not current_user()['username'] else DATABASE.get_teacher_classes(
                current_user()['username'], True)
            return render_template('for-teachers.html', current_page='my-profile',
                                   page_title=hedyweb.get_page_title(page),
                                   content=for_teacher_translations, teacher_classes=teacher_classes,
                                   welcome_teacher=welcome_teacher)
        else:
            return utils.error_page(error=403, ui_message='not_teacher')

    if page == 'stats':
        if not is_admin(current_user()):
            return utils.error_page(error=403, ui_message='unauthorized')
        return render_template('admin-stats.html')

    requested_page = hedyweb.PageTranslations(page)
    if not requested_page.exists():
        abort(404)

    main_page_translations = requested_page.get_page_translations(g.lang)
    return render_template('main-page.html', page_title=hedyweb.get_page_title('start'),
                           content=main_page_translations)


@app.route('/explore', methods=['GET'])
def explore():
    level = request.args.get('level', default=None, type=str)
    adventure = request.args.get('adventure', default=None, type=str)

    level = None if level == "null" else level
    adventure = None if adventure == "null" else adventure

    if level or adventure:
        programs = DATABASE.get_filtered_explore_programs(level, adventure)
    else:
        programs = DATABASE.get_all_explore_programs()

    for program in programs:
        program['code'] = "\n".join(program['code'].split("\n")[:4])

    adventures = None
    if hedy_content.Adventures(session['lang']).has_adventures():
        adventures = hedy_content.Adventures(session['lang']).get_adventure_keyname_name_levels()

    return render_template('explore.html', programs=programs,
                           filtered_level=level,
                           filtered_adventure=adventure,
                           max_level=hedy.HEDY_MAX_LEVEL,
                           adventures=adventures,
                           page_title=hedyweb.get_page_title('explore'),
                           current_page='explore')


@app.route('/admin', methods=['GET'])
def get_admin_page():
    if not utils.is_testing_request(request) and not is_admin(current_user()):
        return 'unauthorized', 403

    category = request.args.get('filter', default=None, type=str)
    category = None if category == "null" else category

    substring = request.args.get('substring', default=None, type=str)
    start_date = request.args.get('start', default=None, type=str)
    end_date = request.args.get('end', default=None, type=str)

    substring = None if substring == "null" else substring
    start_date = None if start_date == "null" else start_date
    end_date = None if end_date == "null" else end_date

    filtering = False
    if substring or start_date or end_date or category == "all":
        filtering = True

    # After hitting 1k users, it'd be wise to add pagination.
    users = DATABASE.all_users(filtering)
    userdata =[]
    fields =['username', 'email', 'birth_year', 'country', 'gender', 'created', 'last_login', 'verification_pending', 'is_teacher', 'program_count', 'prog_experience', 'experience_languages']

    for user in users:
        data = pick(user, *fields)
        data['email_verified'] = not bool(data['verification_pending'])
        data['is_teacher'] = bool(data['is_teacher'])
        data['created'] = utils.datetotimeordate (utils.mstoisostring(data['created'])) if data['created'] else '?'
        if filtering and category == "email":
            if substring not in data['email']:
                continue
        if filtering and category == "created":
            if (start_date and utils.datetotimeordate(start_date) >= data['created']) or (end_date and utils.datetotimeordate(end_date) <= data['created']):
                continue
        if data['last_login']:
            data['last_login'] = utils.datetotimeordate(utils.mstoisostring(data['last_login'])) if data['last_login'] else '?'
            if filtering and category == "last_login":
                if (start_date and utils.datetotimeordate(start_date) >= data['last_login']) or (end_date and utils.datetotimeordate(end_date) <= data['last_login']):
                    continue
        userdata.append(data)

    userdata.sort(key=lambda user: user['created'], reverse=True)
    counter = 1
    for user in userdata:
        user['index'] = counter
        counter = counter + 1

    return render_template('admin.html', users=userdata, page_title=hedyweb.get_page_title('admin'),
                           filter=category, start_date=start_date, end_date=end_date, email_filter=substring,
                           program_count=DATABASE.all_programs_count(), user_count=DATABASE.all_users_count())


@app.route('/change_language', methods=['POST'])
def change_language():
    body = request.json
    session['lang'] = body.get('lang')
    return jsonify({'succes': 200})


def session_id():
    """Returns or sets the current session ID."""
    if 'session_id' not in session:
        if os.getenv('IS_TEST_ENV') and 'X-session_id' in request.headers:
            session['session_id'] = request.headers['X-session_id']
        else:
            session['session_id'] = uuid.uuid4().hex
    return session['session_id']


@app.template_global()
def current_language():
    return make_lang_obj(g.lang)


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


@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, url_encode(args))


def no_none_sense(d):
    """Remove all None values from a dict."""
    return {k: v for k, v in d.items() if v is not None}


def split_markdown_front_matter(md):
    parts = re.split('^---', md, 1, re.M)
    if len(parts) == 1:
        return {}, md
    # safe_load returns 'None' if the string is empty
    front_matter = yaml.safe_load(parts[0]) or {}
    if not isinstance(front_matter, dict):
        # There was some kind of parsing error
        return {}, md

    return front_matter, parts[1]


def render_main_menu(current_page):
    """Render a list of(caption, href, selected, color) from the main menu."""
    return [dict(
        caption=item.get(g.lang, item.get('en', '???')),
        href='/' + item['_'],
        selected=(current_page == item['_']),
        accent_color=item.get('accent_color', 'white'),
        short_name=item['_']
    ) for item in main_menu_json['nav']]


# *** PROGRAMS ***

@app.route('/programs_list', methods=['GET'])
@requires_login
def list_programs(user):
    return {'programs': DATABASE.programs_for_user(user['username']).records}


@app.route('/programs/delete/', methods=['POST'])
@requires_login
def delete_program(user):
    body = request.json
    if not isinstance(body.get('id'), str):
        return 'program id must be a string', 400

    result = DATABASE.program_by_id(body['id'])

    if not result or result['username'] != user['username']:
        return "", 404
    DATABASE.delete_program_by_id(body['id'])
    DATABASE.increase_user_program_count(user['username'], -1)

    # This only happens in the situation were a user deletes their favourite program -> Delete from public profile
    public_profile = DATABASE.get_public_profile_settings(current_user()['username'])
    if public_profile and 'favourite_program' in public_profile and public_profile['favourite_program'] == body['id']:
        DATABASE.set_favourite_program(user['username'], None)

    achievement = ACHIEVEMENTS.add_single_achievement(user['username'], "do_you_have_copy")
    if achievement:
        return {'achievement': achievement}, 200
    return {}, 200


@app.route('/programs/duplicate-check', methods=['POST'])
@requires_login
def check_duplicate_program(user):
    body = request.json
    if not isinstance(body, dict):
        return 'body must be an object', 400
    if not isinstance(body.get('name'), str):
        return 'name must be a string', 400

    programs = DATABASE.programs_for_user(user['username'])
    for program in programs:
        if program['name'] == body['name']:
            return jsonify({'duplicate': True})
    return jsonify({'duplicate': False})


@app.route('/programs', methods=['POST'])
@requires_login
def save_program(user):
    body = request.json
    if not isinstance(body, dict):
        return 'body must be an object', 400
    if not isinstance(body.get('code'), str):
        return 'code must be a string', 400
    if not isinstance(body.get('name'), str):
        return 'name must be a string', 400
    if not isinstance(body.get('level'), int):
        return 'level must be an integer', 400
    if 'adventure_name' in body:
        if not isinstance(body.get('adventure_name'), str):
            return 'if present, adventure_name must be a string', 400

    # We check if a program with a name `xyz` exists in the database for the username.
    # It'd be ideal to search by username & program name, but since DynamoDB doesn't allow searching for two indexes at the same time, this would require to create a special index to that effect, which is cumbersome.
    # For now, we bring all existing programs for the user and then search within them for repeated names.
    programs = DATABASE.programs_for_user(user['username']).records
    program_id = uuid.uuid4().hex
    overwrite = False
    for program in programs:
        if program['name'] == body['name']:
            overwrite = True
            program_id = program['id']
            break

    stored_program = {
        'id': program_id,
        'session': session_id(),
        'date': timems(),
        'lang': g.lang,
        'version': version(),
        'level': body['level'],
        'code': body['code'],
        'name': body['name'],
        'username': user['username']
    }

    if 'adventure_name' in body:
        stored_program['adventure_name'] = body['adventure_name']

    DATABASE.store_program(stored_program)
    if not overwrite:
        DATABASE.increase_user_program_count(user['username'])
    DATABASE.increase_user_save_count(user['username'])
    ACHIEVEMENTS.increase_count("saved")

    if ACHIEVEMENTS.verify_save_achievements(user['username'], 'adventure_name' in body and len(body['adventure_name']) > 2):
        return jsonify({'name': body['name'], 'id': program_id, "achievements": ACHIEVEMENTS.get_earned_achievements()})
    return jsonify({'name': body['name'], 'id': program_id})


@app.route('/programs/share', methods=['POST'])
@requires_login
def share_unshare_program(user):
    body = request.json
    if not isinstance(body, dict):
        return 'body must be an object', 400
    if not isinstance(body.get('id'), str):
        return 'id must be a string', 400
    if not isinstance(body.get('public'), bool):
        return 'public must be a boolean', 400

    result = DATABASE.program_by_id(body['id'])
    if not result or result['username'] != user['username']:
        return 'No such program!', 404

    #This only happens in the situation were a user un-shares their favourite program -> Delete from public profile
    public_profile = DATABASE.get_public_profile_settings(current_user()['username'])
    if public_profile and 'favourite_program' in public_profile and public_profile['favourite_program'] == body['id']:
        DATABASE.set_favourite_program(user['username'], None)

    DATABASE.set_program_public_by_id(body['id'], bool(body['public']))
    achievement = ACHIEVEMENTS.add_single_achievement(user['username'], "sharing_is_caring")
    if achievement:
        return jsonify({'achievement': achievement, 'id': body['id']})
    return jsonify({'id': body['id']})


@app.route('/programs/submit', methods=['POST'])
@requires_login
def submit_program(user):
    body = request.json
    if not isinstance(body, dict):
        return 'body must be an object', 400
    if not isinstance(body.get('id'), str):
        return 'id must be a string', 400

    result = DATABASE.program_by_id(body['id'])
    if not result or result['username'] != user['username']:
        return 'No such program!', 404

    DATABASE.submit_program_by_id(body['id'])
    DATABASE.increase_user_submit_count(user['username'])
    ACHIEVEMENTS.increase_count("submitted")

    if ACHIEVEMENTS.verify_submit_achievements(user['username']):
        return jsonify({"achievements": ACHIEVEMENTS.get_earned_achievements()})
    return jsonify({})

@app.route('/programs/set_favourite', methods=['POST'])
@requires_login
def set_favourite_program(user):
    body = request.json
    if not isinstance(body, dict):
        return 'body must be an object', 400
    if not isinstance(body.get('id'), str):
        return 'id must be a string', 400

    result = DATABASE.program_by_id(body['id'])
    if not result or result['username'] != user['username']:
        return 'No such program!', 404

    DATABASE.set_favourite_program(user['username'], body['id'])
    return jsonify({})

@app.route('/translate/<source>/<target>')
def translate_fromto(source, target):
    source_adventures = YamlFile.for_file(f'coursedata/adventures/{source}.yaml').to_dict()
    source_levels = YamlFile.for_file(f'coursedata/level-defaults/{source}.yaml').to_dict()
    source_texts = YamlFile.for_file(f'coursedata/texts/{source}.yaml').to_dict()
    source_keywords = YamlFile.for_file(f'coursedata/keywords/{source}.yaml').to_dict()

    target_adventures = YamlFile.for_file(f'coursedata/adventures/{target}.yaml').to_dict()
    target_levels = YamlFile.for_file(f'coursedata/level-defaults/{target}.yaml').to_dict()
    target_texts = YamlFile.for_file(f'coursedata/texts/{target}.yaml').to_dict()
    target_keywords = YamlFile.for_file(f'coursedata/keywords/{target}.yaml').to_dict()

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
    filename = path.join('coursedata', request.form['file'])
    # The file MUST point to something inside our 'coursedata' directory
    filepath = path.abspath(filename)
    expected_path = path.abspath('coursedata')
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
    user = DATABASE.user_by_username(username.lower())
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

# *** TEACHER BACKEND

from website import teacher

teacher.routes(app, DATABASE, ACHIEVEMENTS)

# *** ACHIEVEMENTS BACKEND

ACHIEVEMENTS.routes(app, DATABASE)

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
