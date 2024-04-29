import logging
import os
from os import path

import static_babel_content

from utils import customize_babel_locale
from website.yaml_file import YamlFile
from safe_format import safe_format

logger = logging.getLogger(__name__)

COUNTRIES = static_babel_content.COUNTRIES

# Define dictionary for available languages. Fill dynamically later.
ALL_LANGUAGES = {}
ALL_KEYWORD_LANGUAGES = {}

# Babel has a different naming convention than Weblate and doesn't support some languages -> fix this manually
CUSTOM_BABEL_LANGUAGES = {'pa_PK': 'pa_Arab_PK',
                          'kmr': 'ku_TR',
                          'tl': 'en'}

# For the non-existing language manually overwrite the display language to make sure it is displayed correctly
CUSTOM_LANGUAGE_TRANSLATIONS = {'kmr': 'Kurdî (Tirkiye)',
                                'tl': 'ᜆᜄᜎᜓᜄ᜔'}

customize_babel_locale(CUSTOM_BABEL_LANGUAGES)

# This changes the color of the adventure tab to pink
KEYWORDS_ADVENTURES = {'print_command', 'ask_command', 'is_command', 'sleep_command', 'random_command',
                       'add_remove_command', 'quotation_marks', 'if_command', 'in_command', 'maths', 'repeat_command',
                       'repeat_command_2', 'for_command', 'and_or_command', 'while_command', 'elif_command',
                       'clear_command', 'pressit', 'debugging', 'functions'}

ADVENTURE_ORDER_PER_LEVEL = {
    1: [
        'default',
        'print_command',
        'ask_command',
        'parrot',
        'rock',
        'haunted',
        'story',
        'music',
        'turtle',
        'turtle_draw_it',
        'restaurant',
        'fortune',
        'debugging',
        'parsons',
        'quiz',
    ],
    2: [
        'default',
        'is_command',
        'rock',
        'ask_command',
        'rock_2',
        'haunted',
        'sleep_command',
        'parrot',
        'story',
        'music',
        'restaurant',
        'turtle',
        'turtle_draw_it',
        'debugging',
        'parsons',
        'quiz',
    ],
    3: [
        'default',
        'random_command',
        'dice',
        'rock',
        'music',
        'fortune',
        'restaurant',
        'add_remove_command',
        'parrot',
        'dishes',
        'story',
        'haunted',
        'turtle',
        'turtle_draw_it',
        'debugging',
        'parsons',
        'quiz',
    ],
    4: [
        'default',
        'quotation_marks',
        'rock',
        'dice',
        'dishes',
        'parrot',
        'turtle',
        'turtle_draw_it',
        'clear_command',
        'music',
        'story',
        'haunted',
        'fortune',
        'restaurant',
        'debugging',
        'parsons',
        'quiz',
    ],
    5: [
        'default',
        'if_command',
        'music',
        'language',
        'dice',
        'dishes',
        'story',
        'rock',
        'parrot',
        'haunted',
        'in_command',
        'restaurant',
        'fortune',
        'pressit',
        'turtle',
        'turtle_draw_it',
        'debugging',
        'parsons',
        'quiz',
    ],
    6: [
        'default',
        'maths',
        'music',
        'is_command',
        'songs',
        'dice',
        'dishes',
        'turtle',
        'turtle_draw_it',
        'calculator',
        'fortune',
        'restaurant',
        'debugging',
        'parsons',
        'quiz',
    ],
    7: [
        'default',
        'repeat_command',
        'story',
        'songs',
        'music',
        'dishes',
        'dice',
        'repeat_command_2',
        'fortune',
        'restaurant',
        'pressit',
        'turtle_draw_it',
        'debugging',
        'parsons',
        'quiz',
    ],
    8: [
        'default',
        'repeat_command',
        'fortune',
        'repeat_command_2',
        'songs',
        'music',
        'if_command',
        'story',
        'haunted',
        'restaurant',
        'turtle',
        'turtle_draw_it',
        'debugging',
        'parsons',
        'quiz',
    ],
    9: [
        'default',
        'repeat_command',
        'if_command',
        'rock',
        'story',
        'calculator',
        'music',
        'restaurant',
        'haunted',
        'pressit',
        'turtle',
        'turtle_draw_it',
        'debugging',
        'parsons',
        'quiz',
    ],
    10: [
        'default',
        'for_command',
        'dishes',
        'dice',
        'fortune',
        'turtle',
        'turtle_draw_it',
        'harry_potter',
        'songs',
        'story',
        'rock',
        'calculator',
        'restaurant',
        'debugging',
        'parsons',
        'quiz',
    ],
    11: [
        'default',
        'for_command',
        'years',
        'calculator',
        'songs',
        'restaurant',
        'haunted',
        'turtle_draw_it',
        'debugging',
        'parsons',
        'quiz',
    ],
    12: [
        'default',
        'maths',
        'quotation_marks',
        'functions',
        'story',
        'fortune',
        'music',
        'songs',
        'songs_2',
        'restaurant',
        'calculator',
        'turtle',
        'piggybank',
        'secret',
        'turtle_draw_it',
        'debugging',
        'parsons',
        'quiz',
    ],
    13: [
        'default',
        'and_or_command',
        'secret',
        'functions',
        'music',
        'story',
        'rock',
        'turtle_draw_it',
        'restaurant',
        'calculator',
        'tic',
        'debugging',
        'quiz',
    ],
    14: [
        'default',
        'is_command',
        'guess_my_number',
        'music',
        'haunted',
        'functions',
        'turtle_draw_it',
        'hotel',
        'calculator',
        'calculator_2',
        'piggybank',
        'quizmaster',
        'tic',
        'debugging',
        'quiz',
    ],
    15: [
        'default',
        'while_command',
        'music',
        'turtle_draw_it',
        'restaurant',
        'story',
        'dice',
        'rock',
        'calculator',
        'tic',
        'debugging',
        'quiz',
    ],
    16: [
        'default',
        'random_command',
        'haunted',
        'songs',
        'songs_2',
        'music',
        'language',
        'simon',
        'simon_2',
        'simon_3',
        'debugging',
        'quiz',
    ],
    17: [
        'default',
        'for_command',
        'elif_command',
        'music',
        'tic',
        'hangman',
        'hangman_2',
        'hangman_3',
        'blackjack',
        'blackjack_2',
        'blackjack_3',
        'blackjack_4',
        'debugging',
        'quiz',
    ],
    18: [
        'default',
        'print_command',
        'ask_command',
        'functions',
        'for_command',
        'story',
        'songs',
        'music',
        'debugging'
    ]
}

HOUR_OF_CODE_ADVENTURES = {
    1: [
        'print_command',
        'parrot',
        'turtle',
        'debugging'
    ],
    2: [
        'default',
        'parrot',
        'turtle',
        'debugging'
    ],
    3: [
        'parrot',
        'dishes',
        'turtle',
        'debugging'
    ],
    4: [
        'dishes',
        'parrot',
        'story',
        'debugging'
    ],
    5: [
        'language',
        'parrot',
        'turtle',
        'debugging'
    ],
    6: [
        'songs',
        'dishes',
        'turtle',
        'debugging'
    ],
    7: [
        'songs',
        'dishes',
        'restaurant',
        'debugging'
    ],
    8: [
        'songs',
        'restaurant',
        'turtle',
        'debugging'
    ],
    9: [
        'rock',
        'restaurant',
        'turtle',
        'debugging'
    ],
    10: [
        'dishes',
        'dice',
        'turtle',
        'songs',
        'debugging'
    ],
    11: [
        'years',
        'songs',
        'restaurant',
        'debugging'
    ],
    12: [
        'maths',
        'functions',
        'story',
        'turtle',
        'debugging'
    ],
    13: [
        'story',
        'rock',
        'restaurant',
        'calculator',
        'debugging'
    ],
    14: [
        'guess_my_number',
        'haunted',
        'hotel',
        'calculator',
        'quizmaster',
        'debugging'
    ],
    15: [
        'restaurant',
        'story',
        'dice',
        'rock',
        'debugging'
    ],
    16: [
        'haunted',
        'songs',
        'language',
        'debugging'
    ],
    17: [
        'blackjack',
        'debugging'
    ],
    18: [
        'story',
        'songs',
        'debugging'
    ]
}

# We must find our data relative to this .py file. This will give the
# correct answer both for when Hedy is run as a webserver on Heroku, as well
# as when it has been bundled using pyinstaller.
data_root = path.dirname(__file__)

content_dir = path.join(data_root, 'content')
translations_dir = path.join(data_root, 'translations')

RESEARCH = {}
for paper in sorted(os.listdir(f'{content_dir}/research'),
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
if not os.path.isdir(translations_dir):
    # should not be possible, but if it's moved someday, EN would still be working.
    ALL_LANGUAGES['en'] = 'English'
    ALL_KEYWORD_LANGUAGES['en'] = 'EN'

for folder in os.listdir(translations_dir):
    locale_dir = os.path.join(translations_dir, folder, 'LC_MESSAGES')
    if not os.path.isdir(locale_dir):
        continue
    if filter(lambda x: x.endswith('.mo'), os.listdir(locale_dir)):
        languages[folder] = CUSTOM_LANGUAGE_TRANSLATIONS.get(folder,
                                                             static_babel_content.LANGUAGE_NAMES.get(folder, folder))


for lang in sorted(languages):
    ALL_LANGUAGES[lang] = languages[lang]
    if os.path.exists(path.join(data_root, './grammars/keywords-' + lang + '.lark')):
        ALL_KEYWORD_LANGUAGES[lang] = lang[0:2].upper()  # first two characters

# Load and cache all keyword yamls
KEYWORDS = {}
for lang in ALL_KEYWORD_LANGUAGES.keys():
    KEYWORDS[lang] = YamlFile.for_file(f'{content_dir}/keywords/{lang}.yaml').to_dict()
    for k, v in KEYWORDS[lang].items():
        if isinstance(v, str) and "|" in v:
            # when we have several options, pick the first one as default
            # Some keys are ints, turn them into strings
            KEYWORDS[lang][k] = v.split('|')[0]


class StructuredDataFile:
    """Base class for all data files in the content directory."""

    def __init__(self, filename):
        self.filename = filename
        self._file = None

    @property
    def file(self):
        """Lazily load the requested file."""
        if not self._file:
            self._file = YamlFile.for_file(self.filename)
        return self._file


class Commands(StructuredDataFile):
    def __init__(self, language):
        self.language = language
        super().__init__(f'{content_dir}/cheatsheets/{self.language}.yaml')

    def get_commands_for_level(self, level, keyword_lang):
        return deep_translate_keywords(self.file.get(int(level), {}), keyword_lang)


def deep_translate_keywords(yaml, keyword_language):
    try:
        """Recurse through a data structure and replace keyword placeholders in any strings we encounter."""
        if isinstance(yaml, str):
            # this is used to localize adventures linked in slides (PR 3860)
            yaml = yaml.replace('/raw', f'/raw?keyword_language={keyword_language}')
            return safe_format(yaml, **KEYWORDS.get(keyword_language))
        if isinstance(yaml, list):
            return [deep_translate_keywords(e, keyword_language) for e in yaml]
        if isinstance(yaml, dict):
            return {k: deep_translate_keywords(v, keyword_language) for k, v in yaml.items()}
        return yaml
    except ValueError as E:
        raise ValueError(f'Issue in language {keyword_language}. Offending yaml: {yaml}. Error: {E}')
    except TypeError as E:
        raise TypeError(f'Issue in language {keyword_language}. Offending yaml: {yaml}. Error: {E}')


def get_localized_name(name, keyword_lang):
    return safe_format(name, **KEYWORDS.get(keyword_lang))

# Todo TB -> We don't need these anymore as we guarantee with Weblate that
# each language file is there


class NoSuchCommand:
    def get_commands_for_level(self, level, keyword_lang):
        return {}


class Adventures(StructuredDataFile):
    def __init__(self, language):
        self.language = language
        super().__init__(f'{content_dir}/adventures/{self.language}.yaml')

    def get_adventure_keyname_name_levels(self):
        return {aid: {adv['name']: list(adv['levels'].keys())} for aid, adv in self.file.get('adventures', {}).items()}

    def get_sorted_level_programs(self, programs, adventure_names):
        programs_by_level = []
        for item in programs:
            programs_by_level.append(
                {'level': item['level'],
                 'adventure_name': item.get('adventure_name', item['name']),
                 }
            )

        sort = {}

        for program in programs_by_level:
            if program['level'] in sort:
                sort[program['level']].append(adventure_names.get(program['adventure_name'], program['adventure_name']))
            else:
                sort[program['level']] = [adventure_names.get(program['adventure_name'], program['adventure_name'])]
        for level, adventures in sort.copy().items():
            sort[level] = sorted(adventures, key=lambda s: s.lower() if s else "")

        return dict(sorted(sort.items(), key=lambda item: item[0]))

    def get_sorted_adventure_programs(self, programs, adventure_names):
        programs_by_adventure = []
        for item in programs:
            if item.get('adventure_name'):
                programs_by_adventure.append(
                    {'adventure_name': adventure_names.get(item.get('adventure_name')) or item.get('adventure_name'),
                     'level': item['level'],
                     }
                )

        sort = {}
        for program in programs_by_adventure:
            if program['adventure_name'] in sort:
                sort[program['adventure_name']].append(program['level'])
            else:
                sort[program['adventure_name']] = [program['level']]
        for adventure, levels in sort.copy().items():
            sort[adventure] = sorted(levels, key=lambda item: item)

        return {key: sort[key]
                for key in sorted(sort.keys(), key=lambda s: s.lower() if s else "")}

    def get_adventure_names(self, keyword_lang):
        return {aid: adv['name'] for aid, adv in deep_translate_keywords(
            self.file.get('adventures'), keyword_lang).items()}

    def get_adventures(self, keyword_lang="en"):
        return deep_translate_keywords(self.file.get('adventures'), keyword_lang)

    def get_adventures_subset(self, subset=["print_command", "parrot"], keyword_lang="en"):
        adventures = {aid: adv for aid, adv in self.file.get('adventures', {}).items() if aid in subset}
        return deep_translate_keywords(adventures, keyword_lang)

    def has_adventures(self):
        return True if self.file.get('adventures') else False


class NoSuchAdventure:
    def get_adventure(self):
        return {}


class ParsonsProblem(StructuredDataFile):
    def __init__(self, language):
        self.language = language
        super().__init__(f'{content_dir}/parsons/{self.language}.yaml')

    def get_highest_exercise_level(self, level):
        return max(int(lnum) for lnum in self.file.get('levels', {}).get(level, {}).keys())

    def get_parsons_data_for_level(self, level, keyword_lang="en"):
        return deep_translate_keywords(self.file.get('levels', {}).get(level, None), keyword_lang)

    def get_parsons_data_for_level_exercise(self, level, excercise, keyword_lang="en"):
        return deep_translate_keywords(self.file.get('levels', {}).get(level, {}).get(excercise), keyword_lang)


class Quizzes(StructuredDataFile):
    def __init__(self, language):
        self.language = language
        super().__init__(f'{content_dir}/quizzes/{self.language}.yaml')

    def get_highest_question_level(self, level):
        return max(int(k) for k in self.file.get('levels', {}).get(level, {}))

    def get_quiz_data_for_level(self, level, keyword_lang="en"):
        return deep_translate_keywords(self.file.get('levels', {}).get(level), keyword_lang)

    def get_quiz_data_for_level_question(self, level, question, keyword_lang="en"):
        return deep_translate_keywords(self.file.get('levels', {}).get(level, {}).get(question), keyword_lang)


class NoSuchQuiz:
    def get_quiz_data_for_level(self, level, keyword_lang):
        return {}


class Tutorials(StructuredDataFile):
    # Want to parse the keywords only once, they can be cached -> perform this
    # action on server start
    def __init__(self, language):
        self.language = language
        super().__init__(f'{content_dir}/tutorials/{self.language}.yaml')

    def get_tutorial_for_level(self, level, keyword_lang="en"):
        if level not in ["intro", "teacher"]:
            level = int(level)
        return deep_translate_keywords(self.file.get(level, None), keyword_lang)

    def get_tutorial_for_level_step(self, level, step, keyword_lang="en"):
        if level not in ["intro", "teacher"]:
            level = int(level)
        return deep_translate_keywords(self.file.get(level, {}).get('steps', {}).get(step), keyword_lang)


class NoSuchTutorial:
    def get_tutorial_for_level(self, level, keyword_lang):
        return {}


class Slides(StructuredDataFile):
    def __init__(self, language):
        self.language = language
        super().__init__(f'{content_dir}/slides/{self.language}.yaml')

    def get_slides_for_level(self, level, keyword_lang="en"):
        return deep_translate_keywords(self.file.get('levels', {}).get(level), keyword_lang)


class NoSuchSlides:
    def get_slides_for_level(self, level, keyword_lang):
        return {}


class NoSuchTags:
    def get_tags(self):
        return {}


class Tags(StructuredDataFile):
    def __init__(self, language):
        self.language = language
        super().__init__(f'{content_dir}/tags/{self.language}.yaml')

    def get_tags_names(self):
        return {tid: tags['items'] for tid, tags in self.file.get('tags', {}).items()}

    def get_tags(self, keyword_lang="en"):
        return deep_translate_keywords(self.file.get('tags'), keyword_lang)

    def has_tags(self):
        return True if self.file.get('tags') else False
