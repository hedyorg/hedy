import copy
import attr
from website.yaml_file import YamlFile


class LevelDefaults:
  def __init__(self, language):
    self.language = language
    self.levels = YamlFile.for_file(f'coursedata/level-defaults/{self.language}.yaml')

  def get_defaults(self, level):
    """Return the level defaults for a given level number."""

    return copy.deepcopy(self.levels.get(int(level), {}))

class NoSuchDefaults:
  def get_defaults(self, level):
    return {}

class Adventures:
  def __init__(self, language):
    self.language = language
    self.adventures_file = YamlFile.for_file(f'coursedata/adventures/{self.language}.yaml')

  def has_adventures(self):
    return self.adventures_file.exists() and self.adventures_file.get('adventures')

class NoSuchAdventure:
  def get_defaults(self, level):
    return {}

@attr.s(slots=True, frozen=True)
class Command:
  name = attr.ib(default='')
  explanation = attr.ib(default='')
  example = attr.ib(default='')
  demo_code = attr.ib(default='')


@attr.s(slots=True, frozen=True)
class DefaultValues:
  """Default texts for a level"""

  level = attr.ib()
  intro_text = attr.ib(default=None)
  start_code = attr.ib(default=None)
  commands = attr.ib(default=None)

