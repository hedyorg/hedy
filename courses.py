import json
import copy
import attr
from utils import load_yaml

import docs

import re
from utils import type_check

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
    self.docs = docs.DocCollection(keys=['level', 'slug'], synth={
      'slug': lambda d: docs.slugify(d.front_matter.get('title', None))
    })
    self.docs.load_dir(f'coursedata/course/{course_name}/docs-{language}')
    self._validated = False


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

  def max_step(self, level):
    level_ix = int(level) - 1
    if level_ix >= len(self.course): return 0
    return len(self.course[level_ix].get('assignments', []))

  def get_assignment(self, level, number, sublevel=0):

    """Return the 1-based Assignment from this course."""
    level_ix = int(level) - 1
    if level_ix >= len(self.course): return None

    assignments = self.course[level_ix].get('assignments')

    assignment_values = {
      "level": str(level),
    }
    assignment_values.update(**self.defaults.get_defaults(int(level), sublevel))

    # If we don't have any "assignments", return a default Assignment object
    # based off the level and the level defaults. This is used in the Hedy main
    # course.
    #
    # Otherwise, if this is a course that DOES have assignments, validate and
    # load the data into the accumulator object.
    if assignments:
      step_ix = int(number) - 1
      if step_ix >= len(assignments): return None
      assignment_values.update(**assignments[step_ix])

    assignment_values['commands'] = [Command(**c) for c in assignment_values.get('commands', [])]

    assignment_values['docs'] = [Doc(slug=slug, title=doc.front_matter.get('title'))
                          for slug, doc in self.docs.get(level).items()]

    return Assignment(**assignment_values)

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
class Assignment:
  """A single assignment.

  Either a concrete assignment written in the YAML, or a default-generated
  Assignment.
  """
  level = attr.ib()
  prompt = attr.ib(default='')
  intro_text = attr.ib(default=None)
  start_code = attr.ib(default=None)
  commands = attr.ib(default=None)
  step = attr.ib(default=None)
  docs = attr.ib(default=list)


@attr.s(slots=True, frozen=True)
class Doc:
  slug = attr.ib()
  title = attr.ib()
