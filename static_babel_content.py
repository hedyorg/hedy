import json

with open("static_babel_content.json") as f:
    data = json.load(f)


COUNTRIES = data["COUNTRIES"]
LANGUAGE_NAMES = data["LANGUAGE_NAMES"]
TEXT_DIRECTIONS = data["TEXT_DIRECTIONS"]
