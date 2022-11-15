# coding=utf-8
import collections
import copy
import datetime
import json
import logging
import os
import sys
import textwrap
import traceback
import zipfile
from logging.config import dictConfig as logConfig
from os import path

from babel import Locale
from flask import (Flask, Markup, Response, abort, after_this_request, g,
                   jsonify, make_response, redirect, request, send_file,
                   send_from_directory, session)
from flask_babel import Babel, gettext
from flask_commonmark import Commonmark
from flask_compress import Compress
from werkzeug.urls import url_encode

import hedy
import hedy_content
import hedy_translation
import hedyweb
import utils
from config import config
from flask_helpers import render_template
from hedy_content import (ADVENTURE_ORDER_PER_LEVEL, ALL_KEYWORD_LANGUAGES,
                          ALL_LANGUAGES, COUNTRIES,
                          NON_LATIN_LANGUAGES)
from logging_config import LOGGING_CONFIG
from utils import dump_yaml_rt, is_debug_mode, load_yaml_rt, timems, version
from website import (ab_proxying, achievements, admin, auth_pages, aws_helpers,
                     cdn, classes, database, for_teachers, jsonbin, parsons,
                     profile, programs, querylog, quiz, statistics,
                     translating)
from website.auth import (current_user, is_admin, is_teacher,
                          login_user_from_token_cookie, requires_login, requires_teacher)
from website.log_fetcher import log_fetcher
from website.yaml_file import YamlFile


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
babel = Babel(app)

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

ACHIEVEMENTS_TRANSLATIONS = hedyweb.AchievementTranslations()
DATABASE = database.Database()
ACHIEVEMENTS = achievements.Achievements(DATABASE, ACHIEVEMENTS_TRANSLATIONS)

# We retrieve these once on server-start: Would be nice to automate this
# somewhere in the future (06/22)
PUBLIC_PROGRAMS = DATABASE.get_all_public_programs()


# Load the adventures, by default with the selected keyword language
def load_adventures_per_level(level, keyword_lang):
    loaded_programs = {}
    # If user is logged in, we iterate their programs that belong to the
    # current level. Out of these, we keep the latest created program for both
    # the level mode(no adventure) and for each of the adventures.
    if current_user()['username']:
        user_programs = DATABASE.level_programs_for_user(
            current_user()['username'], level)
        for program in user_programs:
            program_key = 'default' if not program.get(
                'adventure_name') else program['adventure_name']
            if (program_key not in loaded_programs or loaded_programs[program_key]['date'] < program['date']):
                loaded_programs[program_key] = program

    all_adventures = []
    adventures = ADVENTURES[g.lang].get_adventures(keyword_lang)

    for short_name, adventure in adventures.items():
        if level not in adventure['levels']:
            continue
        # end adventure is the quiz
        # if quizzes are not enabled, do not load it
        # Todo TB -> Is this still relevant? Teachers can simply "disable"
        # adventures in customizations!
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
    # Set the database object on the global object (auth.py needs it)
    g.db = DATABASE

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
        if g.lang in ALL_KEYWORD_LANGUAGES.keys() and g.lang in NON_LATIN_LANGUAGES:
            g.keyword_lang = g.lang
        else:
            g.keyword_lang = "en"
    else:
        g.keyword_lang = session['keyword_lang']

    # Set the page direction -> automatically set it to "left-to-right"
    # Switch to "right-to-left" if one of the language is rtl according to Locale (from Babel) settings.
    # This is the only place to expand / shrink the list of RTL languages ->
    # front-end is fixed based on this value
    g.dir = "ltr"
    if Locale(g.lang).text_direction in ["ltr", "rtl"]:
        g.dir = Locale(g.lang).text_direction

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
            'is_teacher': is_teacher(user), 'is_admin': is_admin(user)}
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
    return jsonify({'session': dict(session),
                    'proxy_enabled': bool(os.getenv('PROXY_TO_TEST_HOST'))})


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
        keyword_lang = current_keyword_language()["lang"]
        with querylog.log_time('transpile'):
            try:
                transpile_result = transpile_add_stats(code, level, lang)
                if username and not body.get('tutorial'):
                    DATABASE.increase_user_run_count(username)
                    ACHIEVEMENTS.increase_count("run")
            except hedy.exceptions.WarningException as ex:
                translated_error = translate_error(ex.error_code, ex.arguments, keyword_lang)
                if isinstance(ex, hedy.exceptions.InvalidSpaceException):
                    response['Warning'] = translated_error
                else:
                    response['Error'] = translated_error
                response['Location'] = ex.error_location
                response['FixedCode'] = ex.fixed_code
                transpile_result = ex.fixed_result
                exception = ex
            except hedy.exceptions.UnquotedEqualityCheck as ex:
                response['Error'] = translate_error(ex.error_code, ex.arguments, keyword_lang)
                response['Location'] = ex.error_location
                exception = ex
        try:
            response['Code'] = transpile_result.code

            if transpile_result.has_pygame:
                response['has_pygame'] = True

            if transpile_result.has_turtle:
                response['has_turtle'] = True
        except Exception:
            pass
        try:
            response['has_sleep'] = 'sleep' in hedy.all_commands(code, level, lang)
        except BaseException:
            pass
        try:
            if username and not body.get('tutorial') and ACHIEVEMENTS.verify_run_achievements(
                    username, code, level, response):
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
            hedy.transpile(
                program.get('code'),
                program.get('level'),
                program.get('lang')
            )
            return {}, 200
        except BaseException:
            return {"error": "parsing error"}, 200
    else:
        return 'this is not your program!', 400


@app.route('/parse_tutorial', methods=['POST'])
@requires_login
def parse_tutorial(user):
    body = request.json

    code = body['code']
    level = int(body['level'])
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


def transpile_add_stats(code, level, lang_):
    username = current_user()['username'] or None
    number_of_lines = code.count('\n')
    try:
        result = hedy.transpile(code, level, lang_)
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
        "Error": translate_error(ex.error_code, ex.arguments, keyword_lang),
        "Location": ex.error_location
    }


def translate_error(code, arguments, keyword_lang):
    arguments_that_require_translation = [
        'allowed_types',
        'invalid_type',
        'invalid_type_2',
        'character_found',
        'concept',
        'tip',
        'command',
        'print',
        'ask',
        'echo',
        'is',
        'repeat']
    arguments_that_require_highlighting = [
        'command',
        'guessed_command',
        'invalid_argument',
        'invalid_argument_2',
        'variable',
        'invalid_value',
        'print',
        'ask',
        'echo',
        'is',
        'repeat']

    # Todo TB -> We have to find a more delicate way to fix this: returns some gettext() errors
    error_template = gettext('' + str(code))

    # Fetch tip if it exists and merge into template, since it can also contain placeholders
    # that need to be translated/highlighted

    if 'tip' in arguments:
        error_template = error_template.replace("{tip}", gettext('' + str(arguments['tip'])))
        # TODO, FH Oct 2022 -> Could we do this with a format even though we don't have all fields?

    # adds keywords to the dictionary so they can be translated if they occur in the error text

    # FH Oct 2022: this could be optimized by only adding them when they occur in the text
    # (either with string matching or with a list of placeholders for each error)
    arguments["print"] = "print"
    arguments["ask"] = "ask"
    arguments["echo"] = "echo"
    arguments["repeat"] = "repeat"
    arguments["is"] = "is"

    # some arguments like allowed types or characters need to be translated in the error message
    for k, v in arguments.items():
        if k in arguments_that_require_translation:
            if isinstance(v, list):
                arguments[k] = translate_list(v)
            else:
                arguments[k] = gettext('' + str(v))

        if k in arguments_that_require_highlighting:
            if k in arguments_that_require_translation:
                local_keyword = hedy_translation.translate_keyword_from_en(v, keyword_lang)
                arguments[k] = hedy.style_command(local_keyword)
            else:
                arguments[k] = hedy.style_command(v)

    return error_template.format(**arguments)


def translate_list(args):
    translated_args = [gettext('' + str(a)) for a in args]
    # Deduplication is needed because diff values could be translated to the
    # same value, e.g. int and float => a number
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

    adventures_names = hedy_content.Adventures(session['lang']).get_adventure_names()

    # We request our own page -> also get the public_profile settings
    public_profile = None
    if not from_user:
        public_profile = DATABASE.get_public_profile_settings(username)

    level = request.args.get('level', default=None, type=str)
    adventure = request.args.get('adventure', default=None, type=str)
    filter = request.args.get('filter', default=None, type=str)

    level = None if level == "null" else level
    adventure = None if adventure == "null" else adventure

    if level or adventure:
        result = DATABASE.filtered_programs_for_user(from_user or username, level, adventure)
    else:
        result = DATABASE.programs_for_user(from_user or username)

    programs = []
    for item in result:
        # If we filter on the submitted programs -> skip the onces that are not submitted
        if filter == "submitted" and not item.get('submitted'):
            continue
        date = utils.delta_timestamp(item['date'])
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
             'public': item.get('public'),
             'number_lines': item['code'].count('\n') + 1
             }
        )

    return render_template(
        'programs.html',
        programs=programs,
        page_title=gettext('title_programs'),
        current_page='programs',
        from_user=from_user,
        adventure_names=adventures_names,
        public_profile=public_profile,
        max_level=hedy.HEDY_MAX_LEVEL)


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
        if not class_ or class_['teacher'] != user['username'] or username_filter not in class_.get('students', [
        ]):
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


@app.route('/tutorial', methods=['GET'])
def tutorial_index():
    if not current_user()['username']:
        return redirect('/login')
    level = 1
    cheatsheet = COMMANDS[g.lang].get_commands_for_level(level, g.keyword_lang)
    commands = hedy.commands_per_level.get(level)
    adventures = load_adventures_per_level(level, g.keyword_lang)
    parsons = len(PARSONS[g.lang].get_parsons_data_for_level(level))

    return hedyweb.render_tutorial_mode(level=level, cheatsheet=cheatsheet, commands=commands,
                                        adventures=adventures, parsons_exercises=parsons)


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
                           page_title=gettext('title_for-teacher'), teacher_classes=teacher_classes,
                           teacher_adventures=adventures, tutorial=True,
                           content=hedyweb.PageTranslations('for-teachers').get_page_translations(g.lang))


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
    except BaseException:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    loaded_program = ''
    adventure_name = ''

    if program_id:
        result = DATABASE.program_by_id(program_id)
        if not result:
            return utils.error_page(error=404, ui_message=gettext('no_such_program'))

        user = current_user()
        public_program = result.get('public')
        # Verify that the program is either public, the current user is the
        # creator, teacher or the user is admin
        if not public_program and user['username'] != result['username'] and not is_admin(user):
            if ((not is_teacher(user)) or (is_teacher(user)
                                           and result['username'] not in
                                           DATABASE.get_teacher_students(user['username']))):
                return utils.error_page(error=404, ui_message=gettext(u'no_such_program'))

        loaded_program = {'code': result['code'], 'name': result['name'],
                          'adventure_name': result.get('adventure_name')}
        if 'adventure_name' in result:
            adventure_name = result['adventure_name']

    # In case of a "forced keyword language" -> load that one, otherwise: load
    # the one stored in the g object
    keyword_language = request.args.get('keyword_language', default=None, type=str)
    if keyword_language:
        adventures = load_adventures_per_level(level, keyword_language)
    else:
        adventures = load_adventures_per_level(level, g.keyword_lang)

    # Sort the adventures based on the ordering defined
    adventures_order = ADVENTURE_ORDER_PER_LEVEL[level]
    index_map = {v: i for i, v in enumerate(adventures_order)}
    adventures = sorted(
        adventures,
        key=lambda pair: index_map.get(
            pair['short_name'],
            len(adventures_order)))

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
            if level > 1:
                scores = [x.get('scores', []) for x in quiz_stats if x.get('level') == level - 1]
                scores = [score for week_scores in scores for score in week_scores]
                max_score = 0 if len(scores) < 1 else max(scores)
                if max_score < threshold:
                    return utils.error_page(
                        error=403, ui_message=gettext('quiz_threshold_not_reached'))

            # We also have to check if the next level should be removed from the available_levels
            if level < hedy.HEDY_MAX_LEVEL:
                scores = [x.get('scores', []) for x in quiz_stats if x.get('level') == level]
                scores = [score for week_scores in scores for score in week_scores]
                max_score = 0 if len(scores) < 1 else max(scores)
                # We don't have the score yet for the next level -> remove all upcoming
                # levels from 'available_levels'
                if max_score < threshold:
                    available_levels = available_levels[:available_levels.index(level) + 1]

    # Add the available levels to the customizations dict -> simplify
    # implementation on the front-end
    customizations['available_levels'] = available_levels
    cheatsheet = COMMANDS[g.lang].get_commands_for_level(level, g.keyword_lang)

    teacher_adventures = []
    # Todo: TB It would be nice to improve this by using level as a sort key
    for adventure in customizations.get('teacher_adventures', []):
        current_adventure = DATABASE.get_adventure(adventure)
        if current_adventure.get('level') == str(level):
            try:
                current_adventure['content'] = current_adventure['content'].format(
                    **hedy_content.KEYWORDS.get(g.keyword_lang))
            except BaseException:
                # We don't want teacher being able to break the student UI -> pass this adventure
                pass
            teacher_adventures.append(current_adventure)

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

    if 'other_settings' in customizations and 'hide_parsons' in customizations['other_settings']:
        parsons = False
    if 'other_settings' in customizations and 'hide_quiz' in customizations['other_settings']:
        quiz = False

    commands = hedy.commands_per_level.get(level)

    return hedyweb.render_code_editor_with_tabs(
        cheatsheet=cheatsheet,
        commands=commands,
        max_level=hedy.HEDY_MAX_LEVEL,
        level_number=level,
        version=version(),
        quiz=quiz,
        quiz_questions=quiz_questions,
        adventures=adventures,
        parsons=parsons,
        parsons_exercises=parson_exercises,
        tutorial=tutorial,
        customizations=customizations,
        hide_cheatsheet=hide_cheatsheet,
        enforce_developers_mode=enforce_developers_mode,
        teacher_adventures=teacher_adventures,
        loaded_program=loaded_program,
        adventure_name=adventure_name)


@app.route('/hedy/<id>/view', methods=['GET'])
@requires_login
def view_program(user, id):
    result = DATABASE.program_by_id(id)

    if not result:
        return utils.error_page(error=404, ui_message=gettext('no_such_program'))

    public_program = result.get('public')
    # Verify that the program is either public, the current user is the
    # creator, teacher or the user is admin
    if not public_program and user['username'] != result['username'] and not is_admin(user):
        if (not is_teacher(user)) or (is_teacher(user)
                                      and result['username'] not in DATABASE.get_teacher_students(user['username'])):
            return utils.error_page(error=404, ui_message=gettext(u'no_such_program'))

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
    arguments_dict['loaded_program'] = result
    arguments_dict['editor_readonly'] = True

    if "submitted" in result and result['submitted']:
        arguments_dict['show_edit_button'] = False
        arguments_dict['program_timestamp'] = utils.localized_date_format(result['date'])
    else:
        arguments_dict['show_edit_button'] = True

    # Everything below this line has nothing to do with this page and it's silly
    # that every page needs to put in so much effort to re-set it

    return render_template("view-program-page.html", blur_button_available=True, **arguments_dict)


@app.route('/adventure/<name>', methods=['GET'], defaults={'level': 1})
@app.route('/adventure/<name>/<level>', methods=['GET'])
def get_specific_adventure(name, level):
    try:
        level = int(level)
    except BaseException:
        return utils.error_page(error=404, ui_message=gettext('no_such_level'))

    # In case of a "forced keyword language" -> load that one, otherwise: load
    # the one stored in the g object
    keyword_language = request.args.get('keyword_language', default=None, type=str)
    if keyword_language:
        adventure = [x for x in load_adventures_per_level(
            level, keyword_language) if x.get('short_name') == name]
    else:
        adventure = [x for x in load_adventures_per_level(
            level, g.keyword_lang) if x.get('short_name') == name]
    if not adventure:
        return utils.error_page(error=404, ui_message=gettext('no_such_adventure'))

    prev_level = level - 1 if [x for x in load_adventures_per_level(
        level - 1, g.keyword_lang) if x.get('short_name') == name] else False
    next_level = level + 1 if [x for x in load_adventures_per_level(
        level + 1, g.keyword_lang) if x.get('short_name') == name] else False

    # Add the commands to enable the language switcher dropdown
    commands = hedy.commands_per_level.get(level)

    return hedyweb.render_specific_adventure(
        commands=commands,
        level_number=level,
        adventure=adventure,
        version=version(),
        prev_level=prev_level,
        next_level=next_level)


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

    return render_template("cheatsheet.html", commands=commands, level=level)


@app.route('/certificate/<username>', methods=['GET'])
def get_certificate_page(username):
    if not current_user()['username']:
        return utils.error_page(error=403, ui_message=gettext('unauthorized'))
    username = username.lower()
    user = DATABASE.user_by_username(username)
    if not user:
        return utils.error_page(error=403, ui_message=gettext('user_inexistent'))
    progress_data = DATABASE.progress_by_username(username)
    if progress_data is None:
        return utils.error_page(error=404, ui_message=gettext('no_certificate'))
    achievements = progress_data.get('achieved', None)
    if achievements is None or 'hedy_certificate' not in achievements:
        return utils.error_page(error=404, ui_message=gettext('no_certificate'))
    if 'run_programs' in progress_data:
        count_programs = progress_data['run_programs']
    else:
        count_programs = 0
    quiz_score = get_highest_quiz_score(username)
    longest_program = get_longest_program(username)

    number_achievements = len(achievements)
    congrats_message = gettext('congrats_message').format(**{'username': username})
    return render_template("certificate.html", count_programs=count_programs, quiz_score=quiz_score,
                           longest_program=longest_program, number_achievements=number_achievements,
                           congrats_message=congrats_message)


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
        return utils.error_page(error=403, ui_message=gettext('unauthorized'))
    return render_template(
        'reset.html',
        page_title=gettext('title_reset'),
        reset_username=username,
        reset_token=token,
        current_page='login')


@app.route('/my-profile', methods=['GET'])
@requires_login
def profile_page(user):

    profile = DATABASE.user_by_username(user['username'])
    programs = DATABASE.public_programs_for_user(user['username'])
    public_profile_settings = DATABASE.get_public_profile_settings(current_user()['username'])

    classes = []
    if profile.get('classes'):
        for class_id in profile.get('classes'):
            classes.append(DATABASE.get_class(class_id))

    invite = DATABASE.get_username_invite(user['username'])
    if invite:
        # We have to keep this in mind as well, can simply be set to 1 for now
        # But when adding more message structures we have to use a more sophisticated structure
        session['messages'] = 1
        # If there is an invite: retrieve the class information
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
        invite_data=invite,
        public_settings=public_profile_settings,
        user_classes=classes,
        current_page='my-profile')


@app.route('/research/<filename>', methods=['GET'])
def get_research(filename):
    return send_from_directory('content/research/', filename)


@app.route('/<page>')
def main_page(page):
    if page == 'favicon.ico':
        abort(404)

    if page == "my-achievements":
        return achievements_page()

    if page == 'learn-more':
        learn_more_translations = hedyweb.PageTranslations(page).get_page_translations(g.lang)
        return render_template(
            'learn-more.html',
            papers=hedy_content.RESEARCH,
            page_title=gettext('title_learn-more'),
            current_page='learn-more',
            content=learn_more_translations)

    if page == 'join':
        join_translations = hedyweb.PageTranslations(page).get_page_translations(g.lang)
        return render_template('join.html', page_title=gettext('title_learn-more'),
                               current_page='join', content=join_translations)

    if page == 'privacy':
        privacy_translations = hedyweb.PageTranslations(
            page).get_page_translations(g.lang)
        return render_template('privacy.html', page_title=gettext('title_privacy'),
                               content=privacy_translations)

    requested_page = hedyweb.PageTranslations(page)
    if not requested_page.exists():
        abort(404)

    main_page_translations = requested_page.get_page_translations(g.lang)
    return render_template('main-page.html', page_title=gettext('title_start'),
                           current_page='start', content=main_page_translations)


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

    level = request.args.get('level', default=None, type=str)
    adventure = request.args.get('adventure', default=None, type=str)
    language = request.args.get('lang', default=None, type=str)

    level = None if level == "null" else level
    adventure = None if adventure == "null" else adventure
    language = None if language == "null" else language

    achievement = None
    if level or adventure or language:
        programs = PUBLIC_PROGRAMS
        if level:
            programs = [x for x in programs if x.get('level') == int(level)]
        if language:
            programs = [x for x in programs if x.get('lang') == language]
        if adventure:
            # If the adventure we filter on is called 'default' -> return all programs
            # WITHOUT an adventure
            if adventure == "default":
                programs = [x for x in programs if x.get('adventure_name') == ""]
                return programs[-48:]
            programs = [x for x in programs if x.get('adventure_name') == adventure]
        programs = programs[-48:]
        achievement = ACHIEVEMENTS.add_single_achievement(
            current_user()['username'], "indiana_jones")
    else:
        programs = PUBLIC_PROGRAMS[:48]

    filtered_programs = []
    for program in programs:
        # If program does not have an error value set -> parse it and set value
        if 'error' not in program:
            try:
                hedy.transpile(program.get('code'), program.get('level'), program.get('lang'))
                program['error'] = False
            except BaseException:
                program['error'] = True
            DATABASE.store_program(program)
        public_profile = DATABASE.get_public_profile_settings(program['username'])

        # If the language doesn't match the user -> parse the keywords
        # We perform a "double parse" to make sure english keywords are also always translated
        code = program['code']

        # First, if the program language is not equal to english and the language supports keywords
        # It might contain non-english keywords -> parse all to english
        if program.get("lang") != "en" and program.get("lang") in ALL_KEYWORD_LANGUAGES.keys():
            code = hedy_translation.translate_keywords(code, from_lang=program.get(
                'lang'), to_lang="en", level=int(program.get('level', 1)))
        # If the keyword language is non-English -> parse again to guarantee
        # completely localized keywords
        if g.keyword_lang != "en":
            code = hedy_translation.translate_keywords(
                code,
                from_lang="en",
                to_lang=g.keyword_lang,
                level=int(
                    program.get(
                        'level',
                        1)))

        filtered_programs.append({
            'username': program['username'],
            'name': program['name'],
            'level': program['level'],
            'id': program['id'],
            'error': program['error'],
            'hedy_choice': True if program.get('hedy_choice') == 1 else False,
            'public_user': True if public_profile else None,
            'code': "\n".join(code.split("\n")[:4]),
            'number_lines': code.count('\n') + 1
        })

    favourite_programs = DATABASE.get_hedy_choices()
    hedy_choices = []
    for program in favourite_programs:
        hedy_choices.append({
            'username': program['username'],
            'name': program['name'],
            'level': program['level'],
            'id': program['id'],
            'hedy_choice': True,
            'public_user': True if public_profile else None,
            'code': "\n".join(program['code'].split("\n")[:4]),
            'number_lines': code.count('\n') + 1
        })

    adventures_names = hedy_content.Adventures(session['lang']).get_adventure_names()

    return render_template(
        'explore.html',
        programs=filtered_programs,
        favourite_programs=hedy_choices,
        filtered_level=level,
        achievement=achievement,
        filtered_adventure=adventure,
        filtered_lang=language,
        max_level=hedy.HEDY_MAX_LEVEL,
        adventures_names=adventures_names,
        page_title=gettext('title_explore'),
        current_page='explore')


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
    except BaseException:
        return gettext('translate_error'), 400


# TODO TB: Think about changing this to sending all steps to the front-end at once
@app.route('/get_tutorial_step/<level>/<step>', methods=['GET'])
def get_tutorial_translation(level, step):
    # Keep this structure temporary until we decide on a nice code / parse structure
    if step == "code_snippet":
        return jsonify({'code': gettext('tutorial_code_snippet')}), 200
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
    if not isinstance(body.get('level'), str):
        return 'level must be a string', 400
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
    return jsonify({}), 200


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


@app.template_global()
def translate_command(command):
    # Return the translated command found in KEYWORDS, if not found return the command itself
    return hedy_content.KEYWORDS[g.lang].get(command, command)


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
    current_lang = g.lang
    return [make_lang_obj(lang) for lang in ALL_LANGUAGES.keys() if lang != current_lang]


@app.template_global()
def other_keyword_languages():
    current_lang = g.lang
    return [make_lang_obj(lang) for lang in ALL_KEYWORD_LANGUAGES.keys() if lang != current_lang]


@app.template_global()
def keyword_languages():
    return [make_lang_obj(lang) for lang in ALL_KEYWORD_LANGUAGES.keys()]


@app.template_global()
def keyword_languages_keys():
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

    return '{}?{}'.format(request.path, url_encode(args))


@app.template_global()
def get_user_messages():
    if not session.get('messages'):
        # Todo TB: In the future this should contain the class invites + other messages
        # As the class invites are binary (you either have one or you have none, we can possibly simplify this)
        # Simply set it to 1 if we have an invite, otherwise keep at 0
        invite = DATABASE.get_username_invite(current_user()['username'])
        session['messages'] = 1 if invite else 0
    if session.get('messages') > 0:
        return session.get('messages')
    return None

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
        certificate_message = gettext('see_certificate').format(**{'username': username})
        # Todo: TB -> In the near future: add achievement for user visiting their own profile

        return render_template(
            'public-page.html',
            user_info=user_public_info,
            achievements=ACHIEVEMENTS_TRANSLATIONS.get_translations(
                g.lang).get('achievements'),
            favourite_program=favourite_program,
            programs=user_programs,
            last_achieved=last_achieved,
            user_achievements=user_achievements,
            certificate_message=certificate_message)
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


app.register_blueprint(auth_pages.AuthModule(DATABASE))
app.register_blueprint(profile.ProfileModule(DATABASE))
app.register_blueprint(programs.ProgramsModule(DATABASE, ACHIEVEMENTS))
app.register_blueprint(for_teachers.ForTeachersModule(DATABASE, ACHIEVEMENTS))
app.register_blueprint(classes.ClassModule(DATABASE, ACHIEVEMENTS))
app.register_blueprint(classes.MiscClassPages(DATABASE, ACHIEVEMENTS))
app.register_blueprint(admin.AdminModule(DATABASE))
app.register_blueprint(achievements.AchievementsModule(ACHIEVEMENTS))
app.register_blueprint(quiz.QuizModule(DATABASE, ACHIEVEMENTS, QUIZZES))
app.register_blueprint(parsons.ParsonsModule(PARSONS))
app.register_blueprint(statistics.StatisticsModule(DATABASE))

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
    logger.debug('app starting in debug mode')
    # Threaded option enables multiple instances for multiple user access support
    app.run(threaded=True, debug=not is_in_debugger,
            port=config['port'], host="0.0.0.0")

    # See `Procfile` for how the server is started on Heroku.
