import copy
import os
import logging

from babel import Locale, languages

from utils import customize_babel_locale
from website.yaml_file import YamlFile
import iso3166

logger = logging.getLogger(__name__)

# Define and load all countries
COUNTRIES = {k: v.name for k, v in iso3166.countries_by_alpha2.items()}
# Iterate through all found country abbreviations
for country in COUNTRIES.keys():
    # Get all spoken languages in this "territory"
    spoken_languages = languages.get_territory_language_info(country).keys()
    found = False
    country_name = None
    # For each language, try to parse the country name -> if correct: adjust in dict and break
    # If we don't find any, keep the English one
    for language in spoken_languages:
        if found:
            break
        try:
            value = language + "_" + country
            lang = Locale.parse(value)
            country_name = lang.get_territory_name(value)
            found = True
        except BaseException:
            pass
    if country_name:
        COUNTRIES[country] = country_name

# Define dictionary for available languages. Fill dynamically later.
ALL_LANGUAGES = {}
ALL_KEYWORD_LANGUAGES = {}

# Todo TB -> We create this list manually, but it would be nice if we find
# a way to automate this as well
NON_LATIN_LANGUAGES = ['ar', 'bg', 'bn', 'el', 'fa', 'hi', 'he', 'pa_PK', 'ru', 'zh_Hans']

# Babel has a different naming convention than Weblate and doesn't support some languages -> fix this manually
CUSTOM_BABEL_LANGUAGES = {'pa_PK': 'pa_Arab_PK', 'tn': 'en', 'tl': 'en'}
# For the non-existing language manually overwrite the display language to make sure it is displayed correctly
CUSTOM_LANGUAGE_TRANSLATIONS = {'tn': 'Setswana', 'tl': 'ᜆᜄᜎᜓᜄ᜔'}
customize_babel_locale(CUSTOM_BABEL_LANGUAGES)

ADVENTURE_NAMES = [
    'default',
    'parrot',
    'fortune',
    'haunted',
    'restaurant',
    'story',
    'songs',
    'turtle',
    'dishes',
    'dice',
    'pressit',
    'rock',
    'calculator',
    'piggybank',
    'quizmaster',
    'language',
    'secret',
    'tic',
    'blackjack',
    'next',
    'end'
]

ADVENTURE_ORDER_PER_LEVEL = {
    1: [
        'default',
        'parrot',
        'rock',
        'story',
        'turtle',
        'restaurant',
        'fortune',
        'haunted',
        'next',
        'end'
    ],
    2: [
        'default',
        'rock',
        'parrot',
        'story',
        'haunted',
        'restaurant',
        'turtle',
        'next',
        'end'
    ],
    3: [
        'default',
        'rock',
        'dice',
        'dishes',
        'fortune',
        'turtle',
        'story',
        'parrot',
        'haunted',
        'restaurant',
        'next',
        'end'
    ],
    4: [
        'default',
        'rock',
        'dice',
        'dishes',
        'turtle',
        'story',
        'haunted',
        'fortune',
        'restaurant',
        'next',
        'end'
    ],
    5: [
        'default',
        'story',
        'language',
        'rock',
        'dice',
        'dishes',
        'parrot',
        'fortune',
        'haunted',
        'restaurant',
        'turtle',
        'pressit',
        'next',
        'end'
    ],
    6: [
        'default',
        'songs',
        'dice',
        'dishes',
        'turtle',
        'calculator',
        'fortune',
        'restaurant',
        'next',
        'end'
    ],
    7: [
        'default',
        'story',
        'songs',
        'turtle',
        'dice',
        'dishes',
        'fortune',
        'restaurant',
        'next',
        'end'
    ],
    8: [
        'default',
        'story',
        'songs',
        'fortune',
        'haunted',
        'restaurant',
        'turtle',
        'next',
        'end'
    ],
    9: [
        'default',
        'rock',
        'story',
        'calculator',
        'haunted',
        'restaurant',
        'next',
        'end'
    ],
    10: [
        'default',
        'rock',
        'dishes',
        'dice',
        'songs',
        'story',
        'fortune',
        'restaurant',
        'calculator',
        'next',
        'end'
    ],
    11: [
        'default',
        'songs',
        'haunted',
        'restaurant',
        'next',
        'end'
    ],
    12: [
        'default',
        'story',
        'fortune',
        'songs',
        'restaurant',
        'calculator',
        'piggybank',
        'secret',
        'next',
        'end'
    ],
    13: [
        'default',
        'restaurant',
        'secret',
        'rock',
        'story',
        'tic',
        'next',
        'end'
    ],
    14: [
        'default',
        'haunted',
        'calculator',
        'piggybank',
        'quizmaster',
        'tic',
        'next',
        'end'
    ],
    15: [
        'default',
        'restaurant',
        'story',
        'dice',
        'rock',
        'calculator',
        'tic',
        'next',
        'end'
    ],
    16: [
        'default',
        'haunted',
        'songs',
        'language',
        'next',
        'end'
    ],
    17: [
        'default',
        'tic',
        'blackjack',
        'next',
        'end'
    ],
    18: [
        'default',
        'next',
        'end'
    ]
}

RESEARCH = {}
for paper in sorted(os.listdir('content/research'),
                    key=lambda x: int(x.split("_")[-1][:-4]),
                    reverse=True):
    # An_approach_to_describing_the_semantics_of_Hedy_2022.pdf -> 2022, An
    # approach to describing the semantics of Hedy
    name = paper.replace("_", " ").split(".")[0]
    name = name[-4:] + ". " + name[:-5]
    RESEARCH[name] = paper

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
        if folder in CUSTOM_LANGUAGE_TRANSLATIONS.keys():
            languages[folder] = CUSTOM_LANGUAGE_TRANSLATIONS.get(folder)
            continue
        locale = Locale.parse(folder)
        languages[folder] = locale.display_name.title()


for lang in sorted(languages):
    ALL_LANGUAGES[lang] = languages[lang]
    if os.path.exists('./grammars/keywords-' + lang + '.lark'):
        ALL_KEYWORD_LANGUAGES[lang] = lang[0:2].upper()  # first two characters

# Load and cache all keyword yamls
KEYWORDS = {}
for lang in ALL_KEYWORD_LANGUAGES.keys():
    KEYWORDS[lang] = dict(YamlFile.for_file(f'content/keywords/{lang}.yaml'))
    for k, v in KEYWORDS[lang].items():
        if isinstance(v, str) and "|" in v:
            # when we have several options, pick the first one as default
            KEYWORDS[lang][k] = v.split('|')[0]


class Commands:
    # Want to parse the keywords only once, they can be cached -> perform this
    # action on server start
    def __init__(self, language):
        self.language = language
        # We can keep these cached, even in debug_mode: files are small and don't
        # influence start-up time much
        self.file = YamlFile.for_file(f'content/cheatsheets/{self.language}.yaml')
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
            # Take a copy -> otherwise we overwrite the parsing
            commands = copy.deepcopy(self.file.get(level))
            for command in commands:
                for k, v in command.items():
                    try:
                        command[k] = v.format(**KEYWORDS.get(language))
                    except IndexError:
                        logger.error(
                            f"There is an issue due to an empty placeholder in line: {v}")
                    except KeyError:
                        logger.error(
                            f"There is an issue due to a non-existing key in line: {v}")
            keyword_data[level] = commands
        return keyword_data

    def get_commands_for_level(self, level, keyword_lang="en"):
        if self.debug_mode and not self.data.get(keyword_lang, None):
            self.data[keyword_lang] = self.cache_keyword_parsing(keyword_lang)
        return self.data.get(keyword_lang, {}).get(int(level), None)


# Todo TB -> We don't need these anymore as we guarantee with Weblate that
# each language file is there


class NoSuchCommand:
    def get_commands_for_level(self, level, keyword_lang):
        return {}


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
            self.file = YamlFile.for_file(
                f'content/adventures/{self.language}.yaml').get('adventures')
            # We always create one with english keywords
            self.data["en"] = self.cache_adventure_keywords("en")
            if language in ALL_KEYWORD_LANGUAGES.keys():
                self.data[language] = self.cache_adventure_keywords(language)

    def cache_adventure_keywords(self, language):
        # Sort the adventure to a fixed structure to make sure they are structured
        # the same for each language
        sorted_adventures = {}
        for adventure_index in ADVENTURE_NAMES:
            if self.file.get(adventure_index, None):
                sorted_adventures[adventure_index] = (self.file.get(adventure_index))
        self.file = sorted_adventures

        keyword_data = {}
        for short_name, adventure in self.file.items():
            parsed_adventure = copy.deepcopy(adventure)
            for level in adventure.get('levels'):
                for k, v in adventure.get('levels').get(level).items():
                    try:
                        parsed_adventure.get('levels').get(
                            level)[k] = v.format(**KEYWORDS.get(language))
                    except IndexError:
                        logger.error(
                            f"There is an issue due to an empty placeholder in line: {v}")
                    except KeyError:
                        logger.error(
                            f"There is an issue due to a non-existing key in line: {v}")
            keyword_data[short_name] = parsed_adventure
        return keyword_data

    # Todo TB -> We can also cache this; why not?
    # When customizing classes we only want to retrieve the name, (id) and level of each adventure
    def get_adventure_keyname_name_levels(self):
        if self.debug_mode and not self.data.get("en", None):
            if not self.file:
                self.file = YamlFile.for_file(
                    f'content/adventures/{self.language}.yaml').get('adventures')
            self.data["en"] = self.cache_adventure_keywords("en")
        adventures_dict = {}
        for adventure in self.data["en"].items():
            adventures_dict[adventure[0]] = {adventure[1]
                                             ['name']: list(adventure[1]['levels'].keys())}
        return adventures_dict

    # Todo TB -> We can also cache this; why not?
    # When filtering on the /explore or /programs page we only want the actual names
    def get_adventure_names(self):
        if self.debug_mode and not self.data.get("en", None):
            if not self.file:
                self.file = YamlFile.for_file(
                    f'content/adventures/{self.language}.yaml').get('adventures')
            self.data["en"] = self.cache_adventure_keywords("en")
        adventures_dict = {}
        for adventure in self.data["en"].items():
            adventures_dict[adventure[0]] = adventure[1]['name']
        return adventures_dict

    def get_adventures(self, keyword_lang="en"):
        if self.debug_mode and not self.data.get(keyword_lang, None):
            if not self.file:
                self.file = YamlFile.for_file(
                    f'content/adventures/{self.language}.yaml').get('adventures')
            self.data[keyword_lang] = self.cache_adventure_keywords(
                keyword_lang)
        return self.data.get(keyword_lang)

    def has_adventures(self):
        if self.debug_mode and not self.data.get("en", None):
            if not self.file:
                self.file = YamlFile.for_file(
                    f'content/adventures/{self.language}.yaml').get('adventures')
            self.data["en"] = self.cache_adventure_keywords("en")
        return True if self.data.get("en") else False

# Todo TB -> We don't need these anymore as we guarantee with Weblate that
# each language file is there


class NoSuchAdventure:
    def get_adventure(self):
        return {}


class ParsonsProblem:
    def __init__(self, language):
        self.language = language
        self.file = {}
        self.data = {}

        self.debug_mode = not os.getenv('NO_DEBUG_MODE')

        if not self.debug_mode:
            self.file = YamlFile.for_file(f'content/parsons/{self.language}.yaml').get('levels')
            # We always create one with english keywords
            self.data["en"] = self.cache_parsons_keywords("en")
            if language in ALL_KEYWORD_LANGUAGES.keys():
                self.data[language] = self.cache_parsons_keywords(language)

    def cache_parsons_keywords(self, language):
        keyword_data = {}
        for level in copy.deepcopy(self.file):
            exercises = copy.deepcopy(self.file.get(level))
            for number, exercise in exercises.items():
                try:
                    exercises.get(number)['code'] = exercises.get(number).get('code').format(**KEYWORDS.get(language))
                except IndexError:
                    logger.error(
                        f"There is an issue due to an empty placeholder in exercise: {number}")
                except KeyError:
                    logger.error(
                        f"There is an issue due to a non-existing key in exercise: {number}")
            keyword_data[level] = exercises
        return keyword_data

    def get_highest_exercise_level(self, level):
        if self.debug_mode and not self.data.get("en", None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/parsons/{self.language}.yaml').get('levels')
            self.data["en"] = self.cache_parsons_keywords("en")
        return len(self.data["en"].get(level, {}))

    def get_parsons_data_for_level(self, level, keyword_lang="en"):
        if self.debug_mode and not self.data.get(keyword_lang, None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/parsons/{self.language}.yaml').get('levels')
            self.data[keyword_lang] = self.cache_parsons_keywords(keyword_lang)
        return self.data.get(keyword_lang, {}).get(level, None)

    def get_parsons_data_for_level_exercise(self, level, excercise, keyword_lang="en"):
        if self.debug_mode and not self.data.get(keyword_lang, None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/parsons/{self.language}.yaml').get('levels')
            self.data[keyword_lang] = self.cache_parsons_keywords(keyword_lang)
        return self.data.get(keyword_lang, {}).get(level, {}).get(excercise, None)


class Quizzes:
    def __init__(self, language):
        self.language = language
        self.file = {}
        self.data = {}

        # For some reason the is_debug_mode() function is not (yet) ready when we call this code
        # So we call the NO_DEBUG_MODE directly from the environment
        # Todo TB -> Fix that the is_debug_mode() function is ready before server start
        self.debug_mode = not os.getenv('NO_DEBUG_MODE')

        if not self.debug_mode:
            self.file = YamlFile.for_file(f'content/quizzes/{self.language}.yaml').to_dict()
            self.data["en"] = self.cache_quiz_keywords("en")
            if language in ALL_KEYWORD_LANGUAGES.keys():
                self.data[language] = self.cache_quiz_keywords(language)

    def cache_quiz_keywords(self, language):
        keyword_data = {}
        for level in copy.deepcopy(self.file):
            questions = copy.deepcopy(self.file.get(level))
            for number, question in questions.items():
                for k, v in question.items():
                    # We have to parse another way for the mp_choice_options
                    if k == "mp_choice_options":
                        options = []
                        for option in copy.deepcopy(v):
                            temp = {}
                            for key, value in option.items():
                                temp[key] = value.format(**KEYWORDS.get(language))
                            options.append(temp)
                        questions[number][k] = options
                    else:
                        questions[number][k] = v.format(**KEYWORDS.get(language))
            keyword_data[level] = questions
        return keyword_data

    def get_highest_question_level(self, level):
        if self.debug_mode and not self.data.get("en", None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/quizzes/{self.language}.yaml').get('levels')
            self.data["en"] = self.cache_quiz_keywords("en")
        return len(self.data["en"].get(level, {}))

    def get_quiz_data_for_level(self, level, keyword_lang="en"):

        if self.debug_mode and not self.data.get(keyword_lang, None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/quizzes/{self.language}.yaml').get('levels')
            self.data[keyword_lang] = self.cache_quiz_keywords(keyword_lang)
        return self.data.get(keyword_lang, {}).get(level, None)

    def get_quiz_data_for_level_question(self, level, question, keyword_lang="en"):
        if self.debug_mode and not self.data.get(keyword_lang, None):
            if not self.file:
                self.file = YamlFile.for_file(f'content/quizzes/{self.language}.yaml').get('levels')
            self.data[keyword_lang] = self.cache_quiz_keywords(keyword_lang)
        return self.data.get(keyword_lang, {}).get(level, {}).get(question, None)


class NoSuchQuiz:
    def get_quiz_data_for_level(self, level, keyword_lang):
        return {}


class Tutorials:
    # Want to parse the keywords only once, they can be cached -> perform this
    # action on server start
    def __init__(self, language):
        self.language = language
        # We can keep these cached, even in debug_mode: files are small and don't
        # influence start-up time much
        self.file = YamlFile.for_file(f'content/tutorials/{self.language}.yaml')
        self.data = {}

        self.debug_mode = not os.getenv('NO_DEBUG_MODE')

        if not self.debug_mode:
            self.data["en"] = self.cache_tutorials("en")
            if language in ALL_KEYWORD_LANGUAGES.keys():
                self.data[language] = self.cache_tutorials(language)

    def cache_tutorials(self, language):
        tutorial_data = {}
        for level in copy.deepcopy(self.file):
            steps = copy.deepcopy(self.file).get(level).get('steps')
            for index, data in steps.items():
                steps[index]['text'] = data['text'].format(**KEYWORDS.get(language))
            tutorial_data[level] = steps
        return tutorial_data

    def get_tutorial_for_level(self, level, keyword_lang="en"):
        if self.debug_mode and not self.data.get(keyword_lang, None):
            self.data[keyword_lang] = self.cache_tutorials(keyword_lang)
        if level not in ["intro", "teacher"]:
            level = int(level)
        return self.data.get(keyword_lang, {}).get(level, None)

    def get_tutorial_for_level_step(self, level, step, keyword_lang="en"):
        if self.debug_mode and not self.data.get(keyword_lang, None):
            self.data[keyword_lang] = self.cache_tutorials(keyword_lang)
        if level not in ["intro", "teacher"]:
            level = int(level)
        return self.data.get(keyword_lang, {}).get(level, {}).get(step, None)


class NoSuchTutorial:
    def get_tutorial_for_level(self, level, keyword_lang):
        return {}
