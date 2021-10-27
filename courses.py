import json
import copy
import attr
from utils import load_yaml

import docs


class LevelDefaults:
  def __init__(self, language):
    self.language = language

  @property
  def levels(self):
    return load_yaml(f'coursedata/level-defaults/{self.language}.yaml')

  def get_defaults(self, level, sub=0):
    """Return the level defaults for a given level number.

    Returns: Default
    """
    if sub:
      return copy.deepcopy(self.levels.get(str(level) + "-" + str(sub), {}))
    else:
      return copy.deepcopy(self.levels.get(int(level), {}))


class NoSuchDefaults:
  def get_defaults(self, level):
    return {}


class Course:
  def __init__(self, course_name, language, defaults):
    self.course_name = course_name
    self.language = language
    self.defaults = defaults
    self._validated = False
    custom = load_yaml(f'coursedata/course/{self.course_name}/{self.language}.yaml').get('custom')
    self.custom = False if custom is None else custom
    adventures = load_yaml(f'coursedata/course/{self.course_name}/{self.language}.yaml').get('adventures')
    self.adventures = False if adventures is None else adventures

  @property
  def course(self):
    ret = load_yaml(f'coursedata/course/{self.course_name}/{self.language}.yaml').get('course')

    if not ret:
      raise RuntimeError(f'File should have top-level "course" field: coursedata/course/{self.course_name}/{self.language}.yaml')

    if not self._validated:
      self._validated = True
      self.validate_course()
    return ret

  def max_level(self):
    return len(self.course)

  def get_default_text(self, level, sublevel=0):

    """Return the 1-based Assignment from this course."""
    level_ix = int(level) - 1
    if level_ix >= len(self.course): return None

    default_values = {
      "level": str(level),
    }
    default_values.update(**self.defaults.get_defaults(int(level)))

    return DefaultValues(**default_values)

  def validate_course(self):
    """Check that the 'level' and 'step' fields have the right number in the entire course.

    This information is redundant, but it helps the human locate their way in the YAML file.
    """
    for level_i, level in enumerate(self.course):
      expected_value = str(level_i + 1)
      actual_value = level.get('level')

      # Check for sub levels
      subs = level.get('subs')
      if (subs):
        for sub_i, sub in enumerate(subs):
          expected_sub = str(sub_i + 1)
          actual_sub = sub.get('sub')
          if expected_sub != actual_sub:
            raise RuntimeError(f'Expected \'sub: "{expected_sub}"\' but got "{actual_sub}" in {self.course_name}-{self.language}')


      if expected_value != actual_value:
        raise RuntimeError(f'Expected \'level: "{expected_value}"\' but found "{actual_value}" in {self.course_name}-{self.language}')

      assignments = level.get('assignments')
      if assignments:
        for ass_i, ass in enumerate(assignments):
          expected_ass = str(ass_i + 1)
          actual_ass = ass.get('step')
          if expected_value != actual_value:
            raise RuntimeError(f'Expected \'step: "{expected_ass}"\' but got "{actual_ass}" in {self.course_name}-{self.language}')


class NoSuchCourse:
  def get_assignment(self, level, number):
    return None


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

