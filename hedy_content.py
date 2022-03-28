import copy
import attr
from website.yaml_file import YamlFile


class LevelDefaults:
  def __init__(self, language):
    self.language = language
    self.keyword_lang = "en"
    self.keywords = YamlFile.for_file(f'coursedata/keywords/{self.keyword_lang}.yaml').to_dict()
    self.levels = YamlFile.for_file(f'coursedata/level-defaults/{self.language}.yaml')

  def set_keyword_language(self, language):
      if language != self.keyword_lang:
          self.keyword_lang = language
          self.keywords = YamlFile.for_file(f'coursedata/keywords/{self.keyword_lang}.yaml')

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

    # Todo TB -> We have to improve this coding (a lot!)
    # We use the following section to replace the placeholders with the actual keywords, but this is complex
    # One solution might be: Separate the commands from the level_defaults -> load them separately
    # This way can use a more simplistic structure less keen to mistakes and easier to understand

    # We have to verify if it's a string as the extra examples are stored within a list
    for k,v in default_values.items():
        if isinstance(v, str):
            default_values[k] = v.format(**self.keywords)
        # The commands value is a list of dicts -> we have to parse this separately
        if k == "commands":
            parsed_commands = []
            for command in v:
                temp = {}
                for command_key, command_value in command.items():
                    temp[command_key] = command_value.format(**self.keywords)
                parsed_commands.append(temp)
            default_values[k] = parsed_commands

    default_type = {
      "level": str(level),
    }
    default_type.update(**default_values)

    return DefaultValues(**default_type)

  def get_defaults(self, level):
    """Return the level defaults for a given level number."""

    return copy.deepcopy(self.levels.get(int(level), {}))

class NoSuchDefaults:
  def get_defaults(self, level):
    return {}

class Adventures:
  def __init__(self, language):
    self.language = language
    self.keyword_lang = "en"
    self.keywords = YamlFile.for_file(f'coursedata/keywords/{self.keyword_lang}.yaml').to_dict()
    self.adventures_file = YamlFile.for_file(f'coursedata/adventures/{self.language}.yaml')

  def set_keyword_language(self, language):
    if language != self.keyword_lang:
        self.keyword_lang = language
        self.keywords = YamlFile.for_file(f'coursedata/keywords/{self.keyword_lang}.yaml')

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
  def get_defaults(self, level):
    return {}


@attr.s(slots=True)
class DefaultValues:
  """Default texts for a level"""

  level = attr.ib()
  intro_text = attr.ib(default=None)
  example_code = attr.ib(default=None)
  extra_examples = attr.ib(default=None)
  start_code = attr.ib(default=None)
  commands = attr.ib(default=None)

