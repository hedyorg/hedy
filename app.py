import hedy
import json
import os
import requests
from flask import request
from datetime import datetime
import jsonbin
import logging

# app.py
from flask import Flask, request, jsonify, render_template
from flask_compress import Compress

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)-8s: %(message)s')

app = Flask(__name__, static_url_path='')
Compress(app)
logger = jsonbin.JsonBinLogger.from_env_vars()

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
    level = request.args.get("level", None)

    log_to_jsonbin(code, level)

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
            response["Code"] = result
        except Exception as E:
            print(f"error transpiling {code}")
            response["Error"] = str(E)

    return jsonify(response)


def log_to_jsonbin(code, level):
    # log all info to jsonbin
    data = {
        'ip': request.remote_addr,
        'date': str(datetime.now()),
        'level': level,
        'code': code
    }
    logger.log(data)

# @app.route('/post/', methods=['POST'])
# for now we do not need a post but I am leaving it in for a potential future

# routing to index.html
@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    level = request.args.get("level", 1)
    level = int(level)
    lang = request.args.get("lang", 'Nl')

    arguments_dict = {}
    arguments_dict['level'] = level
    arguments_dict['lang'] = lang

    try:
        file = open("static/levels.json", "r")
        contents = str(file.read())
        response_levels = (json.loads(contents))
        file.close()
        file = open("static/texts.json", "r")
        contents = str(file.read())
        response_texts = (json.loads(contents))
        file.close()
    except Exception as E:
        print(f"error opening level {level}")
        response_levels["Error"] = str(E)


    response_texts_lang = [r for r in response_texts if r['Language'] == lang][0]
    arguments_dict['page_title'] = response_texts_lang['Page_Title']
    arguments_dict['run_button'] = response_texts_lang['Run_code_button']
    arguments_dict['advance_button'] = response_texts_lang['Advance_button']
    arguments_dict['enter_text'] = response_texts_lang['Enter_Text']
    arguments_dict['enter'] = response_texts_lang['Enter']

    level_and_lang_dict = [r for r in response_levels if int(r['Level']) == level and r['Language'] == lang][0]
    maxlevel = max(int(r['Level']) for r in response_levels)

    arguments_dict['commands'] = level_and_lang_dict['Commands']
    arguments_dict['introtext'] = level_and_lang_dict['Intro_text']
    arguments_dict['startcode'] = level_and_lang_dict['Start_code']

    next_level_available = level != maxlevel
    arguments_dict['nextlevel'] = level + 1 if next_level_available else None
    arguments_dict['latest'] = 'March 13th'

    return render_template("index.html", **arguments_dict)

@app.route('/error_messages.js', methods=['GET'])
def error():
    lang = request.args.get("lang", 'Nl')
    try:
        file = open("static/texts.json", "r")
        contents = str(file.read())
        response = (json.loads(contents))
        file.close()
    except Exception as E:
        print(f"error opening texts.json")
        response["Error"] = str(E)

    response_texts_lang = [r for r in response if r['Language'] == lang][0]
    transpile_error = '"' + response_texts_lang['Transpile_error'] + '"'
    connection_error = '"' + response_texts_lang['Connection_error'] + '"'
    other_error = '"' + response_texts_lang['Other_error'] + '"'

    return render_template("error_messages.js", transpile_error = transpile_error, connection_error = connection_error, other_error = other_error)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
