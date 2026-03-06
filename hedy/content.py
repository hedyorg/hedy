import glob
from os import path
from hedy.yaml_file import YamlFile

# We must find our data relative to this .py file. This will give the
# correct answer both for when Hedy is run as a webserver on Heroku, as well
# as when it has been bundled using pyinstaller.
data_root = path.join(path.dirname(__file__), 'data')


def grammars_dir():
    """Returns the path to the grammars directory."""
    return path.join(data_root, 'grammars')


def total_grammars_dir():
    """Returns the path to the Total grammars directory."""
    return path.join(data_root, 'grammars-Total')


MAX_LEVEL = 16

languages_in_grammar_dir = set(
    kw_file[len('keywords-'):-len('.lark')]
    for kw_file in glob.glob('keywords-*.lark', root_dir=grammars_dir()))
languages_in_keywords_dir = set(
    kw_file[:-len('.yaml')]
    for kw_file in glob.glob('*.yaml', root_dir=path.join(data_root, 'keywords')))

# Define dictionary for available languages. Fill dynamically later.
ALL_KEYWORD_LANGUAGES = {}
for lang in sorted(list(languages_in_grammar_dir & languages_in_keywords_dir)):
    # Use the first two characters as the language code
    ALL_KEYWORD_LANGUAGES[lang] = lang[0:2].upper()  # first two characters

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
