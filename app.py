# coding=utf-8
import datetime
from functools import wraps
import hedy
import json
import jsonbin
import logging
import os
import requests
import uuid
from flaskext.markdown import Markdown
from werkzeug.urls import url_encode


# app.py
from flask import Flask, request, jsonify, render_template, session
from flask_compress import Compress

ALL_LANGUAGES = {
    'en': '🇺🇸',
    'nl': '🇳🇱',
    'es': '🇪🇸',
}

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)-8s: %(message)s')

app = Flask(__name__, static_url_path='')

# Unique random key for sessions
app.config['SECRET_KEY'] = uuid.uuid4().hex

Compress(app)
Markdown(app)
logger = jsonbin.JsonBinLogger.from_env_vars()

if not os.getenv('HEROKU_RELEASE_CREATED_AT'):
    logging.warning('Cannot determine release; enable Dyno metadata by running "heroku labs:enable runtime-dyno-metadata -a <APP_NAME>"')

@app.route('/levels-text/', methods=['GET'])
def levels():
    level = request.args.get("level", None)

    #read levels from file
    try:
        file = open("levels.json", "r")
        contents = str(file.read())
        response = (json.loads(contents))
        file.close()
    except Exception as E:
            print(f"error opening level {level}")
            response["Error"] = str(E)
    return jsonify(response)


@app.route('/parse/', methods=['GET'])
def parse():
    # Retrieve the name from url parameter
    code = request.args.get("code", None)
    level = int(request.args.get("level", None))

    # For debugging
    print(f"got code {code}")

    response = {}

    # Check if user sent code
    if not code:
        response["Error"] = "no code found, please send code."
    # is so, parse
    else:
        try:
            result = hedy.transpile(code, level)
            response["Code"] = "# coding=utf8\n" + result
        except hedy.HedyException as E:
            texts = load_texts()
            error_template = texts['HedyErrorMessages'][E.error_code]
            response["Error"] = error_template.format(**E.arguments)
        except Exception as E:
            print(f"error transpiling {code}")
            response["Error"] = str(E)

    logger.log({
        'session': session_id(),
        'date': str(datetime.datetime.now()),
        'level': level,
        'lang': requested_lang(),
        'code': code,
        'server_error': response.get('Error'),
        'version': version(),
    })

    return jsonify(response)

@app.route('/report_error', methods=['POST'])
def report_error():
    post_body = request.json

    logger.log({
        'session': session_id(),
        'date': str(datetime.datetime.now()),
        'level': post_body.get('level'),
        'code': post_body.get('code'),
        'client_error': post_body.get('client_error'),
        'version': version(),
    })

    return 'logged'


# @app.route('/post/', methods=['POST'])
# for now we do not need a post but I am leaving it in for a potential future

# routing to index.html
@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    session_id()  # Run this for the side effect of generating a session ID
    level = requested_level()
    lang = requested_lang()

    arguments_dict = {}
    arguments_dict['level'] = level
    arguments_dict['lang'] = lang

    try:
        with open("static/levels.json", "r") as file:
            response_levels = json.load(file)
        response_texts_lang = load_texts()
    except Exception as E:
        print(f"error opening level {level}")
        return jsonify({"Error": str(E)})

    arguments_dict['page_title'] = response_texts_lang['Page_Title']
    arguments_dict['level_title'] = response_texts_lang['Level']
    arguments_dict['code_title'] = response_texts_lang['Code']
    arguments_dict['docs_title'] = response_texts_lang['Docs'] + ' - ' + response_texts_lang['Level'] + ' ' + str(level)
    arguments_dict['video_title'] = response_texts_lang['Video'] + ' - ' + response_texts_lang['Level'] + ' ' + str(level)
    arguments_dict['contact'] = response_texts_lang['Contact']
    arguments_dict['try_button'] = response_texts_lang['Try_button']
    arguments_dict['run_button'] = response_texts_lang['Run_code_button']
    arguments_dict['advance_button'] = response_texts_lang['Advance_button']
    arguments_dict['enter_text'] = response_texts_lang['Enter_Text']
    arguments_dict['enter'] = response_texts_lang['Enter']

    level_and_lang_dict = [r for r in response_levels if int(r['Level']) == level and r['Language'] == lang][0]
    maxlevel = max(int(r['Level']) for r in response_levels if r['Language'] == lang)

    arguments_dict['commands'] = level_and_lang_dict['Commands']
    arguments_dict['introtext'] = level_and_lang_dict['Intro_text']
    arguments_dict['startcode'] = level_and_lang_dict['Start_code']

    next_level_available = level != maxlevel
    arguments_dict['nextlevel'] = level + 1 if next_level_available else None
    arguments_dict['latest'] = version()
    arguments_dict['selected_page'] = 'code'

    return render_template("index.html", **arguments_dict)

# routing to docs.html
@app.route('/docs', methods=['GET'])
def docs():
    level = request.args.get("level", 1)
    lang = requested_lang()
    response_texts_lang = load_texts()

    arguments_dict = {}
    arguments_dict['level'] = level
    arguments_dict['pagetitle'] = f'Level{level}'
    arguments_dict['lang'] = lang
    arguments_dict['level_title'] = response_texts_lang['Level']
    arguments_dict['code_title'] = response_texts_lang['Code']
    arguments_dict['docs_title'] = response_texts_lang['Docs'] + ' - ' + response_texts_lang['Level'] + ' ' + str(level)
    arguments_dict['video_title'] = response_texts_lang['Video'] + ' - ' + response_texts_lang['Level'] + ' ' + str(level)
    arguments_dict['contact'] = response_texts_lang['Contact']
    arguments_dict['selected_page'] = 'docs'

    arguments_dict['mkd'] = load_docs()

    return render_template("docs_per_level.html", **arguments_dict)

# routing to video.html
@app.route('/video', methods=['GET'])
def video():
    level = request.args.get("level", 1)
    lang = requested_lang()
    response_texts_lang = load_texts()

    arguments_dict = {}
    arguments_dict['level'] = level
    arguments_dict['pagetitle'] = f'Level{level}'
    arguments_dict['lang'] = lang
    arguments_dict['selected_page'] = 'video'
    arguments_dict['level_title'] = response_texts_lang['Level']
    arguments_dict['code_title'] = response_texts_lang['Code']
    arguments_dict['docs_title'] = response_texts_lang['Docs'] + ' - ' + response_texts_lang['Level'] + ' ' + str(level)
    arguments_dict['video_title'] = response_texts_lang['Video'] + ' - ' + response_texts_lang['Level'] + ' ' + str(level)
    arguments_dict['contact'] = response_texts_lang['Contact']

    arguments_dict['mkd'] = load_video()

    return render_template("video_per_level.html", **arguments_dict)

# routing to contact.html
@app.route('/contact', methods=['GET'])
def contact():
    level = request.args.get("level", 1)
    lang = requested_lang()
    response_texts_lang = load_texts()

    arguments_dict = {}
    arguments_dict['level'] = level
    arguments_dict['pagetitle'] = f'Level{level}'
    arguments_dict['lang'] = lang
    arguments_dict['selected_page'] = 'video'
    arguments_dict['level_title'] = response_texts_lang['Level']
    arguments_dict['code_title'] = response_texts_lang['Code']
    arguments_dict['docs_title'] = response_texts_lang['Docs'] + ' - ' + response_texts_lang['Level'] + ' ' + str(level)
    arguments_dict['video_title'] = response_texts_lang['Video'] + ' - ' + response_texts_lang['Level'] + ' ' + str(level)
    arguments_dict['contact'] = response_texts_lang['Contact']

    arguments_dict['mkd'] = load_contact()

    return render_template("contact.html", **arguments_dict)

@app.route('/error_messages.js', methods=['GET'])
def error():
    try:
        lang_texts = load_texts()
        error_messages = lang_texts["ClientErrorMessages"]
    except Exception as E:
        print(f"error opening texts.json")
        error_messages = {"Error": str(E)}

    return render_template("error_messages.js", error_messages=json.dumps(error_messages))


@app.errorhandler(500)
def internal_error(exception):
    import traceback
    print(traceback.format_exc())
    return "<h1>500 Internal Server Error</h1>"


def session_id():
    """Returns or sets the current session ID."""
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4().hex
    return session['session_id']


def requested_lang():
    """Return the user's requested language code.

    If not in the request parameters, use the browser's accept-languages
    header to do language negotiation.
    """
    lang = request.args.get("lang")
    if lang: return lang

    return request.accept_languages.best_match(ALL_LANGUAGES.keys(), 'en')

def requested_level():
    """Return the user's requested level."""
    return int(request.args.get("level", 1))


def load_contact():
    """Load the markdown docs for the given language and level. """
    lang = requested_lang()

    try:
        with open(f'docs/contact-{lang}.md', "r") as file:
            markdown = file.read()
        return markdown

    except IOError as e: #if no contact info is available, fall back to En version
        with open(f'docs/contact-en.md', "r") as file:
            markdown = file.read()
            return markdown

def load_docs():
    """Load the markdown docs for the given language and level. """
    lang = requested_lang()
    level = requested_level()

    try:
        with open(f'docs/{lang}-level{level}.md', "r") as file:
            markdown = file.read()

        return markdown
    except IOError as e:
        return f'No documentation available for language {lang} at Level {level}. You might want to translate this yourself via our GitHub repo?'

def load_video():
    """Load the markdown video document for the given language and level. """
    lang = requested_lang()
    level = requested_level()

    try:
        with open(f'docs/video-{lang}-level{level}.md', "r") as file:
            markdown = file.read()

        return markdown
    except IOError as e:
        return f'No docs available for {lang} at level {level}'


@app.template_global()
def current_language():
    return make_lang_obj(requested_lang())


@app.template_global()
def other_languages():
    cl = requested_lang()
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

def load_texts():
    """Load the texts for the given language.

    If the language is unknown, default to English.
    """
    with open("static/texts.json", "r") as file:
        texts_file = json.load(file)
    texts = texts_file.get(requested_lang().lower())
    return texts if texts else texts_file.get('en')


def no_none_sense(d):
    """Remove all None values from a dict."""
    return {k: v for k, v in d.items() if v is not None}


def version():
    """Get the version from the Heroku environment variables."""
    if not os.getenv('DYNO'):
        # Not on Heroku
        return 'DEV'

    vrz = os.getenv('HEROKU_RELEASE_CREATED_AT')
    the_date = datetime.date.fromisoformat(vrz[:10]) if vrz else datetime.date.today()

    commit = os.getenv('HEROKU_SLUG_COMMIT', '????')[0:6]
    return the_date.strftime('%b %d') + f' ({commit})'


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
