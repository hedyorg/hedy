# coding=utf-8
from website import auth
from website import statistics
from website import quiz
from website import admin
from website import teacher
from website import programs
import textwrap
import utils
from utils import timems, load_yaml_rt, dump_yaml_rt, version, is_debug_mode
from website.log_fetcher import log_fetcher
from website.auth import current_user, login_user_from_token_cookie, requires_login, is_admin, is_teacher, update_is_teacher
from website.yaml_file import YamlFile
from website import querylog, aws_helpers, jsonbin, translating, ab_proxying, cdn, database, achievements
import hedy_translation
from hedy_content import COUNTRIES, ALL_LANGUAGES, ALL_KEYWORD_LANGUAGES, ADVENTURE_ORDER
import hedyweb
import hedy_content
from flask_babel import gettext
from flask_babel import Babel, refresh
from flask_compress import Compress
from flask_helpers import render_template
from flask import Flask, request, jsonify, session, abort, g, redirect, Response, make_response, Markup
from config import config
from werkzeug.urls import url_encode
from babel import Locale
from flask_commonmark import Commonmark
import traceback
import re
import logging
import json
import hedy
import collections
import datetime
import sys

if (sys.version_info.major < 3 or sys.version_info.minor < 7):
    print('Hedy requires Python 3.7 or newer to run. However, your version of Python is',
          '.'.join([str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro)]))
    quit()

# Set the current directory to the root Hedy folder
import os
from os import path
os.chdir(os.path.join(os.getcwd(), __file__.replace(
    os.path.basename(__file__), '')))

# Setting up Flask and babel (web and translations)
app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False  # Ignore trailing slashes in URLs
babel = Babel(app)

COMMANDS = collections.defaultdict(hedy_content.NoSuchCommand)
for lang in ALL_LANGUAGES.keys():
    COMMANDS[lang] = hedy_content.Commands(lang)

ADVENTURES = collections.defaultdict(hedy_content.NoSuchAdventure)
for lang in ALL_LANGUAGES.keys():
    ADVENTURES[lang] = hedy_content.Adventures(lang)

QUIZZES = collections.defaultdict(hedy_content.NoSuchQuiz)
for lang in ALL_LANGUAGES.keys():
    QUIZZES[lang] = hedy_content.Quizzes(lang)

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
# numerals list generated from: https://replit.com/@mevrHermans/multilangnumerals

NORMAL_PREFIX_CODE = textwrap.dedent("""\
    # coding=utf8
    import random, time
    global int_saver
    int_saver = int
    def int(s):
      if isinstance(s, str):
        numerals_dict = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '𑁦': '0', '𑁧': '1', '𑁨': '2', '𑁩': '3', '𑁪': '4', '𑁫': '5', '𑁬': '6', '𑁭': '7', '𑁮': '8', '𑁯': '9', '०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9', '૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4', '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9', '੦': '0', '੧': '1', '੨': '2', '੩': '3', '੪': '4', '੫': '5', '੬': '6', '੭': '7', '੮': '8', '੯': '9', '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9', '೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4', '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9', '୦': '0', '୧': '1', '୨': '2', '୩': '3', '୪': '4', '୫': '5', '୬': '6', '୭': '7', '୮': '8', '୯': '9', '൦': '0', '൧': '1', '൨': '2', '൩': '3', '൪': '4', '൫': '5', '൬': '6', '൭': '7', '൮': '8', '൯': '9', '௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9', '౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4', '౫': '5', '౬': '6', '౭': '7', '౮': '8', '౯': '9', '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4', '၅': '5', '၆': '6', '၇': '7', '၈': '8', '၉': '9', '༠': '0', '༡': '1', '༢': '2', '༣': '3', '༤': '4', '༥': '5', '༦': '6', '༧': '7', '༨': '8', '༩': '9', '᠐': '0', '᠑': '1', '᠒': '2', '᠓': '3', '᠔': '4', '᠕': '5', '᠖': '6', '᠗': '7', '᠘': '8', '᠙': '9', '០': '0', '១': '1', '២': '2', '៣': '3', '៤': '4', '៥': '5', '៦': '6', '៧': '7', '៨': '8', '៩': '9', '๐': '0', '๑': '1', '๒': '2', '๓': '3', '๔': '4', '๕': '5', '๖': '6', '๗': '7', '๘': '8', '๙': '9', '໐': '0', '໑': '1', '໒': '2', '໓': '3', '໔': '4', '໕': '5', '໖': '6', '໗': '7', '໘': '8', '໙': '9', '꧐': '0', '꧑': '1', '꧒': '2', '꧓': '3', '꧔': '4', '꧕': '5', '꧖': '6', '꧗': '7', '꧘': '8', '꧙': '9', '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9', '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9', '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0'}
        latin_numerals = ''.join([numerals_dict.get(letter, letter) for letter in s])
        return int_saver(latin_numerals)
      return(int_saver(s))
""")


def load_adventures_per_level(level):
    loaded_programs = {}
    # If user is logged in, we iterate their programs that belong to the current level. Out of these, we keep the latest created program for both the level mode(no adventure) and for each of the adventures.
    if current_user()['username']:
        user_programs = DATABASE.level_programs_for_user(
            current_user()['username'], level)
        for program in user_programs:
            program_key = 'default' if not program.get(
                'adventure_name') else program['adventure_name']
            if program_key not in loaded_programs or loaded_programs[program_key]['date'] < program['date']:
                loaded_programs[program_key] = program

    all_adventures = []
    adventures = ADVENTURES[g.lang].get_adventures(g.keyword_lang)

    for short_name, adventure in adventures.items():
        if level not in adventure['levels']:
            continue
        # end adventure is the quiz
        # if quizzes are not enabled, do not load it
        # Todo TB -> Is this still relevant? Teachers can simply "disable" adventures in customizations!
        if short_name == 'end' and not config['quiz-enabled']:
            continue
        current_adventure = {
            'short_name': short_name,
            'name': adventure['name'],
            'image': adventure.get('image', None),
            'default_save_name': adventure.get('default_save_name', adventure['name']),
            'text': adventure['levels'][level].get('story_text', ""),
            'example_code': adventure['levels'][level].get('example_code', ""),
            'start_code': adventure['levels'][level].get('start_code', ""),
            'loaded_program': '' if not loaded_programs.get(short_name) else {
                'name': loaded_programs.get(short_name)['name'],
                'code': loaded_programs.get(short_name)['code']
            }
        }
        # Sometimes we have multiple text and example_code -> iterate these and add as well!
        extra_stories = []
        for i in range(2, 10):
            extra_story = {}
            if adventure['levels'][level].get('story_text_' + str(i)):
                extra_story['text'] = adventure['levels'][level].get(
                    'story_text_' + str(i))
                if adventure['levels'][level].get('example_code_' + str(i)):
                    extra_story['example_code'] = adventure['levels'][level].get(
                        'example_code_' + str(i))
                extra_stories.append(extra_story)
            else:
                break
        current_adventure['extra_stories'] = extra_stories
        all_adventures.append(current_adventure)
    return all_adventures


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)-8s: %(message)s')

# Return the session language, if not: return best match


@babel.localeselector
def get_locale():
    return session.get("lang", request.accept_languages.best_match(ALL_LANGUAGES.keys(), 'en'))


cdn.Cdn(app, os.getenv('CDN_PREFIX'), os.getenv('HEROKU_SLUG_COMMIT', 'dev'))


@app.before_request
def before_request_begin_logging():
    """Initialize the query logging.

    This needs to happen as one of the first things, as the database calls
    etc. depend on it.
    """
    path = (str(request.path) + '?' + str(request.query_string)
            ) if request.query_string else str(request.path)
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
    if utils.is_testing_request(request) and os.getenv('IS_TEST_ENV'):
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
        raise RuntimeError(
            'The SECRET KEY must be provided for non-dev environments.')

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
querylog.LOG_QUEUE.set_transmitter(
    aws_helpers.s3_querylog_transmitter_from_env())


@app.before_request
def setup_language():
    # Determine the user's requested language code.
    #
    # If not in the request parameters, use the browser's accept-languages
    # header to do language negotiation.
    if 'lang' not in session:
        session['lang'] = request.accept_languages.best_match(
            ALL_LANGUAGES.keys(), 'en')

    g.lang = session['lang']
    if 'keyword_lang' not in session:
        if g.lang in ALL_KEYWORD_LANGUAGES.keys():
            g.keyword_lang = g.lang
        else:
            g.keyword_lang = "en"
    else:
        g.keyword_lang = session['keyword_lang']

    # Set the page direction -> automatically set it to "left-to-right"
    # Switch to "right-to-left" if one of the language is rtl according to Locale (from Babel) settings.
    # This is the only place to expand / shrink the list of RTL languages -> front-end is fixed based on this value
    g.dir = "ltr"
    if Locale(g.lang).text_direction in ["ltr", "rtl"]:
        g.dir = Locale(g.lang).text_direction

    # Check that requested language is supported, otherwise return 404
    if g.lang not in ALL_LANGUAGES.keys():
        return "Language " + g.lang + " not supported", 404


if utils.is_heroku() and not os.getenv('HEROKU_RELEASE_CREATED_AT'):
    logging.warning(
        'Cannot determine release; enable Dyno metadata by running "heroku labs:enable runtime-dyno-metadata -a <APP_NAME>"')


# A context processor injects variables in the context that are available to all templates.
@app.context_processor
def enrich_context_with_user_info():
    user = current_user()
    data = {'username': user.get('username', ''),
            'is_teacher': is_teacher(user)}
    return data


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
    ab_proxying.ABProxying(app, os.getenv(
        'PROXY_TO_TEST_HOST'), app.config['SECRET_KEY'])


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

    error_check = False
    if 'error_check' in body:
        error_check = True

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

    querylog.log_value(level=level, lang=lang,
                       session_id=utils.session_id(), username=username)

    try:
        with querylog.log_time('transpile'):

            try:
                transpile_result = transpile_add_stats(code, level, lang)
                if username:
                    DATABASE.increase_user_run_count(username)
                    ACHIEVEMENTS.increase_count("run")
            except hedy.exceptions.FtfyException as ex:
                translated_error = translate_error(ex.error_code, ex.arguments)
                if type(ex) is hedy.exceptions.InvalidSpaceException:
                    response['Warning'] = translated_error
                else:
                    response['Error'] = translated_error
                response['Location'] = ex.error_location
                response['FixedCode'] = ex.fixed_code
                transpile_result = ex.fixed_result
                exception = ex
            except hedy.exceptions.UnquotedEqualityCheck as ex:
                response['Error'] = translate_error(
                    ex.error_code, ex.arguments)
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
        response = hedy_error_to_response(ex)
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

    if "Error" in response and error_check:
        response["message"] = gettext('program_contains_error')
    return jsonify(response)


@app.route('/parse-by-id', methods=['POST'])
@requires_login
def parse_by_id(user):
    body = request.json
    # Validations
    if not isinstance(body, dict):
        return 'body must be an object', 400
    if not isinstance(body.get('id'), str):
        return 'class id must be a string', 400

    program = DATABASE.program_by_id(body.get('id'))
    if program and program.get('username') == user['username']:
        try:
            hedy.transpile(program.get('code'), program.get(
                'level'), program.get('lang'))
            return {}, 200
        except:
            return {"error": "parsing error"}, 200
    else:
        return 'this is not your program!', 400


def transpile_add_stats(code, level, lang_):
    username = current_user()['username'] or None
    try:
        result = hedy.transpile(code, level, lang_)
        statistics.add(
            username, lambda id_: DATABASE.add_program_stats(id_, level, None))
        return result
    except Exception as ex:
        statistics.add(username, lambda id_: DATABASE.add_program_stats(
            id_, level, get_class_name(ex)))
        raise


def get_class_name(i):
    if i is not None:
        return str(i.__class__.__name__)
    return i


def hedy_error_to_response(ex):
    return {
        "Error": translate_error(ex.error_code, ex.arguments),
        "Location": ex.error_location
    }


def translate_error(code, arguments):
    arguments_that_require_translation = ['allowed_types', 'invalid_type', 'invalid_type_2', 'character_found',
                                          'concept', 'tip']
    arguments_that_require_highlighting = ['command', 'guessed_command', 'invalid_argument', 'invalid_argument_2',
                                           'variable', 'invalid_value']

    # Todo TB -> We have to find a more delicate way to fix this: returns some gettext() errors
    error_template = gettext('' + str(code))

    # some arguments like allowed types or characters need to be translated in the error message
    for k, v in arguments.items():
        if k in arguments_that_require_highlighting:
            arguments[k] = hedy.style_closest_command(v)

        if k in arguments_that_require_translation:
            if isinstance(v, list):
                arguments[k] = translate_list(v)
            else:
                arguments[k] = gettext('' + str(v))

    return error_template.format(**arguments)


def translate_list(args):
    translated_args = [gettext('' + str(a)) for a in args]
    # Deduplication is needed because diff values could be translated to the same value, e.g. int and float => a number
    translated_args = list(dict.fromkeys(translated_args))

    if len(translated_args) > 1:
        return f"{', '.join(translated_args[0:-1])}" \
               f" {gettext('or')} " \
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
    the_date = datetime.date.fromisoformat(
        vrz[:10]) if vrz else datetime.date.today()

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

    user_achievements = DATABASE.achievements_by_username(user.get('username')) or []
    achievements = ACHIEVEMENTS_TRANSLATIONS.get_translations(g.lang)

    return render_template('achievements.html', page_title=gettext('title_achievements'), translations=achievements,
                           user_achievements=user_achievements, current_page='my-profile')


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
            return utils.error_page(error=403, ui_message=gettext('not_teacher'))
        students = DATABASE.get_teacher_students(username)
        if from_user not in students:
            return utils.error_page(error=403, ui_message=gettext('not_enrolled'))

    adventures_names = hedy_content.Adventures(
        session['lang']).get_adventure_names()

    # We request our own page -> also get the public_profile settings
    public_profile = None
    if not from_user:
        public_profile = DATABASE.get_public_profile_settings(username)

    level = request.args.get('level', default=None, type=str)
    adventure = request.args.get('adventure', default=None, type=str)
    level = None if level == "null" else level
    adventure = None if adventure == "null" else adventure

    if level or adventure:
        result = DATABASE.filtered_programs_for_user(
            from_user or username, level, adventure)
    else:
        result = DATABASE.programs_for_user(from_user or username)

    programs = []
    now = timems()
    for item in result:
        date = get_user_formatted_age(now, item['date'])
        # This way we only keep the first 4 lines to show as preview to the user
        code = "\n".join(item['code'].split("\n")[:4])
        programs.append(
            {'id': item['id'],
             'code': code,
             'date': date,
             'level': item['level'],
             'name': item['name'],
             'adventure_name': item.get('adventure_name'),
             'submitted': item.get('submitted'),
             'public': item.get('public')
             }
        )

    return render_template('programs.html', programs=programs, page_title=gettext('title_programs'),
                           current_page='programs', from_user=from_user, filtered_level=level,
                           filtered_adventure=adventure, adventure_names=adventures_names,
                           public_profile=public_profile, max_level=hedy.HEDY_MAX_LEVEL)


@app.route('/logs/query', methods=['POST'])
def query_logs():
    user = current_user()
    if not is_admin(user) and not is_teacher(user):
        return utils.error_page(error=403, ui_message=gettext('unauthorized'))

    body = request.json
    if body is not None and not isinstance(body, dict):
        return 'body must be an object', 400

    class_id = body.get('class_id')
    if not is_admin(user):
        username_filter = body.get('username')
        if not class_id or not username_filter:
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        class_ = DATABASE.get_class(class_id)
        if not class_ or class_['teacher'] != user['username'] or username_filter not in class_.get('students', []):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

    (exec_id, status) = log_fetcher.query(body)
    response = {'query_status': status, 'query_execution_id': exec_id}
    return jsonify(response)


@app.route('/logs/results', methods=['GET'])
def get_log_results():
    query_execution_id = request.args.get(
        'query_execution_id', default=None, type=str)
    next_token = request.args.get('next_token', default=None, type=str)

    user = current_user()
    if not is_admin(user) and not is_teacher(user):
        return utils.error_page(error=403, ui_message=gettext('unauthorized'))

    data, next_token = log_fetcher.get_query_results(
        query_execution_id, next_token)
    response = {'data': data, 'next_token': next_token}
    return jsonify(response)


def get_user_formatted_age(now, date):
    program_age = now - date
    if program_age < 1000 * 60 * 60:
        measure = gettext('minutes')
        date = round(program_age / (1000 * 60))
    elif program_age < 1000 * 60 * 60 * 24:
        measure = gettext('hours')
        date = round(program_age / (1000 * 60 * 60))
    else:
        measure = gettext('days')
        date = round(program_age / (1000 * 60 * 60 * 24))
    age = {'time': str(date) + " " + measure}
    return gettext('ago').format(**age)


# routing to index.html
@app.route('/ontrack', methods=['GET'], defaults={'level': '1', 'program_id': None})
@app.route('/onlinemasters', methods=['GET'], defaults={'level': '1', 'program_id': None})
@app.route('/onlinemasters/<int:level>', methods=['GET'], defaults={'program_id': None})
@app.route('/space_eu', methods=['GET'], defaults={'level': '1', 'program_id': None})
@app.route('/hedy', methods=['GET'], defaults={'level': '1', 'program_id': None})
@app.route('/hedy/<level>', methods=['GET'], defaults={'program_id': None})
@app.route('/hedy/<level>/<program_id>', methods=['GET'])
def index(level, program_id):
    try:
        level = int(level)
        if level < 1 or level > hedy.HEDY_MAX_LEVEL:
            return utils.error_page(error=404, ui_message=gettext('no_such_level'))
    except:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    loaded_program = ''
    adventure_name = ''

    if program_id:
        result = DATABASE.program_by_id(program_id)
        if not result:
            return utils.error_page(error=404, ui_message=gettext('no_such_program'))

        user = current_user()
        public_program = result.get('public')
        # Verify that the program is either public, the current user is the creator, teacher or the user is admin
        if not public_program and user['username'] != result['username'] and not is_admin(user):
            if (not is_teacher(user)) or (is_teacher(user) and result['username'] not in DATABASE.get_teacher_students(user['username'])):
                return utils.error_page(error=404, ui_message=gettext(u'no_such_program'))

        loaded_program = {'code': result['code'], 'name': result['name'],
                          'adventure_name': result.get('adventure_name')}
        if 'adventure_name' in result:
            adventure_name = result['adventure_name']

    adventures = load_adventures_per_level(level)
    customizations = {}
    if current_user()['username']:
        customizations = DATABASE.get_student_class_customizations(current_user()[
                                                                   'username'])

    if 'levels' in customizations:
        available_levels = customizations['levels']
        now = timems()
        for current_level, timestamp in customizations.get('opening_dates', {}).items():
            if utils.datetotimeordate(timestamp) > utils.datetotimeordate(utils.mstoisostring(now)):
                try:
                    available_levels.remove(int(current_level))
                except:
                    print("Error: there is an openings date without a level")

    if 'levels' in customizations and level not in available_levels:
        return utils.error_page(error=403, ui_message=gettext('level_not_class'))

    commands = COMMANDS[g.lang].get_commands_for_level(level, g.keyword_lang)

    teacher_adventures = []
    for adventure in customizations.get('teacher_adventures', []):
        current_adventure = DATABASE.get_adventure(adventure)
        if current_adventure.get('level') == str(level):
            teacher_adventures.append(current_adventure)

    enforce_developers_mode = False
    if 'other_settings' in customizations and 'developers_mode' in customizations['other_settings']:
        enforce_developers_mode = True

    hide_cheatsheet = False
    if 'other_settings' in customizations and 'hide_cheatsheet' in customizations['other_settings']:
        hide_cheatsheet = True

    quiz = True if QUIZZES[g.lang].get_quiz_data_for_level(level) else False
    if 'other_settings' in customizations and 'hide_quiz' in customizations['other_settings']:
        quiz = False


    return hedyweb.render_code_editor_with_tabs(
        commands=commands,
        max_level=hedy.HEDY_MAX_LEVEL,
        level_number=level,
        version=version(),
        quiz=quiz,
        adventures=adventures,
        customizations=customizations,
        hide_cheatsheet=hide_cheatsheet,
        enforce_developers_mode=enforce_developers_mode,
        teacher_adventures=teacher_adventures,
        loaded_program=loaded_program,
        adventure_name=adventure_name)


@app.route('/hedy/<id>/view', methods=['GET'])
def view_program(id):

    user = current_user()
    result = DATABASE.program_by_id(id)

    if not result:
        return utils.error_page(error=404, ui_message=gettext('no_such_program'))

    public_program = result.get('public')
    # Verify that the program is either public, the current user is the creator, teacher or the user is admin
    if not public_program and user['username'] != result['username'] and not is_admin(user):
        if (not is_teacher(user)) or (is_teacher(user) and result['username'] not in DATABASE.get_teacher_students(user['username'])):
            return utils.error_page(error=404, ui_message=gettext(u'no_such_program'))

    # The program is valid, verify if the creator also have a public profile
    result['public_profile'] = True if DATABASE.get_public_profile_settings(
        result['username']) else None

    # If the language doesn't match the user -> parse the keywords
    if result.get("lang", "en") not in [g.lang, "en"] and g.lang in ALL_KEYWORD_LANGUAGES:
        result['code'] = hedy_translation.translate_keywords(result.get(
            'code'), result.get('lang', 'en'), g.lang, level=int(result.get('level', 1)))

    arguments_dict = {}
    arguments_dict['program_id'] = id
    arguments_dict['page_title'] = f'{result["name"]} – Hedy'
    arguments_dict['level'] = result['level']  # Necessary for running
    arguments_dict['loaded_program'] = result
    arguments_dict['editor_readonly'] = True

    if "submitted" in result and result['submitted']:
        arguments_dict['show_edit_button'] = False
        now = timems()
        arguments_dict['program_age'] = get_user_formatted_age(
            now, result['date'])
        arguments_dict[
            'program_timestamp'] = f"{datetime.datetime.fromtimestamp(result['date'] / 1000.0).strftime('%d-%m-%Y, %H:%M:%S')} GMT"
    else:
        arguments_dict['show_edit_button'] = True

    # Everything below this line has nothing to do with this page and it's silly
    # that every page needs to put in so much effort to re-set it

    return render_template("view-program-page.html", **arguments_dict)


@app.route('/adventure/<name>', methods=['GET'], defaults={'level': 1})
@app.route('/adventure/<name>/<level>', methods=['GET'])
def get_specific_adventure(name, level):
    try:
        level = int(level)
    except:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    adventure = [x for x in load_adventures_per_level(
        level) if x.get('short_name') == name]
    if not adventure:
        return utils.error_page(error=404, ui_message=gettext('no_such_adventure'))

    prev_level = level-1 if [x for x in load_adventures_per_level(
        level-1) if x.get('short_name') == name] else False
    next_level = level+1 if [x for x in load_adventures_per_level(
        level+1) if x.get('short_name') == name] else False

    return hedyweb.render_specific_adventure(level_number=level, adventure=adventure, version=version(),
                                             prev_level=prev_level, next_level=next_level)


@app.route('/cheatsheet/', methods=['GET'], defaults={'level': 1})
@app.route('/cheatsheet/<level>', methods=['GET'])
def get_cheatsheet_page(level):
    try:
        level = int(level)
        if level < 1 or level > hedy.HEDY_MAX_LEVEL:
            return utils.error_page(error=404, ui_message=gettext('no_such_level'))
    except:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    commands = COMMANDS[g.lang].get_commands_for_level(level, g.keyword_lang)

    return render_template("cheatsheet.html", commands=commands, level=level)


@app.errorhandler(404)
def not_found(exception):
    return utils.error_page(error=404, ui_message=gettext('page_not_found'))


@app.errorhandler(500)
def internal_error(exception):
    import traceback
    print(traceback.format_exc())
    return utils.error_page(error=500)


@app.route('/index.html')
@app.route('/')
def default_landing_page():
    return main_page('start')


@app.route('/signup', methods=['GET'])
def signup_page():
    if current_user()['username']:
        return redirect('/my-profile')
    return render_template('signup.html', page_title=gettext('title_signup'), current_page='login')


@app.route('/login', methods=['GET'])
def login_page():
    if current_user()['username']:
        return redirect('/my-profile')
    return render_template('login.html', page_title=gettext('title_login'), current_page='login')


@app.route('/recover', methods=['GET'])
def recover_page():
    if current_user()['username']:
        return redirect('/my-profile')
    return render_template('recover.html', page_title=gettext('title_recover'), current_page='login')


@app.route('/reset', methods=['GET'])
def reset_page():
    # If there is a user logged in -> don't allow password reset
    if current_user()['username']:
        return redirect('/my-profile')

    username = request.args.get('username', default=None, type=str)
    token = request.args.get('token', default=None, type=str)
    username = None if username == "null" else username
    token = None if token == "null" else token

    if not username or not token:
        return utils.error_page(error=403, ui_message=gettext('unauthorized'))
    return render_template('reset.html', page_title=gettext('title_reset'), reset_username=username, reset_token=token, current_page='login')


@app.route('/my-profile', methods=['GET'])
@requires_login
def profile_page(user):

    profile = DATABASE.user_by_username(user['username'])
    programs = DATABASE.public_programs_for_user(user['username'])
    public_profile_settings = DATABASE.get_public_profile_settings(current_user()[
                                                                   'username'])

    classes = []
    if profile.get('classes'):
        for class_id in profile.get('classes'):
            classes.append(DATABASE.get_class(class_id))

    invite = DATABASE.get_username_invite(user['username'])
    if invite:
        # If there is an invite: retrieve the class information
        class_info = DATABASE.get_class(invite.get('class_id', None))
        if class_info:
            invite['teacher'] = class_info.get('teacher')
            invite['class_name'] = class_info.get('name')
            invite['join_link'] = class_info.get('link')

    return render_template('profile.html', page_title=gettext('title_my-profile'), programs=programs,
                           user_data=profile, invite_data=invite, public_settings=public_profile_settings,
                           user_classes=classes, current_page='my-profile')


@app.route('/<page>')
def main_page(page):
    if page == 'favicon.ico':
        abort(404)

    if page == "my-achievements":
        return achievements_page()

    if page == 'learn-more':
        learn_more_translations = hedyweb.PageTranslations(
            page).get_page_translations(g.lang)
        return render_template('learn-more.html', page_title=gettext('title_learn-more'),
                               current_page='learn-more', content=learn_more_translations)

    if page == 'privacy':
        privacy_translations = hedyweb.PageTranslations(
            page).get_page_translations(g.lang)
        return render_template('privacy.html', page_title=gettext('title_privacy'),
                               content=privacy_translations)

    user = current_user()

    if page == 'landing-page':
        if user['username']:
            return render_template('landing-page.html', page_title=gettext('title_landing-page'), user=user['username'])
        else:
            return utils.error_page(error=403, ui_message=gettext('not_user'))

    if page == 'for-teachers':
        for_teacher_translations = hedyweb.PageTranslations(
            page).get_page_translations(g.lang)
        if is_teacher(user):
            welcome_teacher = session.get('welcome-teacher') or False
            session.pop('welcome-teacher', None)
            teacher_classes = [] if not current_user(
            )['username'] else DATABASE.get_teacher_classes(current_user()['username'], True)
            adventures = []
            for adventure in DATABASE.get_teacher_adventures(current_user()['username']):
                adventures.append(
                    {'id': adventure.get('id'),
                     'name': adventure.get('name'),
                     'date': utils.datetotimeordate(utils.mstoisostring(adventure.get('date'))),
                     'level': adventure.get('level')
                     }
                )

            return render_template('for-teachers.html', current_page='my-profile',
                                   page_title=gettext('title_for-teacher'),
                                   content=for_teacher_translations, teacher_classes=teacher_classes,
                                   teacher_adventures=adventures, welcome_teacher=welcome_teacher)
        else:
            return utils.error_page(error=403, ui_message=gettext('not_teacher'))

    requested_page = hedyweb.PageTranslations(page)
    if not requested_page.exists():
        abort(404)

    main_page_translations = requested_page.get_page_translations(g.lang)
    return render_template('main-page.html', page_title=gettext('title_start'),
                           current_page='start', content=main_page_translations)


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
        achievement = ACHIEVEMENTS.add_single_achievement(
            current_user()['username'], "indiana_jones")
    else:
        programs = DATABASE.get_all_explore_programs()

    filtered_programs = []
    for program in programs:
        # If program does not have an error value set -> parse it and set value
        if 'error' not in program:
            try:
                hedy.transpile(program.get('code'), program.get(
                    'level'), program.get('lang'))
                program['error'] = False
            except:
                program['error'] = True
            DATABASE.store_program(program)
        public_profile = DATABASE.get_public_profile_settings(
            program['username'])
        # If the language doesn't match the user -> parse the keywords
        if program.get("lang", "en") != g.keyword_lang and program.get("lang") in ALL_KEYWORD_LANGUAGES.keys():
            code = hedy_translation.translate_keywords(program.get('code'), from_lang=program.get('lang'),
                                                       to_lang=g.keyword_lang, level=int(program.get('level', 1)))
        else:
            code = program['code']
        filtered_programs.append({
            'username': program['username'],
            'name': program['name'],
            'level': program['level'],
            'id': program['id'],
            'error': program['error'],
            'public_user': True if public_profile else None,
            'code': "\n".join(code.split("\n")[:4])
        })

    adventures_names = hedy_content.Adventures(
        session['lang']).get_adventure_names()

    return render_template('explore.html', programs=filtered_programs,
                           filtered_level=level,
                           achievement=achievement,
                           filtered_adventure=adventure,
                           max_level=hedy.HEDY_MAX_LEVEL,
                           adventures_names=adventures_names,
                           page_title=gettext('title_explore'),
                           current_page='explore')


@app.route('/change_language', methods=['POST'])
def change_language():
    body = request.json
    session['lang'] = body.get('lang')
    return jsonify({'succes': 200})


@app.route('/translate_keywords', methods=['POST'])
def translate_keywords():
    body = request.json
    try:
        translated_code = hedy_translation.translate_keywords(body.get('code'), body.get(
            'start_lang'), body.get('goal_lang'), level=int(body.get('level', 1)))
        if translated_code:
            return jsonify({'success': 200, 'code': translated_code})
        else:
            return gettext('translate_error'), 400
    except:
        return gettext('translate_error'), 400


@app.route('/client_messages.js', methods=['GET'])
def client_messages():
    # Not really nice, but we don't call this often as it is cached
    d = collections.defaultdict(lambda: 'Unknown Exception')
    d.update(YamlFile.for_file('content/client-messages/en.yaml').to_dict())
    d.update(YamlFile.for_file(
        f'content/client-messages/{g.lang}.yaml').to_dict())

    response = make_response(render_template(
        "client_messages.js", error_messages=json.dumps(d)))

    if not is_debug_mode():
        # Cache for longer when not developing
        response.cache_control.max_age = 60 * 60  # Seconds
    return response


@app.template_global()
def current_language():
    return make_lang_obj(g.lang)


@app.template_global()
def current_keyword_language():
    return make_keyword_lang_obj(g.keyword_lang)


@app.template_global()
def other_keyword_language():
    # If the current keyword language isn't English: we are sure the other option is English
    # But, only if the user has an existing keyword language -> on the session
    if session.get('keyword_lang') and session['keyword_lang'] != "en":
        return make_keyword_lang_obj("en")
    return None


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
    parts = ['/hedy']
    parts.append('/' + str(level_nr))
    if str(assignment_nr) != '1' or subpage:
        parts.append('/' + str(assignment_nr if assignment_nr else '1'))
    if subpage and subpage != 'code':
        parts.append('/' + subpage)
    return ''.join(parts)


@app.template_global()
def all_countries():
    return COUNTRIES


@app.template_global()
def other_languages():
    cl = g.lang
    return [make_lang_obj(l) for l in ALL_LANGUAGES.keys() if l != cl]


@app.template_global()
def other_keyword_languages():
    cl = g.lang
    return [make_lang_obj(l) for l in ALL_KEYWORD_LANGUAGES.keys() if l != cl]


@app.template_global()
def keyword_languages():
    return [make_lang_obj(l) for l in ALL_KEYWORD_LANGUAGES.keys()]


@app.template_global()
def keyword_languages_keys():
    return [l for l in ALL_KEYWORD_LANGUAGES.keys()]


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


# We only store this @app.route here to enable the use of achievements -> might want to re-write this in the future
@app.route('/auth/public_profile', methods=['POST'])
@requires_login
def update_public_profile(user):
    body = request.json

    # Validations
    if not isinstance(body, dict):
        return gettext('ajax_error'), 400
    # The images are given as a "picture id" from 1 till 12
    if not isinstance(body.get('image'), str) or int(body.get('image'), 0) < 1 or int(body.get('image'), 0) > 12:
        return gettext('image_invalid'), 400
    if not isinstance(body.get('personal_text'), str):
        return gettext('personal_text_invalid'), 400
    if 'favourite_program' in body and not isinstance(body.get('favourite_program'), str):
        return gettext('favourite_program_invalid'), 400

    # Verify that the set favourite program is actually from the user (and public)!
    if 'favourite_program' in body:
        program = DATABASE.program_by_id(body.get('favourite_program'))
        if not program or program.get('username') != user['username'] or not program.get('public'):
            return gettext('favourite_program_invalid'), 400

    achievement = None
    current_profile = DATABASE.get_public_profile_settings(user['username'])
    if current_profile:
        if current_profile.get('image') != body.get('image'):
            achievement = ACHIEVEMENTS.add_single_achievement(
                current_user()['username'], "fresh_look")
    else:
        achievement = ACHIEVEMENTS.add_single_achievement(
            current_user()['username'], "go_live")
    DATABASE.update_public_profile(user['username'], body)
    if achievement:
        # Todo TB -> Check if we require message or success on front-end
        return {'message': gettext('public_profile_updated'), 'achievement': achievement}, 200
    return {'message': gettext('public_profile_updated')}, 200


@app.route('/translating')
def translating_page():
    return render_template('translating.html')


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
            translating.apply_form_change(
                data, key[2:], translating.normalize_newlines(value))

    data = translating.normalize_yaml_blocks(data)

    return Response(dump_yaml_rt(data),
                    mimetype='application/x-yaml',
                    headers={'Content-disposition': 'attachment; filename=' + request.form['file'].replace('/', '-')})


@app.route('/user/<username>')
def public_user_page(username):
    if not current_user()['username']:
        return utils.error_page(error=403, ui_message=gettext('unauthorized'))
    username = username.lower()
    user = DATABASE.user_by_username(username)
    if not user:
        return utils.error_page(error=404, ui_message=gettext('user_not_private'))
    user_public_info = DATABASE.get_public_profile_settings(username)
    if user_public_info:
        user_programs = DATABASE.public_programs_for_user(username)
        user_achievements = DATABASE.progress_by_username(username) or {}

        favourite_program = None
        if 'favourite_program' in user_public_info and user_public_info['favourite_program']:
            favourite_program = DATABASE.program_by_id(
                user_public_info['favourite_program'])
        if len(user_programs) >= 5:
            user_programs = user_programs[:5]

        last_achieved = None
        if user_achievements.get('achieved'):
            last_achieved = user_achievements['achieved'][-1]

        # Todo: TB -> In the near future: add achievement for user visiting their own profile

        return render_template('public-page.html', user_info=user_public_info,
                               achievements=ACHIEVEMENTS_TRANSLATIONS.get_translations(
                                   g.lang),
                               favourite_program=favourite_program,
                               programs=user_programs,
                               last_achieved=last_achieved,
                               user_achievements=user_achievements)
    return utils.error_page(error=404, ui_message=gettext('user_not_private'))


@app.route('/invite/<code>', methods=['GET'])
def teacher_invitation(code):
    user = current_user()

    if os.getenv('TEACHER_INVITE_CODE') != code:
        return utils.error_page(error=404, ui_message=gettext('invalid_teacher_invitation_code'))
    if not user['username']:
        return render_template('teacher-invitation.html')

    update_is_teacher(user)
    # When visiting this link we update the current user to a teacher -> also update user in session
    session.get('user')['is_teacher'] = True

    session['welcome-teacher'] = True
    url = request.url.replace(f'/invite/{code}', '/for-teachers')
    return redirect(url)

# *** AUTH ***


auth.routes(app, DATABASE)

# *** PROGRAMS BACKEND ***

programs.routes(app, DATABASE, ACHIEVEMENTS)

# *** TEACHER BACKEND ***

teacher.routes(app, DATABASE, ACHIEVEMENTS)

# *** ADMIN BACKEND ***

admin.routes(app, DATABASE)

# *** ACHIEVEMENTS BACKEND ***

ACHIEVEMENTS.routes(app, DATABASE)

# *** QUIZ BACKEND ***

quiz.routes(app, DATABASE, ACHIEVEMENTS, QUIZZES)


# *** STATISTICS ***

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
    app.run(threaded=True, debug=not is_in_debugger,
            port=config['port'], host="0.0.0.0")

    # See `Procfile` for how the server is started on Heroku.
