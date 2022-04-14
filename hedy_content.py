import copy
import os
from babel import Locale
from flask import g

from utils import is_debug_mode
from website.yaml_file import YamlFile
import iso3166

# Define and load all countries
COUNTRIES = {k: v.name for k, v in iso3166.countries_by_alpha2.items()}

# Define dictionary for available languages. Fill dynamically later.
ALL_LANGUAGES = {}
ALL_KEYWORD_LANGUAGES = {}

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

# load all available languages in dict
# list_translations of babel does about the same, but without territories.
languages = {}
if not os.path.isdir('translations'):
    # should not be possible, but if it's moved someday, EN would still be working.
    ALL_LANGUAGES['en'] = 'English'
    ALL_KEYWORD_LANGUAGES['en'] = 'EN'

for folder in os.listdir('translations'):
    locale_dir = os.path.join('translations', folder, 'LC_MESSAGES')
    if not os.path.isdir(locale_dir):
        continue

    if filter(lambda x: x.endswith('.mo'), os.listdir(locale_dir)):
        locale = Locale.parse(folder)
        languages[folder] = locale.display_name.title()

for l in sorted(languages):
    ALL_LANGUAGES[l] = languages[l]
    if os.path.exists('./grammars/keywords-' + l + '.lark'):
        ALL_KEYWORD_LANGUAGES[l] = l[0:2].upper()  # first two characters

# Load and cache all keyword yamls
KEYWORDS = {}
for lang in ALL_KEYWORD_LANGUAGES.keys():
    # If this, for some reason, fails -> fill with English values
    KEYWORDS[lang] = YamlFile.for_file(f'content/keywords/{lang}.yaml')

class Commands:
    # Want to parse the keywords only once, they can be cached -> perform this action on server start
    def __init__(self, language):
        self.language = language
        # We can keep these cached, even in debug_mode: files are small and don't influence start-up time much
        self.file = YamlFile.for_file(f'content/commands/{self.language}.yaml')
        self.data = {}

        # For some reason the is_debug_mode() function is not (yet) ready when we call this code
        # So we call the NO_DEBUG_MODE directly from the environment
        # Todo TB -> Fix that the is_debug_mode() function is ready before server start
        self.debug_mode = not os.getenv('NO_DEBUG_MODE')

        if not self.debug_mode:
            # We always create one with english keywords
            self.data["en"] = self.cache_keyword_parsing("en")
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
        if self.debug_mode and not self.data.get(keyword_lang, None):
            self.data[keyword_lang] = self.cache_keyword_parsing(keyword_lang)
        return self.data.get(keyword_lang, {}).get(int(level), None)

# Todo TB -> We don't need these anymore as we guarantee with Weblate that each language file is there
class NoSuchCommand:
    def get_commands_for_level(self, level):
        return {}

# Parsing all these adventures on server start takes quite some time
# Don't do this when on debug mode!
class Adventures:
    def __init__(self, language):
        self.language = language
        self.file = {}
        self.data = {}

        # For some reason the is_debug_mode() function is not (yet) ready when we call this code
        # So we call the NO_DEBUG_MODE directly from the environment
        # Todo TB -> Fix that the is_debug_mode() function is ready before server start
        self.debug_mode = not os.getenv('NO_DEBUG_MODE')

        if not self.debug_mode:
            self.file = YamlFile.for_file(f'content/adventures/{self.language}.yaml').get('adventures')
            # We always create one with english keywords
            self.data["en"] = self.cache_adventure_keywords("en")
            if language in ALL_KEYWORD_LANGUAGES.keys():
                self.data[language] = self.cache_adventure_keywords(language)

    def cache_adventure_keywords(self, language):
        # Sort the adventure to a fixed structure to make sure they are structured the same for each language
        sorted_adventures = {}
        for adventure_index in ADVENTURE_ORDER:
            if self.file.get(adventure_index, None):
                sorted_adventures[adventure_index] = (self.file.get(adventure_index))
        self.file = sorted_adventures
        keyword_data = {}
        for short_name, adventure in self.file.items():
            parsed_adventure = copy.deepcopy(adventure)
            for level in adventure.get('levels'):
                for k, v in adventure.get('levels').get(level).items():
                    parsed_adventure.get('levels').get(level)[k] = v.format(**KEYWORDS.get(language))
            keyword_data[short_name] = parsed_adventure
        return keyword_data

    # Todo TB -> We can also cache this; why not?
    # When customizing classes we only want to retrieve the name, (id) and level of each adventure
    def get_adventure_keyname_name_levels(self):
        if self.debug_mode and not self.data.get("en", None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/adventures/{self.language}.yaml').get('adventures')
            self.data["en"] = self.cache_adventure_keywords("en")
        adventures_dict = {}
        for adventure in self.data["en"].items():
            adventures_dict[adventure[0]] = {adventure[1]['name']: list(adventure[1]['levels'].keys())}
        return adventures_dict

    # Todo TB -> We can also cache this; why not?
    # When filtering on the /explore or /programs page we only want the actual names
    def get_adventure_names(self):
        if self.debug_mode and not self.data.get("en", None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/adventures/{self.language}.yaml').get('adventures')
            self.data["en"] = self.cache_adventure_keywords("en")
        adventures_dict = {}
        for adventure in self.data["en"].items():
            adventures_dict[adventure[0]] = adventure[1]['name']
        return adventures_dict

    def get_adventures(self, keyword_lang="en"):
        if self.debug_mode and not self.data.get(keyword_lang, None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/adventures/{self.language}.yaml').get('adventures')
            self.data[keyword_lang] = self.cache_adventure_keywords(keyword_lang)
        return self.data.get(keyword_lang)

    def has_adventures(self):
        if self.debug_mode and not self.data.get("en", None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/adventures/{self.language}.yaml').get('adventures')
            self.data["en"] = self.cache_adventure_keywords("en")
        return True if self.data.get("en") else False
      
      
# Todo TB -> We don't need these anymore as we guarantee with Weblate that each language file is there
class NoSuchAdventure:
  def get_adventure(self):
    return {}
  

class ParsonsProblem:
  def __init__(self, language):
    self.language = language
    try:
        self.parsons_file = YamlFile.for_file(f'content/parsons/{self.language}.yaml').to_dict()
    except:
        self.parsons_file = {}

  def get_defaults(self, level):
    """Return the level defaults for a given level number."""
    #print(self.parsons_file)
    return copy.deepcopy(self.parsons_file.get(int(level), {}))

  
class NoSuchParsons:
  def get_defaults(self, level):
    return {}


class Quizzes:
    def __init__(self, language):
        self.language = language
        self.keyword_lang = "en"
        self.keywords = YamlFile.for_file(f'content/keywords/{self.keyword_lang}.yaml').to_dict()
        self.quizzes = YamlFile.for_file(f'content/quizzes/{self.language}.yaml').to_dict()
        if not self.quizzes:
            self.quizzes = YamlFile.for_file(f'content/quizzes/en.yaml').to_dict()

    def set_keyword_language(self, language):
        # Todo TB -> We keep the language at "en" for now to make sure nothing changes for the end user
        # We have to change the questions in the quizzes to make sure everything makes sense with dynamic keywords
        return None
        #if language != self.keyword_lang:
        #    self.keyword_lang = language
        #    self.keywords = YamlFile.for_file(f'coursedata/keywords/{self.keyword_lang}.yaml')

    def get_highest_question_level(self, level):
        return len(self.quizzes['levels'].get(level))

    def get_quiz_data_for_level(self, level):
        return self.quizzes['levels'].get(level)

    def get_quiz_data_for_level_question(self, level, question):
        # We have to parse the keywords before returning
        for k, v in self.quizzes['levels'].get(level).get(question).items():
            if isinstance(self.quizzes['levels'].get(level).get(question)[k], str):
                self.quizzes['levels'].get(level).get(question)[k] = self.quizzes['levels'].get(level).get(question)[k].format(**self.keywords)
            elif isinstance(self.quizzes['levels'].get(level).get(question)[k], list):
                options = []
                for option in self.quizzes['levels'].get(level).get(question)[k]:
                    temp = {}
                    for key, value in option.items():
                        temp[key] = value.format(**self.keywords)
                        temp[key] = value.format(**self.keywords)
                    options.append(temp)
                self.quizzes['levels'].get(level).get(question)[k] = options
        return self.quizzes['levels'].get(level).get(question)

# Todo TB -> We don't need these anymore as we guarantee with Weblate that each language file is there
class NoSuchQuiz:
    def get_quiz_data_for_level(self, level):
        return {}
