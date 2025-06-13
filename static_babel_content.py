import json

from config import ROOT_DIR

with ROOT_DIR.joinpath('static_babel_content.json').open() as f:
    data = json.load(f)


COUNTRIES = data["COUNTRIES"]
LANGUAGE_NAMES = data["LANGUAGE_NAMES"]
TEXT_DIRECTIONS = data["TEXT_DIRECTIONS"]
