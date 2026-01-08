from os import path
import json

with open(path.join(path.dirname(__file__), 'data', 'static_babel_content.json')) as f:
    data = json.load(f)

COUNTRIES = data["COUNTRIES"]
LANGUAGE_NAMES = data["LANGUAGE_NAMES"]
TEXT_DIRECTIONS = data["TEXT_DIRECTIONS"]
