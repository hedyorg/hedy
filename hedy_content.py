import copy
import attr
from website.yaml_file import YamlFile

# Define and load all available language data
ALL_LANGUAGES = {
    'id': 'Bahasa Indonesia',
    'de': 'Deutsch',
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'pl': 'Polski',
    'pt_PT': 'Português (pt)',
    'pt_BR': 'Português (br)',
    'fy': 'Frysk',
    'it': 'Italiano',
    'hu': 'Magyar',
    'el': 'Ελληνικά',
    'zh_Hans': "简体中文",
    'nl': 'Nederlands',
    'nb_NO': 'Norsk',
    'sw': 'Swahili',
    'tr': 'Türk',
    'cs': 'Čeština',
    'bg': 'Български',
    'ar': 'عربى',
    'hi': 'हिंदी',
    'bn': 'বাংলা',
}

# Define fall back languages for adventures
FALL_BACK_ADVENTURE = {
    'fy': 'nl',
    'pt_BR': 'pt_PT'
}

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

class Commands:
    def __init__(self, language):
        self.language = language
        self.keyword_lang = "en"
        self.keywords = YamlFile.for_file(f'content/keywords/{self.keyword_lang}.yaml').to_dict()
        self.levels = YamlFile.for_file(f'content/commands/{self.language}.yaml')

    def set_keyword_language(self, language):
        if language != self.keyword_lang:
            self.keyword_lang = language
            self.keywords = YamlFile.for_file(f'content/keywords/{self.keyword_lang}.yaml')

    def get_commands_for_level(self, level):
        # Commands are stored as a list of dicts, so iterate like a list, then get the dict values
        level_commands = copy.deepcopy(self.levels.get(int(level), []))
        for command in level_commands:
            for k, v in command.items():
                command[k] = v.format(**self.keywords)
        return level_commands

    def get_defaults(self, level):
        return copy.deepcopy(self.levels.get(int(level), {}))


class NoSuchCommand:
  def get_commands(self):
    return {}


class Adventures:
  def __init__(self, language):
    self.language = language
    self.keyword_lang = "en"
    self.keywords = YamlFile.for_file(f'content/keywords/{self.keyword_lang}.yaml').to_dict()
    self.adventures_file = YamlFile.for_file(f'content/adventures/{self.language}.yaml')

  def set_keyword_language(self, language):
    if language != self.keyword_lang:
        self.keyword_lang = language
        self.keywords = YamlFile.for_file(f'content/keywords/{self.keyword_lang}.yaml')

    # When customizing classes we only want to retrieve the name, (id) and level of each adventure
  def get_adventure_keyname_name_levels(self):
    adventures = self.adventures_file['adventures']
    adventures_dict = {}
    for adventure in adventures.items():
      adventures_dict[adventure[0]] = {adventure[1]['name']: list(adventure[1]['levels'].keys())}
    return adventures_dict

  def has_adventures(self):
    return self.adventures_file.exists() and self.adventures_file.get('adventures')


class NoSuchAdventure:
  def get_adventure(self):
    return {}

