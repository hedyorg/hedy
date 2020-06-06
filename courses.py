import json
import copy
import attr
import yaml

import docs

class LevelDefaults:
  def __init__(self, language):
    self.language = language
    self.levels = load_yaml(f'coursedata/level-defaults/{language}.yaml')

  def get_defaults(self, level):
    """Return the level defaults for a given level number.

    Returns: Default
    """
    level_data = copy.deepcopy(self.levels.get(int(level), {}))
    level_data['commands'] = [Command(**c) for c in level_data.get('commands', [])]
    return Defaults(**level_data)

class NoSuchDefaults:
  def get_defaults(self, level):
    return Defaults()


class Course:
  def __init__(self, course_name, language, defaults):
    self.course_name = course_name
    self.language = language
    self.defaults = defaults
    self.course = load_yaml(f'coursedata/course/{course_name}/{language}.yaml')

    self.docs = docs.DocCollection(keys=['level', 'slug'], synth={
      'slug': lambda d: docs.slugify(d.front_matter.get('title', None))
    })
    self.docs.load_dir(f'coursedata/course/{course_name}/docs-{language}')

  def max_level(self, trajectory='default'):
    return len(self.course.get('trajectories', {}).get(trajectory, []))

  def get_assignment(self, number, trajectory='default'):
    """Return the 1-based Assignment from the given trajectory of this course."""
    assignments = self.course.get('trajectories', {}).get(trajectory, [])
    index = int(number) - 1
    if index >= len(assignments): return None

    level = assignments[index]['level']
    assignment = attr.asdict(self.defaults.get_defaults(int(level)))
    assignment.update(**assignments[index])

    assignment['commands'] = [Command(**c) for c in assignment.get('commands', [])]

    assignment['docs'] = [Doc(slug=slug, title=doc.front_matter.get('title'))
                          for slug, doc in self.docs.get(number).items()]

    return Assignment(**assignment)


class NoSuchCourse:
  def get_assignment(self, number, trajectory='default'):
    return None


@attr.s(slots=True, frozen=True)
class Defaults:
  intro_text = attr.ib(default='')
  start_code = attr.ib(default='')
  commands = attr.ib(default=list)


@attr.s(slots=True, frozen=True)
class Command:
  name = attr.ib(default='')
  explanation = attr.ib(default='')
  example = attr.ib(default='')
  demo_code = attr.ib(default='')


@attr.s(slots=True, frozen=True)
class Assignment:
  step = attr.ib()
  level = attr.ib()
  prompt = attr.ib(default='')
  intro_text = attr.ib(default=None)
  start_code = attr.ib(default=None)
  commands = attr.ib(default=None)
  docs = attr.ib(default=list)


@attr.s(slots=True, frozen=True)
class Doc:
  slug = attr.ib()
  title = attr.ib()


def load_yaml(filename):
  try:
    with open(filename, 'r') as f:
      return yaml.safe_load(f)
  except IOError:
    return {}
