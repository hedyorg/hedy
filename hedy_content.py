import copy
import os
from babel import Locale
from flask import g

from website.yaml_file import YamlFile
import iso3166

# Define and load all countries
COUNTRIES = {k: v.name for k, v in iso3166.countries_by_alpha2.items()}

# Define dictionairy for available languages. Fill dynamicly later.
ALL_LANGUAGES = {}

ALL_KEYWORD_LANGUAGES = {
    'en': 'EN',
    'es': 'ES',
    'fr': 'FR',
    'nl': 'NL',
    'nb_NO': 'NB',
    'tr': 'TR',
    'ar': 'AR',
    'hi': 'HI'
}

# Load and cache all keyword yamls
KEYWORDS = {}
for lang in ALL_KEYWORD_LANGUAGES.keys():
    # If this, for some reason, fails -> fill with English values
    KEYWORDS[lang] = YamlFile.for_file(f'content/keywords/{lang}.yaml')

ADVENTURE_ORDER = [
    'default',
    'story',
    'parrot',
    'songs',
    'turtle',
    'dishes',
    'dice',
    'rock',
    'calculator',
    'fortune',
    'restaurant',
    'haunted',
    'piggybank',
    'quizmaster',
    'language',
    'secret',
    'next',
    'end'
]

def fill_all_languages(babel):
    # load all available languages in dict
    # list_translations of babel does about the same, but without territories.
    languages = {}
    for dirname in babel.translation_directories:
        if not os.path.isdir(dirname):
            continue

        for folder in os.listdir(dirname):
            locale_dir = os.path.join(dirname, folder, 'LC_MESSAGES')
            if not os.path.isdir(locale_dir):
                continue

            if filter(lambda x: x.endswith('.mo'), os.listdir(locale_dir)):
                locale = Locale.parse(folder)
                languages[folder] = locale.display_name.title()

    for l in sorted(languages):
        ALL_LANGUAGES[l] = languages[l]


class Commands:
    # Want to parse the keywords only once so they can be cached -> perform this action on server start
    def __init__(self, language):
        self.language = language
        self.file = YamlFile.for_file(f'content/commands/{self.language}.yaml')
        # We always create one with english keywords
        self.data = {"en": self.cache_keyword_parsing("en")}
        if language in ALL_KEYWORD_LANGUAGES.keys():
            self.data[language] = self.cache_keyword_parsing(language)

    def cache_keyword_parsing(self, language):
        keyword_data = {}
        for level in copy.deepcopy(self.file):
            commands = copy.deepcopy(self.file.get(level)) # Take a copy -> otherwise we overwrite the parsing
            for command in commands:
                for k, v in command.items():
                    command[k] = v.format(**KEYWORDS.get(language))
            keyword_data[level] = commands
        return keyword_data

    def get_commands_for_level(self, level, keyword_lang="en"):
        if self.data.get(keyword_lang):
            return self.data.get(keyword_lang).get(int(level), None)
        else:
            return self.data.get("en").get(int(level), None)


class NoSuchCommand:
    def get_commands_for_level(self, level):
        return {}


class Adventures:
    def __init__(self, language):
        self.language = language
        self.adventures = YamlFile.for_file(f'content/adventures/{self.language}.yaml').get('adventures', None)

    # When customizing classes we only want to retrieve the name, (id) and level of each adventure
    def get_adventure_keyname_name_levels(self):
        adventures_dict = {}
        for adventure in self.adventures.items():
            adventures_dict[adventure[0]] = {adventure[1]['name']: list(adventure[1]['levels'].keys())}
        return adventures_dict

    def get_adventures(self):
        return self.adventures if self.adventures else None

    def has_adventures(self):
        return True if self.adventures else False


class NoSuchAdventure:
    def get_adventure(self):
        return {}
