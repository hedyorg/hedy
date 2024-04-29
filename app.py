# coding=utf-8
import base64
import binascii
import collections
import copy
import logging
import json
import datetime
import os
import re
import subprocess
import sys
import traceback
import textwrap
import unicodedata
import zipfile
import jinja_partials
from typing import Optional
from logging.config import dictConfig as logConfig
from os import path

import static_babel_content
from markupsafe import Markup
from flask import (Flask, Response, abort, after_this_request, g, make_response,
                   redirect, request, send_file, url_for, jsonify,
                   send_from_directory, session)
from flask_babel import Babel, gettext
from website.flask_commonmark import Commonmark
from flask_compress import Compress
from urllib.parse import quote_plus

import hedy
import hedy_content
import hedy_translation
import hedyweb
import utils
from hedy_error import get_error_text
from safe_format import safe_format
from config import config
from website.flask_helpers import render_template, proper_tojson, JinjaCompatibleJsonProvider
from hedy_content import (ADVENTURE_ORDER_PER_LEVEL, KEYWORDS_ADVENTURES, ALL_KEYWORD_LANGUAGES,
                          ALL_LANGUAGES, COUNTRIES, HOUR_OF_CODE_ADVENTURES)

from logging_config import LOGGING_CONFIG
from utils import dump_yaml_rt, is_debug_mode, load_yaml_rt, timems, version, strip_accents
from website import (ab_proxying, achievements, admin, auth_pages, aws_helpers,
                     cdn, classes, database, for_teachers, s3_logger, parsons,
                     profile, programs, querylog, quiz, statistics,
                     translating, tags, surveys, public_adventures, user_activity, feedback)
from website.auth import (current_user, hide_explore, is_admin, is_teacher, is_second_teacher, has_public_profile,
                          login_user_from_token_cookie, requires_login, requires_login_redirect, requires_teacher,
                          forget_current_user)
from website.log_fetcher import log_fetcher
from website.frontend_types import Adventure, Program, ExtraStory, SaveInfo

logConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Todo TB: This can introduce a possible app breaking bug when switching
# to Python 4 -> e.g. Python 4.0.1 is invalid
if (sys.version_info.major < 3 or sys.version_info.minor < 7):
    print('Hedy requires Python 3.7 or newer to run. However, your version of Python is', '.'.join(
        [str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro)]))
    quit()

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(
    os.path.basename(__file__), '')))

# Setting up Flask and babel (web and translations)
app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False  # Ignore trailing slashes in URLs
app.json = JinjaCompatibleJsonProvider(app)

# Most files should be loaded through the CDN which has its own caching period and invalidation.
# Use 5 minutes as a reasonable default for all files we load elsewise.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = datetime.timedelta(minutes=5)


def get_locale():
    return session.get("lang", request.accept_languages.best_match(ALL_LANGUAGES.keys(), 'en'))


babel = Babel(app, locale_selector=get_locale)

jinja_partials.register_extensions(app)
app.template_filter('tojson')(proper_tojson)

COMMANDS = collections.defaultdict(hedy_content.NoSuchCommand)
for lang in ALL_LANGUAGES.keys():
    COMMANDS[lang] = hedy_content.Commands(lang)

ADVENTURES = collections.defaultdict(hedy_content.NoSuchAdventure)
for lang in ALL_LANGUAGES.keys():
    ADVENTURES[lang] = hedy_content.Adventures(lang)

PARSONS = collections.defaultdict()
for lang in ALL_LANGUAGES.keys():
    PARSONS[lang] = hedy_content.ParsonsProblem(lang)

QUIZZES = collections.defaultdict(hedy_content.NoSuchQuiz)
for lang in ALL_LANGUAGES.keys():
    QUIZZES[lang] = hedy_content.Quizzes(lang)

TUTORIALS = collections.defaultdict(hedy_content.NoSuchTutorial)
for lang in ALL_LANGUAGES.keys():
    TUTORIALS[lang] = hedy_content.Tutorials(lang)

SLIDES = collections.defaultdict(hedy_content.NoSuchSlides)
for lang in ALL_LANGUAGES.keys():
    SLIDES[lang] = hedy_content.Slides(lang)

ACHIEVEMENTS_TRANSLATIONS = hedyweb.AchievementTranslations()
DATABASE = database.Database()
ACHIEVEMENTS = achievements.Achievements(DATABASE, ACHIEVEMENTS_TRANSLATIONS)
SURVEYS = surveys.SurveysModule(DATABASE)
STATISTICS = statistics.StatisticsModule(DATABASE)

TAGS = collections.defaultdict(hedy_content.NoSuchAdventure)
for lang in ALL_LANGUAGES.keys():
    TAGS[lang] = hedy_content.Tags(lang)


def load_adventures_for_level(level, subset=None):
    """Load the adventures available to the current user at the given level.

    These are the default adventures, with the customizations implied
    by any class they are a part of. We also load any programs the user has
    that apply to the current level.

    Adventures are loaded in the current language, with the keywords in the code
    translated to the default (or explicitly requested) keyword language.
    """
    keyword_lang = g.keyword_lang

    all_adventures = []
    # NOTE: if we ever have ADVENTURES in the DB, adjust how the "levels" field is used.
    if subset:
        adventures = ADVENTURES[g.lang].get_adventures_subset(subset, keyword_lang)
    else:
        adventures = ADVENTURES[g.lang].get_adventures(keyword_lang)

    for short_name, adventure in adventures.items():
        adventure_level = adventure['levels'].get(level, None)
        if not adventure_level:
            continue

        # Sometimes we have multiple text and example_code -> iterate these and add as well!

        extra_stories = [
            ExtraStory(
                text=adventure_level.get(f'story_text_{i}'),
                example_code=adventure_level.get(f'example_code_{i}'))
            for i in range(2, 10)
            if adventure_level.get(f'story_text_{i}', '')
        ]

        default_save_name = adventure.get('default_save_name')
        if not default_save_name or default_save_name == 'intro':
            default_save_name = adventure['name']

        # only add adventures that have been added to the adventure list of this level
        if short_name in ADVENTURE_ORDER_PER_LEVEL.get(level, []):
            current_adventure = Adventure(
                short_name=short_name,
                name=adventure['name'],
                image=adventure.get('image', None),
                text=adventure['levels'][level].get('story_text', ""),
                example_code=adventure['levels'][level].get('example_code', ""),
                extra_stories=extra_stories,
                is_teacher_adventure=False,
                is_command_adventure=short_name in KEYWORDS_ADVENTURES,
                save_name=f'{default_save_name} {level}')

            all_adventures.append(current_adventure)

    # Sort the adventures based on the default ordering
    adventures_order = ADVENTURE_ORDER_PER_LEVEL.get(level, [])
    index_map = {v: i for i, v in enumerate(adventures_order)}
    all_adventures.sort(key=lambda pair: index_map.get(
        pair['short_name'],
        len(adventures_order)))

    return all_adventures


def load_saved_programs(level, into_adventures, preferential_program: Optional[Program]):
    """Load saved previous saved programs by the current user into the given adventures array.

    Mutates the adventures in-place, by setting the 'save_name'
    and 'save_info' attributes of adventures.
    """
    if not current_user()['username']:
        return

    loaded_programs = {k: Program.from_database_row(r)
                       for k, r in DATABASE.last_level_programs_for_user(current_user()['username'], level).items()}

    # If there is a preferential program, overwrite any other one that might exist so we definitely
    # load this one.
    if preferential_program:
        loaded_programs[preferential_program.adventure_name] = preferential_program

    # Copy them into the adventures array
    #
    # For every adventure, find a program in the `loaded_programs` dictionary.
    # Since the program may be saved under either the id or the actual name, check both.
    for adventure in into_adventures:
        program = loaded_programs.get(adventure.short_name)
        if not program:
            program = loaded_programs.get(adventure.name)
        if not program:
            continue

        adventure.save_name = program.name
        adventure.editor_contents = program.code
        adventure.save_info = SaveInfo.from_program(program)


def load_customized_adventures(level, customizations, into_adventures):
    """Load the teacher customizations into the set of adventures.

    It would have been nicer if the complete set of adventures had come
    out of 'load_adventures_for_level', but looking up customizations is
    a bit expensive and since we've already done that in the caller, we pass
    it in here.

    Mutates the 'into_adventures' list in-place. On entry, it is the list of
    default `Adventure` objects in the default order. On exit, it may have been
    reordered and enhanced with teacher-written adventures.
    """
    # First find the list of all teacher adventures for the current level,
    # batch-get all of them, then put them into the adventures array in the correct
    # location.

    # { <str>level -> [ { <str>name, <bool>from_teacher ] }
    # 'name' is either a shortname or an ID into the teacher table
    sorted_adventures = customizations.get('sorted_adventures', {})
    order_for_this_level = sorted_adventures.get(str(level), [])
    if not order_for_this_level:
        return  # Nothing to do

    adventure_ids = {a['name'] for a in order_for_this_level if a['from_teacher']}
    teacher_adventure_map = DATABASE.batch_get_adventures(adventure_ids)
    builtin_adventure_map = {a.short_name: a for a in into_adventures}

    # Replace `into_adventures`
    into_adventures[:] = []
    for a in order_for_this_level:
        if a['from_teacher'] and (db_row := teacher_adventure_map.get(a['name'])):
            try:
                if 'formatted_content' in db_row:
                    db_row['formatted_content'] = safe_format(db_row['formatted_content'],
                                                              **hedy_content.KEYWORDS.get(g.keyword_lang))
                else:
                    db_row['content'] = safe_format(db_row['content'],
                                                    **hedy_content.KEYWORDS.get(g.keyword_lang))
            except Exception:
                # We don't want teacher being able to break the student UI -> pass this adventure
                pass

            into_adventures.append(Adventure.from_teacher_adventure_database_row(db_row))
        if not a['from_teacher'] and (adv := builtin_adventure_map.get(a['name'])):
            into_adventures.append(adv)


cdn.Cdn(app, os.getenv('CDN_PREFIX'), os.getenv('HEROKU_SLUG_COMMIT', 'dev'))


@app.before_request
def redirect_outdated_domains():
    """If Hedy is being loaded from a domain we no longer use or advertise,
    do a 301 redirect to the official 'hedy.org' domain.

    If we keep this up for long enough, eventually Google will update its index
    to forget about the old domains.
    """
    # request.host looks like 'hostname[:port]'
    host = request.host.split(':')[0]

    if host in ['hedycode.com', 'hedy-beta.herokuapp.com']:
        # full_path starts with '/' and has everything
        return redirect(f'https://hedy.org{request.full_path}', code=301)


@app.before_request
def before_request_begin_logging():
    """Initialize the query logging.

    This needs to happen as one of the first things, as the database calls
    etc. depend on it.
    """
    path = (str(request.path) + '?' + request.query_string.decode('utf-8')
            ) if request.query_string else str(request.path)
    querylog.begin_global_log_record(
        path=path,
        method=request.method,
        remote_ip=request.headers.get('X-Forwarded-For', request.remote_addr),
        user_agent=request.headers.get('User-Agent'))


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
    # Set the database object on the global object (auth.py needs it)
    g.db = DATABASE

    # Invoke session_id() for its side effect
    utils.session_id()
    login_user_from_token_cookie()

    g.user = current_user()
    querylog.log_value(session_id=utils.session_id(), username=g.user['username'],
                       is_teacher=is_teacher(g.user), is_admin=is_admin(g.user))


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
# For settings with multiple workers, an environment variable is required,
# otherwise cookies will be constantly removed and re-set by different
# workers.
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

# Set security attributes for cookies in a central place - but not when
# running locally, so that session cookies work well without HTTPS

Compress(app)
Commonmark(app)

# We don't need to log in offline mode
if utils.is_offline_mode():
    parse_logger = s3_logger.NullLogger()
else:
    parse_logger = s3_logger.S3Logger(name="parse", config_key="s3-parse-logs")
    querylog.LOG_QUEUE.set_transmitter(
        aws_helpers.s3_querylog_transmitter_from_env())


@app.before_request
def setup_language():
    # Determine the user's requested language code.
    #
    # If not in the request parameters, use the browser's accept-languages
    # header to do language negotiation. Can be changed in the session by
    # POSTing to `/change_language`, and be overwritten by remember_current_user().
    if lang_from_request := request.args.get('language', None):
        session['lang'] = lang_from_request
    if 'lang' not in session:
        session['lang'] = request.accept_languages.best_match(
            ALL_LANGUAGES.keys(), 'en')
    g.lang = session['lang']
    querylog.log_value(lang=session['lang'])

    if 'keyword_lang' not in session:
        session['keyword_lang'] = g.lang if g.lang in ALL_KEYWORD_LANGUAGES.keys() else 'en'
    # If there is a '?keyword_language=' parameter, it overrides the current keyword lang, permanently
    if request.args.get('keyword_language', None):
        session['keyword_lang'] = request.args.get('keyword_language', None)
    g.keyword_lang = session['keyword_lang']

    # Set the page direction -> automatically set it to "left-to-right"
    # Switch to "right-to-left" if one of the language is rtl according to Locale (from Babel) settings.
    # This is the only place to expand / shrink the list of RTL languages ->
    # front-end is fixed based on this value
    g.dir = static_babel_content.TEXT_DIRECTIONS.get(g.lang, 'ltr')

    # True if it is a Latin alphabet, False if not
    g.latin = all('LATIN' in unicodedata.name(char, '').upper() for char in current_language()['sym'])

    # Check that requested language is supported, otherwise return 404
    if g.lang not in ALL_LANGUAGES.keys():
        return "Language " + g.lang + " not supported", 404


if utils.is_heroku() and not os.getenv('HEROKU_RELEASE_CREATED_AT'):
    logger.warning(
        'Cannot determine release; enable Dyno metadata by running'
        '"heroku labs:enable runtime-dyno-metadata -a <APP_NAME>"')


# A context processor injects variables in the context that are available to all templates.
@app.context_processor
def enrich_context_with_user_info():
    user = current_user()
    data = {'username': user.get('username', ''),
            'is_teacher': is_teacher(user), 'is_second_teacher': is_second_teacher(user),
            'is_admin': is_admin(user), 'has_public_profile': has_public_profile(user),
            'hide_explore': hide_explore(g.user)}
    return data


@app.context_processor
def add_generated_css_file():
    return {
        "generated_css_file": '/css/generated.full.css' if is_debug_mode() else '/css/generated.css'
    }


@app.context_processor
def add_hx_detection():
    """Detect when a request is sent by HTMX.

    A template may decide to render things differently when it is vs. when it isn't.
    """
    hx_request = bool(request.headers.get('Hx-Request'))
    return {
        "hx_request": hx_request,
        "hx_layout": 'htmx-layout-yes.html' if hx_request else 'htmx-layout-no.html',
    }


@app.after_request
def hx_triggers(response):
    """For HTMX Requests, push any pending achievements in the session to the client.

    Use the HX-Trigger header, which will trigger events on the client. There is a listener
    there which will respond to the 'displayAchievements' event.
    """
    if not request.headers.get('HX-Request'):
        return response

    achs = session.pop('pending_achievements', [])
    if achs:
        response.headers.set('HX-Trigger', json.dumps({'displayAchievements': achs}))
    return response


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
    log_record = querylog.finish_global_log_record(exc)
    if is_debug_mode():
        logger.debug(repr(log_record.as_data()))


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
    return jsonify({'session': dict(session),
                    'proxy_enabled': bool(os.getenv('PROXY_TO_TEST_HOST'))})


@app.route('/parse', methods=['POST'])
@querylog.timed_as('parse_handler')
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
    if 'is_debug' not in body:
        return "body.is_debug must be a boolean", 400
    if 'raw' not in body:
        return "body.raw is missing", 400
    error_check = False
    if 'error_check' in body:
        error_check = True

    code = body['code']
    level = int(body['level'])
    is_debug = bool(body['is_debug'])
    # Language should come principally from the request body,
    # but we'll fall back to browser default if it's missing for whatever
    # reason.
    lang = body.get('lang', g.lang)

    # true if kid enabled the read aloud option
    read_aloud = body.get('read_aloud', False)
    raw = body.get('raw')

    response = {}
    username = current_user()['username'] or None
    exception = None

    querylog.log_value(level=level, lang=lang,
                       session_id=utils.session_id(), username=username)

    try:
        keyword_lang = current_keyword_language()["lang"]
        with querylog.log_time('transpile'):
            try:
                transpile_result = transpile_add_stats(code, level, lang, is_debug)
                if username and not body.get('tutorial'):
                    DATABASE.increase_user_run_count(username)
                    if not raw:
                        ACHIEVEMENTS.increase_count("run")
            except hedy.exceptions.WarningException as ex:
                translated_error = get_error_text(ex, keyword_lang)
                if isinstance(ex, hedy.exceptions.InvalidSpaceException):
                    response['Warning'] = translated_error
                elif isinstance(ex, hedy.exceptions.UnusedVariableException):
                    response['Warning'] = translated_error
                else:
                    response['Error'] = translated_error
                response['Location'] = ex.error_location
                transpile_result = ex.fixed_result
                exception = ex
            except hedy.exceptions.UnquotedEqualityCheckException as ex:
                response['Error'] = get_error_text(ex, keyword_lang)
                response['Location'] = ex.error_location
                exception = ex

        try:
            response['Code'] = transpile_result.code
            source_map_result = transpile_result.source_map.get_result()

            for i, mapping in source_map_result.items():
                if mapping['error'] is not None:
                    source_map_result[i]['error'] = get_error_text(source_map_result[i]['error'], keyword_lang)

            response['source_map'] = source_map_result

            if transpile_result.has_pressed:
                response['has_pressed'] = True

            if transpile_result.has_turtle:
                response['has_turtle'] = True

            if transpile_result.has_clear:
                response['has_clear'] = True

            if transpile_result.has_music:
                response['has_music'] = True

        except Exception:
            pass

        if level < 7:
            with querylog.log_time('detect_sleep'):
                try:
                    # FH, Nov 2023: hmmm I don't love that this is not done in the same place as the other "has"es
                    sleep_list = []
                    pattern = (
                        r'time\.sleep\((?P<time>\d+)\)'
                        r'|time\.sleep\(int\("(?P<sleep_time>\d+)"\)\)'
                        r'|time\.sleep\(int\((?P<variable>\w+)\)\)')
                    matches = re.finditer(
                        pattern,
                        response['Code'])
                    for i, match in enumerate(matches, start=1):
                        time = match.group('time')
                        sleep_time = match.group('sleep_time')
                        variable = match.group('variable')
                        if sleep_time:
                            sleep_list.append(int(sleep_time))
                        elif time:
                            sleep_list.append(int(time))
                        elif variable:
                            assignment_match = re.search(r'{} = (.+?)\n'.format(variable), response['Code'])
                            if assignment_match:
                                assignment_code = assignment_match.group(1)
                                variable_value = eval(assignment_code)
                                sleep_list.append(int(variable_value))
                    if sleep_list:
                        response['has_sleep'] = sleep_list
                except BaseException:
                    pass

        if not raw:
            try:
                if username and not body.get('tutorial') and ACHIEVEMENTS.verify_run_achievements(
                        username, code, level, response, transpile_result.commands):
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

    # Save this program (if the user is logged in)
    if username and body.get('save_name'):
        try:
            program_logic = programs.ProgramsLogic(DATABASE, ACHIEVEMENTS, STATISTICS)
            program = program_logic.store_user_program(
                user=current_user(),
                level=level,
                name=body.get('save_name'),
                program_id=body.get('program_id'),
                adventure_name=body.get('adventure_name'),
                short_name=body.get('short_name'),
                code=code,
                error=exception is not None)

            response['save_info'] = SaveInfo.from_program(Program.from_database_row(program))
            if program.get('is_modified'):
                response['is_modified'] = True
        except programs.NotYourProgramError:
            # No permissions to overwrite, no biggie
            pass

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
            hedy.transpile(
                program.get('code'),
                program.get('level'),
                program.get('lang')
            )
            return make_response('', 204)
        except BaseException:
            return {"error": "parsing error"}, 200
    else:
        return 'this is not your program!', 400


@app.route('/parse_tutorial', methods=['POST'])
@requires_login
def parse_tutorial(user):
    body = request.json

    code = body['code']
    level = try_parse_int(body['level'])
    try:
        result = hedy.transpile(code, level, "en")
        jsonify({'code': result.code}), 200
    except BaseException:
        return "error", 400


@app.route("/generate_machine_files", methods=['POST'])
def prepare_files():
    body = request.json
    # Prepare the file -> return the "secret" filename as response
    transpiled_code = hedy.transpile(body.get("code"), body.get("level"), body.get("lang"))
    filename = utils.random_id_generator(12)

    # We have to turn the turtle 90 degrees to align with the user perspective app.ts#16
    # This is not a really nice solution, but as we store the prefix on the
    # front-end it should be good for now
    threader = textwrap.dedent("""
        import time
        from turtlethread import Turtle
        t = Turtle()
        t.left(90)
        with t.running_stitch(stitch_length=20):
        """)
    lines = transpiled_code.code.split("\n")

    # remove all sleeps for speeed, and remove all colors for compatibility:
    lines = [x for x in lines if ("time.sleep" not in x) and ("t.pencolor" not in x)]

    threader += "  " + "\n  ".join(lines)
    threader += "\n" + 't.save("machine_files/' + filename + '.dst")'
    threader += "\n" + 't.save("machine_files/' + filename + '.png")'
    if not os.path.isdir('machine_files'):
        os.makedirs('machine_files')
    exec(threader)

    # stolen from: https://stackoverflow.com/questions/28568687/send-with-multiple-csvs-using-flask

    zip_file = zipfile.ZipFile(f'machine_files/{filename}.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('machine_files/'):
        # only zip files for this request, and exclude the zip file itself:
        for file in [x for x in files if x[:len(filename)] == filename and x[-3:] != 'zip']:
            zip_file.write('machine_files/' + file)
    zip_file.close()

    return jsonify({'filename': filename}), 200


@app.route("/download_machine_files/<filename>", methods=['GET'])
def download_machine_file(filename, extension="zip"):
    # https://stackoverflow.com/questions/24612366/delete-an-uploaded-file-after-downloading-it-from-flask

    # Once the file is downloaded -> remove it
    @after_this_request
    def remove_file(response):
        try:
            os.remove("machine_files/" + filename + ".zip")
            os.remove("machine_files/" + filename + ".dst")
            os.remove("machine_files/" + filename + ".png")
        except BaseException:
            print("Error removing one of the generated files!")
        return response

    return send_file("machine_files/" + filename + "." + extension, as_attachment=True)


MICROBIT_FEATURE = False


@app.route('/generate_microbit_files', methods=['POST'])
def generate_microbit_file():
    if MICROBIT_FEATURE:
        # Extract variables from request body
        body = request.json
        code = body.get("code")
        level = body.get("level")

        transpile_result = hedy.transpile_and_return_python(code, level)
        save_transpiled_code_for_microbit(transpile_result)
        return jsonify({'filename': 'Micro-bit.py', 'microbit': True}), 200
    else:
        return jsonify({'message': 'Microbit feature is disabled'}), 403


def save_transpiled_code_for_microbit(transpiled_python_code):
    folder = 'Micro-bit'
    filepath = os.path.join(folder, 'Micro-bit.py')

    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(filepath, 'w') as file:
        custom_string = "from microbit import *\nwhile True:"
        file.write(custom_string + "\n")

        # Add space before every display.scroll call
        indented_code = transpiled_python_code.replace("display.scroll(", "    display.scroll(")

        # Append the indented transpiled code
        file.write(indented_code)


@app.route('/download_microbit_files/', methods=['GET'])
def convert_to_hex_and_download():
    if MICROBIT_FEATURE:
        flash_micro_bit()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        micro_bit_directory = os.path.join(current_directory, 'Micro-bit')

        @after_this_request
        def remove_file(response):
            try:
                os.remove("Micro-bit/micropython.hex")
                os.remove("Micro-bit/Micro-bit.py")
            except BaseException:
                print("Error removing one of the generated files!")
            return response

        return send_file(os.path.join(micro_bit_directory, "micropython.hex"), as_attachment=True)
    else:
        return jsonify({'message': 'Microbit feature is disabled'}), 403


def flash_micro_bit():
    subprocess.run(['uflash', "Micro-bit/Micro-bit.py", "Micro-bit"])


def transpile_add_stats(code, level, lang_, is_debug):
    username = current_user()['username'] or None
    number_of_lines = code.count('\n')
    try:
        result = hedy.transpile(code, level, lang_, is_debug=is_debug)
        statistics.add(
            username, lambda id_: DATABASE.add_program_stats(id_, level, number_of_lines, None))
        return result
    except Exception as ex:
        class_name = get_class_name(ex)
        statistics.add(username, lambda id_: DATABASE.add_program_stats(
            id_, level, number_of_lines, class_name))
        raise


def get_class_name(i):
    if i is not None:
        return str(i.__class__.__name__)
    return i


def hedy_error_to_response(ex):
    keyword_lang = current_keyword_language()["lang"]
    return {
        "Error": get_error_text(ex, keyword_lang),
        "Location": ex.error_location
    }


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


@app.route('/commands/<id>')
def all_commands(id):
    program = DATABASE.program_by_id(id)
    code = program.get('code')
    level = program.get('level')
    lang = program.get('lang')
    return render_template(
        'commands.html',
        commands=hedy.all_commands(code, level, lang))


@app.route('/my-achievements')
def achievements_page():
    user = current_user()
    username = user['username']
    if not username:
        # redirect users to /login if they are not logged in
        # Todo: TB -> I wrote this once, but wouldn't it make more sense to simply
        # throw a 302 error?
        url = request.url.replace('/my-achievements', '/login')
        return redirect(url, code=302)

    user_achievements = DATABASE.achievements_by_username(user.get('username')) or []
    achievements = ACHIEVEMENTS_TRANSLATIONS.get_translations(g.lang).get('achievements')

    return render_template(
        'achievements.html',
        page_title=gettext('title_achievements'),
        translations=achievements,
        user_achievements=user_achievements,
        current_page='my-profile')


@app.route('/programs', methods=['GET'])
@requires_login_redirect
def programs_page(user):
    username = user['username']
    if not username:
        # redirect users to /login if they are not logged in
        url = request.url.replace('/programs', '/login')
        return redirect(url, code=302)

    from_user = request.args.get('user') or None
    if from_user and from_user == "None":
        from_user = None

    # If from_user -> A teacher is trying to view the user programs
    if from_user and not is_admin(user):
        if not is_teacher(user):
            return utils.error_page(error=401, ui_message=gettext('not_teacher'))
        students = DATABASE.get_teacher_students(username)
        if from_user not in students:
            return utils.error_page(error=403, ui_message=gettext('not_enrolled'))

    # We request our own page -> also get the public_profile settings
    public_profile = None
    if not from_user:
        public_profile = DATABASE.get_public_profile_settings(username)

    keyword_lang = g.keyword_lang

    adventure_names = hedy_content.Adventures(g.lang).get_adventure_names(keyword_lang)
    level = request.args.get('level', default=None, type=str) or None
    adventure = request.args.get('adventure', default=None, type=str) or None
    page = request.args.get('page', default=None, type=str)
    filter = request.args.get('filter', default=None, type=str)
    submitted = True if filter == 'submitted' else None

    all_programs = DATABASE.filtered_programs_for_user(from_user or username,
                                                       submitted=submitted,
                                                       pagination_token=page)
    ids_to_fetch = []
    # Some old programs don't have adventure_name in them, or the field is emtpy.
    for program in all_programs:
        if 'adventure_name' in program and program['adventure_name'] and \
                program['adventure_name'] not in adventure_names:
            ids_to_fetch.append(program['adventure_name'])

    all_programs = [program for program in all_programs if program.get('is_modified')]

    teacher_adventures = DATABASE.batch_get_adventures(ids_to_fetch)
    for id, teacher_adventure in teacher_adventures.items():
        if teacher_adventure is not None:
            adventure_names[id] = teacher_adventure['name']
    swapped_adventure_names = {value: key for key, value in adventure_names.items()}
    result = DATABASE.filtered_programs_for_user(from_user or username,
                                                 level=level,
                                                 adventure=swapped_adventure_names.get(adventure),
                                                 submitted=submitted,
                                                 pagination_token=page,
                                                 limit=10)

    programs = []
    for item in result:
        date = utils.delta_timestamp(item['date'])
        # This way we only keep the first 4 lines to show as preview to the user
        preview_code = "\n".join(item['code'].split("\n")[:4])
        if item.get('is_modified'):
            programs.append(
                {'id': item['id'],
                 'preview_code': preview_code,
                 'code': item['code'],
                 'date': date,
                 'level': item['level'],
                 'name': item['name'],
                 'adventure_name': item.get('adventure_name'),
                 'submitted': item.get('submitted'),
                 'public': item.get('public'),
                 'number_lines': item['code'].count('\n') + 1
                 }
            )

    sorted_level_programs = hedy_content.Adventures(g.lang) \
        .get_sorted_level_programs(all_programs, adventure_names)
    sorted_adventure_programs = hedy_content.Adventures(g.lang) \
        .get_sorted_adventure_programs(all_programs, adventure_names)

    next_page_url = url_for('programs_page', **dict(request.args, page=result.next_page_token)
                            ) if result.next_page_token else None

    return render_template(
        'programs.html',
        programs=programs,
        page_title=gettext('title_programs'),
        current_page='programs',
        from_user=from_user,
        public_profile=public_profile,
        sorted_level_programs=sorted_level_programs,
        sorted_adventure_programs=sorted_adventure_programs,
        adventure_names=adventure_names,
        max_level=hedy.HEDY_MAX_LEVEL,
        next_page_url=next_page_url,
        second_teachers_programs=False,
        user_program_count=len(programs))


@app.route('/logs/query', methods=['POST'])
def query_logs():
    user = current_user()
    if not is_admin(user) and not is_teacher(user):
        return utils.error_page(error=401, ui_message=gettext('unauthorized'))

    body = request.json
    if body is not None and not isinstance(body, dict):
        return 'body must be an object', 400

    class_id = body.get('class_id')
    if not is_admin(user):
        username_filter = body.get('username')
        if not class_id or not username_filter:
            return utils.error_page(error=401, ui_message=gettext('unauthorized'))

        class_ = DATABASE.get_class(class_id)
        if not class_ or class_['teacher'] != user['username'] or username_filter not in class_.get('students', [
        ]):
            return utils.error_page(error=401, ui_message=gettext('unauthorized'))

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
        return utils.error_page(error=401, ui_message=gettext('unauthorized'))

    data, next_token = log_fetcher.get_query_results(
        query_execution_id, next_token)
    response = {'data': data, 'next_token': next_token}
    return jsonify(response)


@app.route('/tutorial', methods=['GET'])
def tutorial_index():
    if not current_user()['username']:
        return redirect('/login')
    level = 1
    cheatsheet = COMMANDS[g.lang].get_commands_for_level(level, g.keyword_lang)
    commands = hedy.commands_per_level.get(level)
    adventures = load_adventures_for_level(level)
    parsons = len(PARSONS[g.lang].get_parsons_data_for_level(level))
    initial_tab = adventures[0].short_name
    initial_adventure = adventures[0]

    max_level = hedy.HEDY_MAX_LEVEL  # do we need to fetch the max level per language?

    return render_template(
        "code-page.html",
        intro_tutorial=True,
        next_level=2,
        level_nr=str(level),
        level=str(level),
        adventures=adventures,
        initial_tab=initial_tab,
        commands=commands,
        quiz=True,
        max_level=max_level,
        parsons=True if parsons else False,
        parsons_exercises=parsons,
        initial_adventure=initial_adventure,
        cheatsheet=cheatsheet,
        blur_button_available=False,
        current_user_is_in_class=len(current_user().get('classes') or []) > 0,
        # See initialize.ts
        javascript_page_options=dict(
            page='code',
            level=level,
            lang=g.lang,
            adventures=adventures,
            initial_tab=initial_tab,
            current_user_name=current_user()['username'],
            start_tutorial=True,
        ))


@app.route('/teacher-tutorial', methods=['GET'])
@requires_teacher
def teacher_tutorial(user):
    teacher_classes = DATABASE.get_teacher_classes(user['username'], True)
    adventures = []
    for adventure in DATABASE.get_teacher_adventures(user['username']):
        adventures.append(
            {'id': adventure.get('id'),
             'name': adventure.get('name'),
             'date': utils.localized_date_format(adventure.get('date')),
             'level': adventure.get('level')
             }
        )

    return render_template('for-teachers.html', current_page='my-profile',
                           page_title=gettext('title_for-teacher'),
                           teacher_classes=teacher_classes,
                           teacher_adventures=adventures,
                           tutorial=True,
                           content=hedyweb.PageTranslations('for-teachers').get_page_translations(g.lang),
                           javascript_page_options=dict(
                               page='for-teachers',
                               tutorial=True,
                           ))


# routing to index.html


@app.route('/hour-of-code/<int:level>', methods=['GET'])
@app.route('/hour-of-code', methods=['GET'], defaults={'level': 1})
def hour_of_code(level, program_id=None):
    try:
        level = int(level)
        if level < 1 or level > hedy.HEDY_MAX_LEVEL:
            return utils.error_page(error=404, ui_message=gettext('no_such_level'))
    except BaseException:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    loaded_program = None
    if program_id:
        result = DATABASE.program_by_id(program_id)
        if not result or not current_user_allowed_to_see_program(result):
            return utils.error_page(error=404, ui_message=gettext('no_such_program'))

        loaded_program = Program.from_database_row(result)

    subset = [adv.strip() for adv in request.args.get("subset", "").strip().split(",")]
    subset = subset if subset[0] else HOUR_OF_CODE_ADVENTURES[level]
    adventures = load_adventures_for_level(level, subset=subset)

    if not adventures:
        return utils.error_page(error=404, ui_message=gettext("no_such_adventure"))

    # Initially all levels are available -> strip those for which conditions
    # are not met or not available yet
    available_levels = list(range(1, hedy.HEDY_MAX_LEVEL + 1))

    customizations = {}
    if current_user()['username']:
        customizations = DATABASE.get_student_class_customizations(current_user()['username'])

    if 'levels' in customizations:
        available_levels = customizations['levels']
        now = timems()
        for current_level, timestamp in customizations.get('opening_dates', {}).items():
            if utils.datetotimeordate(timestamp) > utils.datetotimeordate(utils.mstoisostring(now)):
                try:
                    available_levels.remove(int(current_level))
                except BaseException:
                    print("Error: there is an openings date without a level")

    if 'levels' in customizations and level not in available_levels:
        if available_levels:
            return index(available_levels[0], program_id)
        return utils.error_page(error=403, ui_message=gettext('level_not_class'))

    # At this point we can have the following scenario:
    # - The level is allowed and available
    # - But, if there is a quiz threshold we have to check again if the user has reached it

    if 'level_thresholds' in customizations:
        if 'quiz' in customizations.get('level_thresholds'):
            # Temporary store the threshold
            threshold = customizations.get('level_thresholds').get('quiz')
            # Get the max quiz score of the user in the previous level
            # A bit out-of-scope, but we want to enable the next level button directly after finishing the quiz
            # Todo: How can we fix this without a re-load?
            quiz_stats = DATABASE.get_quiz_stats([current_user()['username']])
            # Only check the quiz threshold if there is a quiz to obtain a score on the previous level
            if level - 1 in available_levels and level > 1 and QUIZZES[g.lang].get_quiz_data_for_level(level - 1):
                scores = [x.get('scores', []) for x in quiz_stats if x.get('level') == level - 1]
                scores = [score for week_scores in scores for score in week_scores]
                max_score = 0 if len(scores) < 1 else max(scores)
                if max_score < threshold:
                    return utils.error_page(
                        error=403, ui_message=gettext('quiz_threshold_not_reached'))

            # We also have to check if the next level should be removed from the available_levels
            # Only check the quiz threshold if there is a quiz to obtain a score on the current level
            if level < hedy.HEDY_MAX_LEVEL and QUIZZES[g.lang].get_quiz_data_for_level(level):
                scores = [x.get('scores', []) for x in quiz_stats if x.get('level') == level]
                scores = [score for week_scores in scores for score in week_scores]
                max_score = 0 if len(scores) < 1 else max(scores)
                # We don't have the score yet for the next level -> remove all upcoming
                # levels from 'available_levels'
                if max_score < threshold:
                    # if this level is currently available, but score is below max score
                    customizations["below_threshold"] = (level + 1 in available_levels)
                    available_levels = available_levels[:available_levels.index(level) + 1]

    # Add the available levels to the customizations dict -> simplify
    # implementation on the front-end
    customizations['available_levels'] = available_levels
    cheatsheet = COMMANDS[g.lang].get_commands_for_level(level, g.keyword_lang)

    load_customized_adventures(level, customizations, adventures)
    load_saved_programs(level, adventures, loaded_program)
    initial_tab = adventures[0].short_name

    if loaded_program:
        # Make sure that there is an adventure(/tab) for a loaded program, otherwise make one
        initial_tab = loaded_program.adventure_name
        if not any(a.short_name == loaded_program.adventure_name for a in adventures):
            adventures.append(Adventure(
                short_name=loaded_program.adventure_name,
                # This is not great but we got nothing better :)
                name=gettext('your_program'),
                text='',
                example_code='',
                editor_contents=loaded_program.code,
                save_name=loaded_program.name,
                is_teacher_adventure=False,
                is_command_adventure=loaded_program.adventure_name in KEYWORDS_ADVENTURES
            ))

    adventures_map = {a.short_name: a for a in adventures}

    enforce_developers_mode = False
    if 'other_settings' in customizations and 'developers_mode' in customizations['other_settings']:
        enforce_developers_mode = True

    hide_cheatsheet = False
    if 'other_settings' in customizations and 'hide_cheatsheet' in customizations['other_settings']:
        hide_cheatsheet = True

    quiz = True if QUIZZES[g.lang].get_quiz_data_for_level(level) else False
    tutorial = True if TUTORIALS[g.lang].get_tutorial_for_level(level) else False

    quiz_questions = 0

    if quiz:
        quiz_questions = len(QUIZZES[g.lang].get_quiz_data_for_level(level))

    if 'other_settings' in customizations and 'hide_quiz' in customizations['other_settings']:
        quiz = False

    max_level = hedy.HEDY_MAX_LEVEL
    level_number = int(level)
    prev_level, next_level = utils.find_prev_next_levels(
        list(available_levels), level_number)

    commands = hedy.commands_per_level.get(level)
    return render_template(
        "code-page.html",
        level_nr=str(level_number),
        level=level_number,
        current_page='Hour of Code',
        max_level=max_level,
        prev_level=prev_level,
        next_level=next_level,
        HOC_tracking_pixel=True,
        customizations=customizations,
        hide_cheatsheet=hide_cheatsheet,
        # enforce_developers_mode=enforce_developers_mode,
        enforce_developers_mode=enforce_developers_mode,
        loaded_program=loaded_program,
        adventures=adventures,
        initial_tab=initial_tab,
        commands=commands,
        # parsons=parsons,
        # parsons_exercises=parson_exercises,
        tutorial=tutorial,
        latest=version(),
        quiz=quiz,
        quiz_questions=quiz_questions,
        cheatsheet=cheatsheet,
        blur_button_available=False,
        initial_adventure=adventures_map[initial_tab],
        current_user_is_in_class=len(current_user().get('classes') or []) > 0,
        # See initialize.ts
        javascript_page_options=dict(
            page='code',
            level=level_number,
            lang=g.lang,
            adventures=adventures,
            initial_tab=initial_tab,
            current_user_name=current_user()['username'],
        ))


# routing to index.html


@app.route('/ontrack', methods=['GET'], defaults={'level': '1', 'program_id': None})
@app.route('/onlinemasters', methods=['GET'], defaults={'level': '1', 'program_id': None})
@app.route('/onlinemasters/<int:level>', methods=['GET'], defaults={'program_id': None})
@app.route('/hedy', methods=['GET'], defaults={'program_id': None, 'level': '1'})
@app.route('/hedy/<int:level>', methods=['GET'], defaults={'program_id': None})
@app.route('/hedy/<int:level>/<program_id>', methods=['GET'])
def index(level, program_id):
    try:
        level = int(level)
        if level < 1 or level > hedy.HEDY_MAX_LEVEL:
            return utils.error_page(error=404, ui_message=gettext('no_such_level'))
    except BaseException:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    loaded_program = None
    if program_id:
        result = DATABASE.program_by_id(program_id)
        if not result or not current_user_allowed_to_see_program(result):
            return utils.error_page(error=404, ui_message=gettext('no_such_program'))

        loaded_program = Program.from_database_row(result)

    adventures = load_adventures_for_level(level)

    # Initially all levels are available -> strip those for which conditions
    # are not met or not available yet
    available_levels = list(range(1, hedy.HEDY_MAX_LEVEL + 1))

    customizations = {}
    if current_user()['username']:
        # class_to_preview is for teachers to preview a class they own
        customizations = DATABASE.get_student_class_customizations(
            current_user()['username'], class_to_preview=session.get("preview_class", {}).get("id"))

    if 'levels' in customizations:
        available_levels = customizations['levels']
        now = timems()
        for current_level, timestamp in customizations.get('opening_dates', {}).items():
            if utils.datetotimeordate(timestamp) > utils.datetotimeordate(utils.mstoisostring(now)):
                try:
                    available_levels.remove(int(current_level))
                except BaseException:
                    print("Error: there is an openings date without a level")

    if 'levels' in customizations and level not in available_levels:
        if available_levels:
            return index(available_levels[0], program_id)
        return utils.error_page(error=403, ui_message=gettext('level_not_class'))

    # At this point we can have the following scenario:
    # - The level is allowed and available
    # - But, if there is a quiz threshold we have to check again if the user has reached it
    if 'level_thresholds' in customizations:
        # If quiz in level and in some of the previous levels, then we check the threshold level.
        check_threshold = 'other_settings' in customizations and 'hide_quiz' not in customizations['other_settings']

        if check_threshold and 'quiz' in customizations.get('level_thresholds'):

            # Temporary store the threshold
            threshold = customizations.get('level_thresholds').get('quiz')
            level_quiz_data = QUIZZES[g.lang].get_quiz_data_for_level(level)
            # Get the max quiz score of the user in the previous level
            # A bit out-of-scope, but we want to enable the next level button directly after finishing the quiz
            # Todo: How can we fix this without a re-load?
            quiz_stats = DATABASE.get_quiz_stats([current_user()['username']])

            previous_quiz_level = level
            for _prev_level in range(level - 1, 0, -1):
                if _prev_level in available_levels and \
                        customizations["sorted_adventures"][str(_prev_level)][-1].get("name") == "quiz" and \
                        not any(x.get("scores") for x in quiz_stats if x.get("level") == _prev_level):
                    previous_quiz_level = _prev_level
                    break

            # Not current leve-quiz's data because some levels may have no data for quizes,
            # but we still need to check for the threshold.
            if level - 1 in available_levels and level > 1 and \
                    (not level_quiz_data or QUIZZES[g.lang].get_quiz_data_for_level(level - 1)):

                # Only if we have found a quiz in previous levels with quiz data, we check the threshold.
                if previous_quiz_level < level:
                    # scores = [x.get('scores', []) for x in quiz_stats if x.get('level') == level - 1]
                    scores = [x.get('scores', []) for x in quiz_stats if x.get('level') == previous_quiz_level]
                    scores = [score for week_scores in scores for score in week_scores]
                    max_score = 0 if len(scores) < 1 else max(scores)
                    if max_score < threshold:
                        # Instead of sending this level isn't available, we could send them to the right level?!
                        # return redirect(f"/hedy/{previous_quiz_level}")
                        return utils.error_page(
                            error=403, ui_message=gettext('quiz_threshold_not_reached'))

            # We also have to check if the next level should be removed from the available_levels
            # Only check the quiz threshold if there is a quiz to obtain a score on the current level
            if level <= hedy.HEDY_MAX_LEVEL and level_quiz_data:
                next_level_with_quiz = level - 1
                for _next_level in range(level, hedy.HEDY_MAX_LEVEL):
                    # find the next level whose quiz isn't answered.
                    if _next_level in available_levels and \
                            customizations["sorted_adventures"][str(_next_level)][-1].get("name") == "quiz" and \
                            not any(x.get("scores") for x in quiz_stats if x.get("level") == _next_level):
                        next_level_with_quiz = _next_level
                        break

                # If the next quiz is in the current or upcoming level,
                # we attempt to adjust available levels beginning from that level.
                # e.g., student2 completed quiz 2, levels 3,4 and 5 have not quizes, 6 does.
                # We should start from that level. If next_level_with_quiz >= level,
                # meaning we don't need to adjust available levels ~ all available/quizes done!
                if next_level_with_quiz >= level:
                    scores = [x.get('scores', []) for x in quiz_stats if x.get('level') == next_level_with_quiz]
                    scores = [score for week_scores in scores for score in week_scores]
                    max_score = 0 if len(scores) < 1 else max(scores)
                    # We don't have the score yet for the next level -> remove all upcoming
                    # levels from 'available_levels'
                    if max_score < threshold:
                        # if this level is currently available, but score is below max score
                        customizations["below_threshold"] = (next_level_with_quiz + 1 in available_levels)
                        available_levels = available_levels[:available_levels.index(next_level_with_quiz) + 1]

    # Add the available levels to the customizations dict -> simplify
    # implementation on the front-end
    customizations['available_levels'] = available_levels
    cheatsheet = COMMANDS[g.lang].get_commands_for_level(level, g.keyword_lang)

    load_customized_adventures(level, customizations, adventures)
    load_saved_programs(level, adventures, loaded_program)
    initial_tab = adventures[0].short_name

    if loaded_program:
        # Make sure that there is an adventure(/tab) for a loaded program, otherwise make one
        initial_tab = loaded_program.adventure_name
        if not any(a.short_name == loaded_program.adventure_name for a in adventures):
            adventures.append(Adventure(
                short_name=loaded_program.adventure_name,
                # This is not great but we got nothing better :)
                name=gettext('your_program'),
                text='',
                example_code='',
                editor_contents=loaded_program.code,
                save_name=loaded_program.name,
                is_teacher_adventure=False,
                is_command_adventure=loaded_program.adventure_name in KEYWORDS_ADVENTURES
            ))

    adventures_map = {a.short_name: a for a in adventures}

    enforce_developers_mode = False
    if 'other_settings' in customizations and 'developers_mode' in customizations['other_settings']:
        enforce_developers_mode = True

    hide_cheatsheet = False
    if 'other_settings' in customizations and 'hide_cheatsheet' in customizations['other_settings']:
        hide_cheatsheet = True

    parsons = True if PARSONS[g.lang].get_parsons_data_for_level(level) else False
    quiz = True if QUIZZES[g.lang].get_quiz_data_for_level(level) else False
    tutorial = True if TUTORIALS[g.lang].get_tutorial_for_level(level) else False

    quiz_questions = 0
    parson_exercises = 0

    if quiz:
        quiz_questions = len(QUIZZES[g.lang].get_quiz_data_for_level(level))
    if parsons:
        parson_exercises = len(PARSONS[g.lang].get_parsons_data_for_level(level))

    parsons_hidden = 'other_settings' in customizations and 'hide_parsons' in customizations['other_settings']
    quizzes_hidden = 'other_settings' in customizations and 'hide_quiz' in customizations['other_settings']

    if customizations:
        for_teachers.ForTeachersModule.migrate_quizzes_parsons_tabs(customizations, parsons_hidden, quizzes_hidden)

    parsons_in_level = True
    quiz_in_level = True
    if customizations.get("sorted_adventures") and\
            len(customizations.get("sorted_adventures", {str(level): []})[str(level)]) > 2:
        last_two_adv_names = [adv["name"] for adv in customizations["sorted_adventures"][str(level)][-2:]]
        parsons_in_level = "parsons" in last_two_adv_names
        quiz_in_level = "quiz" in last_two_adv_names

    if not parsons_in_level or parsons_hidden:
        parsons = False
    if not quiz_in_level or quizzes_hidden:
        quiz = False

    max_level = hedy.HEDY_MAX_LEVEL
    level_number = int(level)
    prev_level, next_level = utils.find_prev_next_levels(
        list(available_levels), level_number)

    commands = hedy.commands_per_level.get(level)
    return render_template(
        "code-page.html",
        level_nr=str(level_number),
        level=level_number,
        current_page='hedy',
        max_level=max_level,
        prev_level=prev_level,
        next_level=next_level,
        customizations=customizations,
        hide_cheatsheet=hide_cheatsheet,
        enforce_developers_mode=enforce_developers_mode,
        loaded_program=loaded_program,
        adventures=adventures,
        initial_tab=initial_tab,
        commands=commands,
        parsons=parsons,
        parsons_exercises=parson_exercises,
        tutorial=tutorial,
        latest=version(),
        quiz=quiz,
        quiz_questions=quiz_questions,
        cheatsheet=cheatsheet,
        blur_button_available=False,
        initial_adventure=adventures_map[initial_tab],
        current_user_is_in_class=len(current_user().get('classes') or []) > 0,
        microbit_feature=MICROBIT_FEATURE,
        # See initialize.ts
        javascript_page_options=dict(
            page='code',
            level=level_number,
            lang=g.lang,
            adventures=adventures,
            initial_tab=initial_tab,
            current_user_name=current_user()['username'],
        ))


@app.route('/hedy', methods=['GET'])
def index_level():
    if current_user()['username']:
        highest_quiz = get_highest_quiz_level(current_user()['username'])
        # This function returns the character '-' in case there are no finished quizes
        if highest_quiz == '-':
            level_rendered = 1
        elif highest_quiz == hedy.HEDY_MAX_LEVEL:
            level_rendered = hedy.HEDY_MAX_LEVEL
        else:
            level_rendered = highest_quiz + 1
        return index(level_rendered, None)
    else:
        return index(1, None)


@app.route('/hedy/<id>/view', methods=['GET'])
@requires_login
def view_program(user, id):
    result = DATABASE.program_by_id(id)

    if not result or not current_user_allowed_to_see_program(result):
        return utils.error_page(error=404, ui_message=gettext('no_such_program'))

    # The program is valid, verify if the creator also have a public profile
    result['public_profile'] = True if DATABASE.get_public_profile_settings(
        result['username']) else None

    code = result['code']
    if result.get("lang") != "en" and result.get("lang") in ALL_KEYWORD_LANGUAGES.keys():
        code = hedy_translation.translate_keywords(code, from_lang=result.get(
            'lang'), to_lang="en", level=int(result.get('level', 1)))
    # If the keyword language is non-English -> parse again to guarantee
    # completely localized keywords
    if g.keyword_lang != "en":
        code = hedy_translation.translate_keywords(
            code,
            from_lang="en",
            to_lang=g.keyword_lang,
            level=int(
                result.get(
                    'level',
                    1)))

    result['code'] = code

    arguments_dict = {}
    arguments_dict['program_id'] = id
    arguments_dict['page_title'] = f'{result["name"]} – Hedy'
    arguments_dict['level'] = result['level']  # Necessary for running
    arguments_dict['initial_adventure'] = dict(result,
                                               editor_contents=code,
                                               )
    arguments_dict['editor_readonly'] = True

    if "submitted" in result and result['submitted']:
        arguments_dict['show_edit_button'] = False
        arguments_dict['program_timestamp'] = utils.localized_date_format(result['date'])
    else:
        arguments_dict['show_edit_button'] = True

    # Everything below this line has nothing to do with this page and it's silly
    # that every page needs to put in so much effort to re-set it

    return render_template("view-program-page.html",
                           blur_button_available=True,
                           javascript_page_options=dict(
                               page='view-program',
                               lang=g.lang,
                               level=int(result['level']),
                               code=code),
                           is_teacher=user['is_teacher'],
                           **arguments_dict)


@app.route('/render_code/<level>/', methods=['GET'])
def render_code_in_editor(level):
    code = request.args['code']

    try:
        level = int(level)
        if level == 0:  # in level 0, the intro slides, we use codes from level 1
            level = 1
    except BaseException:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    if session.get("previous_keyword_lang"):
        code = hedy_translation.translate_keywords(
            code, session["previous_keyword_lang"], g.keyword_lang, level=int(level))

    a = Adventure(
        short_name='start',
        name='start',
        text='start',
        save_name='start',
        editor_contents=code)
    adventures = [a]

    return render_template("code-page.html",
                           specific_adventure=True,
                           level_nr=str(level),
                           level=level,
                           adventures=adventures,
                           raw=True,
                           menu=False,
                           blur_button_available=False,
                           # See initialize.ts
                           javascript_page_options=dict(
                               page='code',
                               lang=g.lang,
                               level=level,
                               adventures=adventures,
                               initial_tab='start',
                               current_user_name=current_user()['username'],
                               suppress_save_and_load_for_slides=True,
                           ))


@app.route('/adventure/<name>', methods=['GET'], defaults={'level': 1, 'mode': 'full'})
@app.route('/adventure/<name>/<level>', methods=['GET'], defaults={'mode': 'full'})
@app.route('/adventure/<name>/<level>/<mode>', methods=['GET'])
def get_specific_adventure(name, level, mode):
    try:
        level = int(level)
    except BaseException:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    adventures = [x for x in load_adventures_for_level(level) if x.short_name == name]
    customizations = {}
    prev_level = None  # we are not rendering buttons in raw, no lookup needed here
    next_level = None
    if not adventures:
        # By adventure's name and creator; since an adventure can be clone in /public-adventures
        if request.args.get("creator"):
            user = DATABASE.user_by_username(request.args["creator"])
        else:
            user = current_user()
        adventure = None
        if user and is_teacher(user):
            adventure = database.ADVENTURES.get({"name": name, "creator": user["username"]})

        if not adventure:
            return utils.error_page(error=404, ui_message=gettext('no_such_adventure'))

        available_levels = adventure["levels"] if adventure.get("levels") else [adventure["level"]]

        customizations["available_levels"] = [int(adv_level) for adv_level in available_levels]
        if level not in customizations["available_levels"]:
            return utils.error_page(error=404, ui_message=gettext('no_such_adventure'))

        adventure["content"] = safe_format(adventure.get("content", ""), **hedy_content.KEYWORDS.get(g.keyword_lang))
        customizations["teachers_adventure"] = True

        current_adventure = Adventure(
            id=adventure["id"],
            author=adventure["creator"],
            short_name="level",
            name=adventure["name"],
            image=adventure.get("image", None),
            text=adventure["content"],
            is_teacher_adventure=True,
            is_command_adventure=False,
            save_name=f"{name} {level}")

        adventures.append(current_adventure)
        prev_level, next_level = utils.find_prev_next_levels(customizations["available_levels"], level)

    # Add the commands to enable the language switcher dropdown
    commands = hedy.commands_per_level.get(level)
    raw = mode == 'raw'
    initial_tab = name
    initial_adventure = adventures[0]

    return render_template("code-page.html",
                           specific_adventure=True,
                           level_nr=str(level),
                           commands=commands,
                           level=level,
                           prev_level=prev_level,
                           next_level=next_level,
                           #    max_level=max_level,
                           customizations=customizations,
                           hide_cheatsheet=None,
                           enforce_developers_mode=None,
                           teacher_adventures=[],
                           adventures=adventures,
                           initial_tab=initial_tab,
                           initial_adventure=initial_adventure,
                           latest=version(),
                           raw=raw,
                           menu=not raw,
                           blur_button_available=False,
                           current_user_is_in_class=len(current_user().get('classes') or []) > 0,
                           # See initialize.ts
                           javascript_page_options=dict(

                               page='code',
                               lang=g.lang,
                               level=level,
                               adventures=adventures,
                               initial_tab='',
                               current_user_name=current_user()['username'],
                           ))


@app.route('/embedded/<int:level>', methods=['GET'])
def get_embedded_code_editor(level):
    forget_current_user()

    # Start with an empty program
    program = ''

    # If for any reason the level is invalid, set to level 1
    try:
        level = int(level)
        if level < 1 or level > hedy.HEDY_MAX_LEVEL:
            program = gettext('invalid_level_comment')
            level = 1
    except ValueError:
        program = gettext('invalid_level_comment')
        level = 1

    run = True if request.args.get('run') == 'true' else False
    fullWidth = True if request.args.get('fullWidth') == 'true' else False
    readOnly = True if request.args.get('readOnly') == 'true' else False
    encoded_program = request.args.get('program')

    # Set a fallback for default use
    language = request.args.get('lang', 'en')
    if language not in ALL_LANGUAGES.keys():
        language = 'nl'
        program = gettext('invalid_language_comment')

    keyword_language = request.args.get('keyword', 'en')
    if keyword_language not in ALL_KEYWORD_LANGUAGES.keys():
        language = 'en'
        program = gettext('invalid_keyword_language_comment')

    # Make sure to set the session lang to enforce the correct translated strings to be rendered
    session['lang'] = language

    if encoded_program and not program:
        try:
            program = base64.b64decode(encoded_program)
            program = program.decode('utf-8')
        except binascii.Error:
            program = gettext('invalid_program_comment')

    return render_template("embedded-editor.html", fullWidth=fullWidth, run=run, language=language,
                           keyword_language=keyword_language, readOnly=readOnly,
                           level=level, javascript_page_options=dict(
                               page='view-program',
                               lang=language,
                               level=level,
                               code=program
                           ))


@app.route('/cheatsheet/', methods=['GET'], defaults={'level': 1})
@app.route('/cheatsheet/<level>', methods=['GET'])
def get_cheatsheet_page(level):
    try:
        level = int(level)
        if level < 1 or level > hedy.HEDY_MAX_LEVEL:
            return utils.error_page(error=404, ui_message=gettext('no_such_level'))
    except BaseException:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    commands = COMMANDS[g.lang].get_commands_for_level(level, g.keyword_lang)

    return render_template("printable/cheatsheet.html", commands=commands, level=level)


@app.route('/certificate/<username>', methods=['GET'])
def get_certificate_page(username):
    if not current_user()['username']:
        return utils.error_page(error=401, ui_message=gettext('unauthorized'))
    username = username.lower()
    user = DATABASE.user_by_username(username)
    if not user:
        return utils.error_page(error=403, ui_message=gettext('user_inexistent'))
    progress_data = DATABASE.progress_by_username(username)
    if progress_data is None:
        return utils.error_page(error=404, ui_message=gettext('no_certificate'))
    achievements = progress_data.get('achieved', None)
    if achievements is None:
        return utils.error_page(error=404, ui_message=gettext('no_certificate'))
    if 'run_programs' in progress_data:
        count_programs = progress_data['run_programs']
    else:
        count_programs = 0
    quiz_score = get_highest_quiz_score(username)
    quiz_level = get_highest_quiz_level(username)
    longest_program = get_longest_program(username)

    number_achievements = len(achievements)
    congrats_message = safe_format(gettext('congrats_message'), username=username)
    return render_template("printable/certificate.html", count_programs=count_programs, quiz_score=quiz_score,
                           longest_program=longest_program, number_achievements=number_achievements,
                           quiz_level=quiz_level, congrats_message=congrats_message)


def get_highest_quiz_level(username):
    quiz_scores = DATABASE.get_quiz_stats([username])
    # Verify if the user did finish any quiz before getting the max() of the finished levels
    finished_quizzes = any("finished" in x for x in quiz_scores)
    return max([x.get("level") for x in quiz_scores if x.get("finished")]) if finished_quizzes else "-"


def get_highest_quiz_score(username):
    max = 0
    quizzes = DATABASE.get_quiz_stats([username])
    for q in quizzes:
        for score in q.get('scores', []):
            if score > max:
                max = score
    return max


def get_longest_program(username):
    programs = DATABASE.get_program_stats([username])
    highest = 0
    for program in programs:
        if 'number_of_lines' in program:
            highest = max(highest, program['number_of_lines'])
    return highest


@app.errorhandler(404)
def not_found(exception):
    return utils.error_page(error=404, ui_message=gettext('page_not_found'))


@app.errorhandler(500)
def internal_error(exception):
    import traceback
    print(traceback.format_exc())
    return utils.error_page(error=500, exception=exception)


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
    return render_template(
        'recover.html',
        page_title=gettext('title_recover'),
        current_page='login')


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
        return utils.error_page(error=401, ui_message=gettext('unauthorized'))
    return render_template(
        'reset.html',
        page_title=gettext('title_reset'),
        reset_username=username,
        reset_token=token,
        current_page='login')


@app.route('/my-profile', methods=['GET'])
@requires_login_redirect
def profile_page(user):
    profile = DATABASE.user_by_username(user['username'])
    programs = DATABASE.filtered_programs_for_user(user['username'], public=True)
    public_profile_settings = DATABASE.get_public_profile_settings(current_user()['username'])

    classes = []
    if profile.get('classes'):
        for class_id in profile.get('classes'):
            classes.append(DATABASE.get_class(class_id))

    invitations = DATABASE.get_user_invitations(user['username'])
    if invitations:
        session['messages'] = len(invitations)
        # If there are invitations: retrieve the class information
        for invite in invitations:
            class_info = DATABASE.get_class(invite.get('class_id', None))
            if class_info:
                invite['teacher'] = class_info.get('teacher')
                invite['class_name'] = class_info.get('name')
                invite['join_link'] = class_info.get('link')
    else:
        session['messages'] = 0

    return render_template(
        'profile.html',
        page_title=gettext('title_my-profile'),
        programs=programs,
        user_data=profile,
        invitations=invitations,
        public_settings=public_profile_settings,
        user_classes=classes,
        current_page='my-profile',
        javascript_page_options=dict(
            page='my-profile',
        ))


@app.route('/research/<filename>', methods=['GET'])
def get_research(filename):
    return send_from_directory('content/research/', filename)


@app.route('/favicon.ico')
def favicon():
    abort(404)


@app.route('/')
@app.route('/index.html')
def main_page():
    sections = hedyweb.PageTranslations('start').get_page_translations(g.lang)['home-sections']

    sections = sections[:]

    # Sections have 'title', 'text'
    # Annotate sections with display styles, based on the order which we know sections will appear
    # Styles are one of: 'block', 'pane-with-image-{left,right}', 'columns'
    # Do this by mutating the list in place
    content = []
    content.append(dict(style='block', **sections.pop(0)))

    section_images = [
        '/images/hedy-multilang.png',
        '/images/hedy-grows.png',
        '/images/hedy-classroom.png'
    ]

    for i, image in enumerate(section_images):
        if not sections:
            break
        content.append(dict(
            style='pane-with-image-' + ('right' if i % 2 == 0 else 'left'),
            image=image,
            **sections.pop(0)))

    if sections:
        content.append(dict(style='block', **sections.pop(0)))
    if sections:
        content.append(dict(style='columns', columns=sections))

    custom_logo = False
    if os.path.isfile(f'static/images/hero-graphic/hero-graphic-{g.lang}.png'):
        custom_logo = True

    user = current_user()

    return render_template('main-page.html', page_title=gettext('title_start'), custom_logo=custom_logo,
                           current_page='start', content=content, user=user)


@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html', current_page='subscribe')


@app.route('/learn-more')
def learn_more():
    learn_more_translations = hedyweb.PageTranslations('learn-more').get_page_translations(g.lang)
    return render_template(
        'learn-more.html',
        papers=hedy_content.RESEARCH,
        page_title=gettext('title_learn-more'),
        current_page='learn-more',
        content=learn_more_translations)


@app.route('/join')
def join():
    join_translations = hedyweb.PageTranslations('join').get_page_translations(g.lang)
    return render_template('join.html', page_title=gettext('title_learn-more'),
                           current_page='join', content=join_translations)


@app.route('/start')
def start():
    start_translations = hedyweb.PageTranslations('start').get_page_translations(g.lang)
    return render_template('start.html', page_title=gettext('title_learn-more'),
                           current_page='start', content=start_translations)


@app.route('/privacy')
def privacy():
    privacy_translations = hedyweb.PageTranslations('privacy').get_page_translations(g.lang)
    return render_template('privacy.html', page_title=gettext('title_privacy'),
                           content=privacy_translations)


@app.route('/landing-page/', methods=['GET'], defaults={'first': False})
@app.route('/landing-page/<first>', methods=['GET'])
@requires_login
def landing_page(user, first):
    username = user['username']

    user_info = DATABASE.get_public_profile_settings(username)
    user_programs = DATABASE.programs_for_user(username)
    # Only return the last program of the user
    if user_programs:
        user_programs = user_programs[:1][0]
    user_achievements = DATABASE.progress_by_username(username)

    return render_template(
        'landing-page.html',
        first_time=True if first else False,
        page_title=gettext('title_landing-page'),
        user=user['username'],
        user_info=user_info,
        program=user_programs,
        achievements=user_achievements)


@app.route('/explore', methods=['GET'])
def explore():
    if not current_user()['username']:
        return redirect('/login')

    level = try_parse_int(request.args.get('level', default=None, type=str))
    adventure = request.args.get('adventure', default=None, type=str)
    language = g.lang

    achievement = None
    if level or adventure or language:
        achievement = ACHIEVEMENTS.add_single_achievement(
            current_user()['username'], "indiana_jones")

    programs = DATABASE.get_public_programs(
        limit=40,
        level_filter=level,
        language_filter=language,
        adventure_filter=adventure)
    favourite_programs = DATABASE.get_hedy_choices()

    # Do 'normalize_public_programs' on both sets at once, to save database calls
    normalized = normalize_public_programs(list(programs) + list(favourite_programs.records))
    programs, favourite_programs = split_at(len(programs), normalized)

    # Filter out programs that are Hedy favorite choice.
    programs = [program for program in programs if program['id'] not in {fav['id'] for fav in favourite_programs}]

    keyword_lang = g.keyword_lang
    adventures_names = hedy_content.Adventures(session['lang']).get_adventure_names(keyword_lang)

    return render_template(
        'explore.html',
        programs=programs,
        favourite_programs=favourite_programs,
        filtered_level=str(level) if level else None,
        achievement=achievement,
        filtered_adventure=adventure,
        filtered_lang=language,
        max_level=hedy.HEDY_MAX_LEVEL,
        adventures_names=adventures_names,
        page_title=gettext('title_explore'),
        current_page='explore')


def normalize_public_programs(programs):
    """Normalize the content for all programs in the given array, for showing on the /explore or /user page.

    Does the following thing:

    - Try to compile and add 'error' field to show if this worked
    - Adds public_user: True|None fields to each program
    - Preprocess keywords into the current language
    - Turn 'hedy_choice' from an integer into a boolean
    - Change 'code' to only show the first 4 lines
    - Add 'number_lines'
    """
    ret = []
    for program in programs:
        program = pre_process_explore_program(program)

        ret.append(dict(program,
                        hedy_choice=True if program.get('hedy_choice') == 1 else False,
                        code="\n".join(program['code'].split("\n")[:4]),
                        number_lines=program['code'].count('\n') + 1))
    DATABASE.add_public_profile_information(ret)
    return ret


@querylog.timed
def pre_process_explore_program(program):
    # If program does not have an error value set -> parse it and set value
    if 'error' not in program:
        try:
            hedy.transpile(program.get('code'), program.get('level'), program.get('lang'))
            program['error'] = False
        except BaseException:
            program['error'] = True
        DATABASE.store_program(program)

    return program


@app.route('/highscores', methods=['GET'], defaults={'filter': 'global'})
@app.route('/highscores/<filter>', methods=['GET'])
@requires_login
def get_highscores_page(user, filter):
    if filter not in ["global", "country", "class"]:
        return utils.error_page(error=404, ui_message=gettext('page_not_found'))

    user_data = DATABASE.user_by_username(user['username'])
    public_profile = True if DATABASE.get_public_profile_settings(user['username']) else False
    classes = list(user_data.get('classes', set()))
    country = user_data.get('country')
    user_country = COUNTRIES.get(country)

    if filter == "global":
        highscores = DATABASE.get_highscores(user['username'], filter)
    elif filter == "country":
        # Can't get a country highscore if you're not in a country!
        if not country:
            return utils.error_page(error=403, ui_message=gettext('no_such_highscore'))
        highscores = DATABASE.get_highscores(user['username'], filter, country)
    elif filter == "class":
        # Can't get a class highscore if you're not in a class!
        if not classes:
            return utils.error_page(error=403, ui_message=gettext('no_such_highscore'))
        highscores = DATABASE.get_highscores(user['username'], filter, classes[0])

    # Make a deepcopy if working locally, otherwise the local database values
    # are by-reference and overwritten
    if not os.getenv('NO_DEBUG_MODE'):
        highscores = copy.deepcopy(highscores)
    for highscore in highscores:
        highscore['country'] = highscore.get('country') if highscore.get('country') else "-"
        highscore['last_achievement'] = utils.delta_timestamp(highscore.get('last_achievement'))
    return render_template(
        'highscores.html',
        highscores=highscores,
        has_country=True if country else False,
        filter=filter,
        user_country=user_country,
        public_profile=public_profile,
        in_class=True if classes else False)


@app.route('/change_language', methods=['POST'])
def change_language():
    body = request.json
    session['lang'] = body.get('lang')
    # Remove 'keyword_lang' from session, it will automatically be renegotiated from 'lang'
    # on the next page load.
    session.pop('keyword_lang')
    return jsonify({'success': 204})


@app.route('/slides', methods=['GET'], defaults={'level': '1'})
@app.route('/slides/<level>', methods=['GET'])
def get_slides(level):
    # In case of a "forced keyword language" -> load that one, otherwise: load
    # the one stored in the g object

    keyword_language = request.args.get('keyword_language', default=g.keyword_lang, type=str)

    try:
        level = int(level)
    except ValueError:
        return utils.error_page(error=404, ui_message="Slides do not exist!")

    if not SLIDES[g.lang].get_slides_for_level(level, keyword_language):
        return utils.error_page(error=404, ui_message="Slides do not exist!")

    slides = SLIDES[g.lang].get_slides_for_level(level, keyword_language)
    return render_template('slides.html', level=level, slides=slides)


@app.route('/translate_keywords', methods=['POST'])
def translate_keywords():
    body = request.json
    try:
        translated_code = hedy_translation.translate_keywords(body.get('code'), body.get(
            'start_lang'), body.get('goal_lang'), level=int(body.get('level', 1)))
        if translated_code or translated_code == '':  # empty string is False, so explicitly allow it
            session["previous_keyword_lang"] = body.get("start_lang")
            session["keyword_lang"] = body.get("goal_lang")
            return jsonify({'success': 200, 'code': translated_code})
        else:
            return gettext('translate_error'), 400
    except BaseException:
        return gettext('translate_error'), 400


# TODO TB: Think about changing this to sending all steps to the front-end at once
@app.route('/get_tutorial_step/<level>/<step>', methods=['GET'])
def get_tutorial_translation(level, step):
    # Keep this structure temporary until we decide on a nice code / parse structure
    if step == "code_snippet":
        code = hedy_content.deep_translate_keywords(gettext('tutorial_code_snippet'), g.keyword_lang)
        return jsonify({'code': code}), 200
    try:
        step = int(step)
    except ValueError:
        return gettext('invalid_tutorial_step'), 400

    data = TUTORIALS[g.lang].get_tutorial_for_level_step(level, step, g.keyword_lang)
    if not data:
        data = {'title': gettext('tutorial_title_not_found'),
                'text': gettext('tutorial_message_not_found')}
    return jsonify(data), 200


@app.route('/store_parsons_order', methods=['POST'])
def store_parsons_order():
    body = request.json
    # Validations
    if not isinstance(body, dict):
        return 'body must be an object', 400
    if not isinstance(body.get('level'), int):
        return 'level must be an integer', 400
    if not isinstance(body.get('exercise'), str):
        return 'exercise must be a string', 400
    if not isinstance(body.get('order'), list):
        return 'order must be a list', 400

    attempt = {
        'id': utils.random_id_generator(12),
        'username': current_user()['username'] or f'anonymous:{utils.session_id()}',
        'level': int(body['level']),
        'exercise': int(body['exercise']),
        'order': body['order'],
        'correct': 1 if body['correct'] else 0,
        'timestamp': utils.timems()
    }

    DATABASE.store_parsons(attempt)
    return make_response('', 204)


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


@app.template_global()
def translate_command(command):
    # Return the translated command found in KEYWORDS, if not found return the command itself
    return hedy_content.KEYWORDS[g.lang].get(command, command)


@app.template_filter()
def markdown_retain_newlines(x):
    """Force newlines in to the input MarkDown string to be rendered as <br>"""
    # This works by adding two spaces before every newline. That's a signal to MarkDown
    # that the newlines should be forced.
    #
    # Nobody is going to type this voluntarily to distinguish between linebreaks line by
    # line, but you can use this filter to do this for all line breaks.
    return x.replace('\n', '  \n')


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


SLUGIFY_RE = re.compile('[^a-z0-9_]+')


@app.template_filter()
def slugify(s):
    """Convert arbitrary text into a text that's safe to use in a URL."""
    if s is None:
        return None
    return SLUGIFY_RE.sub('-', strip_accents(s).lower())


@app.template_filter()
def chunk(x, size):
    """Chunk a list into groups of size at most 'size'."""
    return (x[pos:pos + size] for pos in range(0, len(x), size))


@app.template_filter()
def format_date(date):
    if not isinstance(date, int):
        return date
    return utils.localized_date_format(date)


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
def other_languages(lang_param=None):
    """Return a list of language objects that are NOT the current language."""
    current_lang = lang_param or g.lang
    return [make_lang_obj(lang) for lang in ALL_LANGUAGES.keys() if lang != current_lang]


@app.template_global()
def lang_to_sym(lang):
    return ALL_LANGUAGES[lang]


@app.template_global()
def other_keyword_languages():
    """Return a list of language objects that are NOT the current language, and that have translated keywords."""
    current_lang = g.lang
    return [make_lang_obj(lang) for lang in ALL_KEYWORD_LANGUAGES.keys() if lang != current_lang]


@app.template_global()
def keyword_languages():
    """Return a list of language objects that have translated keywords."""
    return [make_lang_obj(lang) for lang in ALL_KEYWORD_LANGUAGES.keys()]


@app.template_global()
def keyword_languages_keys():
    """Return the language codes for all languages that have translated keywords."""
    return [lang for lang in ALL_KEYWORD_LANGUAGES.keys()]


@app.template_global()
def get_country(country):
    return COUNTRIES.get(country, "-")


@app.template_global()
# If the current user language supports localized keywords: return this value, else: english
def get_syntax_language(lang):
    if lang in ALL_KEYWORD_LANGUAGES.keys():
        return lang
    else:
        return "en"


@app.template_global()
def parse_keyword(keyword):
    return hedy_content.KEYWORDS.get(g.keyword_lang).get(keyword)


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

    return '{}?{}'.format(request.path, quote_plus(args))


@app.template_global()
def get_user_messages():
    if not session.get('messages'):
        # Todo TB: In the future this should contain the class invites + other messages
        # As the class invites are binary (you either have one or you have none, we can possibly simplify this)
        # Simply set it to 1 if we have an invite, otherwise keep at 0
        invitations = DATABASE.get_user_invitations(current_user()['username'])
        session['messages'] = len(invitations) if invitations else 0
    if session.get('messages') > 0:
        return session.get('messages')
    return None


app.add_template_global(utils.prepare_content_for_ckeditor, name="prepare_content_for_ckeditor")


# Todo TB: Re-write this somewhere sometimes following the line below
# We only store this @app.route here to enable the use of achievements ->
# might want to re-write this in the future


@app.route('/auth/public_profile', methods=['POST'])
@requires_login
def update_public_profile(user):
    body = request.json

    # Validations
    if not isinstance(body, dict):
        return gettext('ajax_error'), 400
    # The images are given as a "picture id" from 1 till 12
    if not isinstance(body.get('image'), str) or int(body.get('image'), 0) not in [*range(1, 13)]:
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
        achievement = ACHIEVEMENTS.add_single_achievement(current_user()['username'], "go_live")

    # Make sure the session value for the profile image is up-to-date
    session['profile_image'] = body.get('image')

    # If there is no current profile or if it doesn't have the tags list ->
    # check if the user is a teacher / admin
    if not current_profile or not current_profile.get('tags'):
        body['tags'] = []
        if is_teacher(user):
            body['tags'].append('teacher')
        if is_admin(user):
            body['tags'].append('admin')

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

    return Response(dump_yaml_rt(data), mimetype='application/x-yaml',
                    headers={'Content-disposition': 'attachment; filename=' + request.form['file'].replace('/', '-')})


@app.route('/user/<username>')
def public_user_page(username):
    if not current_user()['username']:
        return utils.error_page(error=401, ui_message=gettext('unauthorized'))
    username = username.lower()
    user = DATABASE.user_by_username(username)
    if not user:
        return utils.error_page(error=404, ui_message=gettext('user_not_private'))
    user_public_info = DATABASE.get_public_profile_settings(username)
    page = request.args.get('page', default=None, type=str)

    keyword_lang = g.keyword_lang
    adventure_names = hedy_content.Adventures(g.lang).get_adventure_names(keyword_lang)
    swapped_adventure_names = {value: key for key, value in adventure_names.items()}

    level = request.args.get('level', default=None, type=str) or None
    adventure = request.args.get('adventure', default=None, type=str) or None

    if user_public_info:
        user_programs = DATABASE.filtered_programs_for_user(username,
                                                            level=level,
                                                            adventure=swapped_adventure_names.get(adventure),
                                                            public=True,
                                                            limit=10,
                                                            pagination_token=page)
        next_page_token = user_programs.next_page_token
        user_programs = normalize_public_programs(user_programs)
        user_achievements = DATABASE.progress_by_username(username) or {}

        all_programs = DATABASE.filtered_programs_for_user(username,
                                                           public=True,
                                                           pagination_token=page)

        sorted_level_programs = hedy_content.Adventures(
            g.lang).get_sorted_level_programs(all_programs, adventure_names)
        sorted_adventure_programs = hedy_content.Adventures(
            g.lang).get_sorted_adventure_programs(all_programs, adventure_names)

        favorite_program = None
        if 'favourite_program' in user_public_info and user_public_info['favourite_program']:
            favorite_program = DATABASE.program_by_id(
                user_public_info['favourite_program'])

        last_achieved = None
        if user_achievements.get('achieved'):
            last_achieved = user_achievements['achieved'][-1]
        certificate_message = safe_format(gettext('see_certificate'), username=username)
        print(user_programs)
        # Todo: TB -> In the near future: add achievement for user visiting their own profile
        next_page_url = url_for(
            'public_user_page',
            username=username, **dict(request.args,
                                      page=next_page_token)) if next_page_token else None

        user = DATABASE.user_by_username(username)
        if user.get('program_count'):
            user_program_count = user.get('program_count')
        else:
            user_program_count = 0

        return render_template(
            'public-page.html',
            user_info=user_public_info,
            achievements=ACHIEVEMENTS_TRANSLATIONS.get_translations(
                g.lang).get('achievements'),
            favorite_program=favorite_program,
            programs=user_programs,
            last_achieved=last_achieved,
            user_achievements=user_achievements,
            certificate_message=certificate_message,
            next_page_url=next_page_url,
            sorted_level_programs=sorted_level_programs,
            sorted_adventure_programs=sorted_adventure_programs,
            user_program_count=user_program_count,
        )
    return utils.error_page(error=404, ui_message=gettext('user_not_private'))


def valid_invite_code(code):
    if not code:
        return False

    # Get the value from the environment, use literal_eval to convert from
    # string list to an actual list
    valid_codes = []
    if os.getenv('TEACHER_INVITE_CODE'):
        valid_codes.append(os.getenv('TEACHER_INVITE_CODE'))
    if os.getenv('TEACHER_INVITE_CODES'):
        valid_codes.extend(os.getenv('TEACHER_INVITE_CODES').split(','))

    return code in valid_codes


@app.route('/invite/<code>', methods=['GET'])
def teacher_invitation(code):
    user = current_user()

    if not valid_invite_code(code):
        return utils.error_page(error=404, ui_message=gettext('invalid_teacher_invitation_code'))

    if not user['username']:
        return render_template('teacher-invitation.html')

    admin.update_is_teacher(DATABASE, user)
    # When visiting this link we update the current user to a teacher -> also update user in session
    session.get('user')['is_teacher'] = True

    session['welcome-teacher'] = True
    url = request.url.replace(f'/invite/{code}', '/for-teachers')
    return redirect(url)


def current_user_allowed_to_see_program(program):
    """Check if the current user is allowed to see the given program.

    Verify that the program is either public, the current user is the
    creator, teacher or the user is admin.
    """
    user = current_user()

    # These are all easy
    if program.get('public'):
        return True
    if user['username'] == program['username']:
        return True
    if is_admin(user):
        return True

    if is_teacher(user) and program['username'] in DATABASE.get_teacher_students(user['username']):
        return True

    return False


app.register_blueprint(auth_pages.AuthModule(DATABASE))
app.register_blueprint(profile.ProfileModule(DATABASE))
app.register_blueprint(programs.ProgramsModule(DATABASE, ACHIEVEMENTS, STATISTICS))
app.register_blueprint(for_teachers.ForTeachersModule(DATABASE, ACHIEVEMENTS))
app.register_blueprint(classes.ClassModule(DATABASE, ACHIEVEMENTS))
app.register_blueprint(classes.MiscClassPages(DATABASE, ACHIEVEMENTS))
app.register_blueprint(admin.AdminModule(DATABASE))
app.register_blueprint(achievements.AchievementsModule(ACHIEVEMENTS))
app.register_blueprint(quiz.QuizModule(DATABASE, ACHIEVEMENTS, QUIZZES))
app.register_blueprint(parsons.ParsonsModule(PARSONS))
app.register_blueprint(statistics.StatisticsModule(DATABASE))
app.register_blueprint(statistics.LiveStatisticsModule(DATABASE))
app.register_blueprint(user_activity.UserActivityModule(DATABASE))
app.register_blueprint(tags.TagsModule(DATABASE, ACHIEVEMENTS))
app.register_blueprint(public_adventures.PublicAdventuresModule(DATABASE, ACHIEVEMENTS))
app.register_blueprint(surveys.SurveysModule(DATABASE))
app.register_blueprint(feedback.FeedbackModule(DATABASE))


# *** START SERVER ***


def on_server_start():
    """Called just before the server is started, both in developer mode and on Heroku.

    Use this to initialize objects, dependencies and connections.
    """
    pass


def try_parse_int(x):
    """Try to parse an int, return None on failure."""
    try:
        return int(x) if x else None
    except ValueError:
        return None


def analyze_memory_snapshot(start_snapshot, end_snapshot):
    filters = [
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<frozen importlib._bootstrap_external>"),
        tracemalloc.Filter(False, "<unknown>"),
    ]
    start_snapshot = start_snapshot.filter_traces(filters)
    end_snapshot = end_snapshot.filter_traces(filters)
    top_stats = end_snapshot.compare_to(start_snapshot, 'traceback')

    limit = 10

    print("Top %s leaking locations" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        print("#%s: %.1f KiB (count=%d)" % (index, stat.size / 1024, stat.count))
        for line in stat.traceback.format():
            print(' ', line)
        print('')

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


def split_at(n, xs):
    """Split a collection at an index."""
    return xs[:n], xs[n:]


def on_offline_mode():
    """Prepare for running in offline mode."""
    # We are running in a standalone build made using pyinstaller.
    # cd to the directory that has the data files, disable debug mode, and
    # use port 80 (unless overridden).
    # There will be a standard teacher invite code that everyone can use
    # by going to `http://localhost/invite/newteacher`.
    os.chdir(utils.offline_data_dir())
    config['port'] = int(os.environ.get('PORT', 80))
    if not os.getenv('TEACHER_INVITE_CODES'):
        os.environ['TEACHER_INVITE_CODES'] = 'newteacher'
    utils.set_debug_mode(False)

    # Disable logging, so Werkzeug doesn't log all requests and tell users with big red
    # letters they're running a non-production server.
    # from werkzeug import serving
    # def do_nothing(*args, **kwargs): pass
    # serving.WSGIRequestHandler.log_request = do_nothing
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # Get our IP addresses so we can print a helpful hint
    import socket
    ip_addresses = [addr[4][0] for addr in socket.getaddrinfo(
        socket.gethostname(), None, socket.AF_INET, socket.SOCK_STREAM)]
    ip_addresses = [i for i in ip_addresses if i != '127.0.0.1']

    from colorama import colorama_text, Fore, Back, Style
    g = Fore.GREEN
    lines = [
        ('', ''),
        ('', ''),
        (g, r' _    _          _       '),
        (g, r'| |  | |        | |      '),
        (g, r'| |__| | ___  __| |_   _ '),
        (g, r'|  __  |/ _ \/ _` | | | |'),
        (g, r'| |  | |  __/ (_| | |_| |'),
        (g, r'|_|  |_|\___|\__,_|\__, |'),
        (g, r'                    __/ |'),
        (g, r'   o f f l i n e   |___/ '),
        ('', ''),
        ('', 'Use a web browser to visit the following website:'),
        ('', ''),
        *[(Fore.BLUE, f'   http://{ip}/') for ip in ip_addresses],
        ('', ''),
        ('', ''),
    ]
    # This is necessary to make ANSI color codes work on Windows.
    # Init and deinit so we don't mess with Werkzeug's use of this library later on.
    with colorama_text():
        for style, text in lines:
            print(Back.WHITE + Fore.BLACK + ''.ljust(10) + style + text.ljust(60) + Style.RESET_ALL)

    # We have this option for testing the offline build. A lot of modules read
    # files upon import, and those happen before the offline build 'cd' we do
    # here and need to be written to use __file__. During the offline build,
    # we want to run the actual code to see that nobody added file accesses that
    # crash, but we don't actually want to start the server.
    smoke_test = '--smoketest' in sys.argv
    if smoke_test:
        sys.exit(0)


if __name__ == '__main__':
    # Start the server on a developer machine. Flask is initialized in DEBUG mode, so it
    # hot-reloads files. We also flip our own internal "debug mode" flag to True, so our
    # own file loading routines also hot-reload.
    no_debug_mode_requested = os.getenv('NO_DEBUG_MODE')
    utils.set_debug_mode(not no_debug_mode_requested)

    if utils.is_offline_mode():
        on_offline_mode()

    # Set some default environment variables for development mode
    env_defaults = dict(
        BASE_URL=f"http://localhost:{config['port']}/",
        ADMIN_USER="admin",
    )
    for key, value in env_defaults.items():
        if key not in os.environ:
            os.environ[key] = value

    if utils.is_debug_mode():
        # For local debugging, fetch all static files on every request
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = None

    # If we are running in a Python debugger, don't use flasks reload mode. It creates
    # subprocesses which make debugging harder.
    is_in_debugger = sys.gettrace() is not None

    # Set PYTHONTRACEMALLOC=10 to debug memory usage
    profile_memory = os.getenv('PYTHONTRACEMALLOC')
    start_snapshot = None
    if profile_memory:
        import tracemalloc

        tracemalloc.start()
        start_snapshot = tracemalloc.take_snapshot()

    on_server_start()
    debug = utils.is_debug_mode() and not (is_in_debugger or profile_memory)
    if debug:
        logger.debug('app starting in debug mode')

    # Threaded option enables multiple instances for multiple user access support
    app.run(threaded=True, debug=debug,
            port=config['port'], host="0.0.0.0")

    # See `Procfile` for how the server is started on Heroku.

    # If we hit Ctrl-C, we end up here
    if profile_memory:
        print('⏳ Taking memory snapshot. This may take a moment.')
        import gc

        gc.collect()
        end_snapshot = tracemalloc.take_snapshot()
        analyze_memory_snapshot(start_snapshot, end_snapshot)
