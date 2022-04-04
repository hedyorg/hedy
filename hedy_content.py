import copy
import attr
from website.yaml_file import YamlFile
import iso3166

# Define and load all countries
COUNTRIES = {k: v.name for k, v in iso3166.countries_by_alpha2.items()}

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

class LevelDefaults:
  def __init__(self, language):
    self.language = language
    self.keyword_lang = "en"
    self.keywords = YamlFile.for_file(f'content/keywords/{self.keyword_lang}.yaml').to_dict()
    self.levels = YamlFile.for_file(f'content/level-defaults/{self.language}.yaml')

  def set_keyword_language(self, language):
      if language != self.keyword_lang:
          self.keyword_lang = language
          self.keywords = YamlFile.for_file(f'content/keywords/{self.keyword_lang}.yaml')

  def max_level(self):
    all_levels = sorted(self.levels.keys()) # We should sort this to make sure the max_level returned is correct
    max_consecutive_level = 1
    previous_level = 0
    for level in all_levels:
      if level == previous_level + 1:
        previous_level = level
        max_consecutive_level = level
      else:
        return previous_level
    return max_consecutive_level

  def get_defaults_for_level(self, level):
    #grabs level defaults from yaml and converts to DefaultValues type
    default_values = copy.deepcopy(self.levels[level])

    # Sometimes we have multiple text and example_code -> iterate these and add as well!
    extra_examples = []
    for i in range(2, 10):
        extra_example = {}
        if default_values.get('intro_text_' + str(i)):
            extra_example['intro_text'] = default_values.get('intro_text_' + str(i)).format(**self.keywords)
            default_values.pop('intro_text_' + str(i))
            if default_values.get('example_code_' + str(i)):
                extra_example['example_code'] = default_values.get('example_code_' + str(i)).format(**self.keywords)
                default_values.pop('example_code_' + str(i))
            extra_examples.append(extra_example)
        else:
            break
    default_values['extra_examples'] = extra_examples
    for k,v in default_values.items():
        if isinstance(v, str):
            default_values[k] = v.format(**self.keywords)
    default_type = {
      "level": str(level),
    }
    default_type.update(**default_values)
    return DefaultValues(**default_type)

  def get_defaults(self, level):
    """Return the level defaults for a given level number."""

    return copy.deepcopy(self.levels.get(int(level), {}))


class NoSuchDefaults:
  def get_defaults(self):
    return {}


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


@attr.s(slots=True)
class DefaultValues:
  """Default texts for a level"""

  level = attr.ib()
  intro_text = attr.ib(default=None)
  example_code = attr.ib(default=None)
  extra_examples = attr.ib(default=None)
  start_code = attr.ib(default=None)

