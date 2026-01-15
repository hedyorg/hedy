import logging
import os
from os import path
import iso3166
from unidecode import unidecode

from . import static_babel_content
from hedy.yaml_file import YamlFile
from hedy.safe_format import safe_format

# We must find our data relative to this .py file. This will give the
# correct answer both for when Hedy is run as a webserver on Heroku, as well
# as when it has been bundled using pyinstaller.
data_root = path.join(path.dirname(__file__), 'data')

MAX_LEVEL = 16

# Define dictionary for available languages. Fill dynamically later.
ALL_KEYWORD_LANGUAGES = {}

# Babel has a different naming convention than Weblate and doesn't support some languages -> fix this manually
# Map our langauge code to the language code recognized by Babel, or 'en' if Babel doesn't support this locale
# at all.
CUSTOM_BABEL_LANGUAGES = {'pa_PK': 'pa_Arab_PK',
                          'kmr': 'ku_TR',
                          'tl': 'en',
                          'iba': 'en',
                          'peo': 'fa',
                          }

# For the non-existing language manually overwrite the display language to make sure it is displayed correctly
CUSTOM_LANGUAGE_TRANSLATIONS = {'kmr': 'Kurdî (Tirkiye)',
                                'tl': 'ᜆᜄᜎᜓᜄ᜔',
                                'peo': 'Old Persian',
                                'iba': 'Iban',
                                'kab': 'Taqbaylit',
                                }


# Load and cache all keyword yamls
ALL_KEYWORDS = {
    str(lang): {
        str(k): str(v).split('|')
        for k, v in YamlFile.for_file(f'{data_root}/keywords/{lang}.yaml').to_dict().items()
    }
    for lang in ALL_KEYWORD_LANGUAGES
}

KEYWORDS = {  # "default" keywords
    lang: {k: local_keys[0] for k, local_keys in keywords.items()}
    for lang, keywords in ALL_KEYWORDS.items()
}

def grammars_dir():
    """Returns the path to the grammars directory."""
    return path.join(data_root, 'grammars')