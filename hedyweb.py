import collections
import attr
import glob
from os import path

from flask import abort
from flask_helpers import render_template

import courses
from website.auth import current_user
import re
import utils

class Translations:
  def __init__(self):
    self._data = None

  @property
  def data(self):
    # In debug mode, always reload all translations
    if self._data is None or utils.is_debug_mode():
      translations = glob.glob('coursedata/texts/*.yaml')
      self._data = {}
      for trans_file in translations:
        lang = path.splitext(path.basename(trans_file))[0]
        self._data[lang] = courses.load_yaml(trans_file)
    return self._data

  def get_translations(self, language, section):
    # Merge with English when lacking translations
    # Start from a defaultdict
    d = collections.defaultdict(lambda: '???')
    d.update(**self.data.get('en', {}).get(section, {}))
    d.update(**self.data.get(language, {}).get(section, {}))
    return d


def render_assignment_editor(request, course, level_number, assignment_number, menu, translations, version, loaded_program, adventure_assignments, adventure_name):


  if not assignment:
    abort(404)

  arguments_dict = {}

  # Meta stuff
  arguments_dict['course'] = course
  arguments_dict['level_nr'] = str(level_number)
  arguments_dict['lang'] = course.language
  arguments_dict['prev_level'] = int(level_number) - 1 if int(level_number) > 1 else None
  arguments_dict['next_level'] = int(level_number) + 1 if int(level_number) < course.max_level() else None
  arguments_dict['menu'] = menu
  arguments_dict['latest'] = version
  arguments_dict['selected_page'] = 'code'
  arguments_dict['page_title'] = f'Level {level_number} – Hedy'
  arguments_dict['auth'] = translations.data [course.language] ['Auth']
  arguments_dict['username'] = current_user(request) ['username']
  arguments_dict['loaded_program'] = loaded_program
  arguments_dict['adventure_assignments'] = adventure_assignments
  arguments_dict['adventure_name'] = adventure_name

  # Translations
  arguments_dict.update(**translations.get_translations(course.language, 'ui'))

  # Actual assignment
  arguments_dict.update(**attr.asdict(assignment))

  return render_template("code-page.html", **arguments_dict)
