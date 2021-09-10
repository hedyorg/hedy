import collections
import os

import attr
import glob
from os import path

from flask import abort
from flask_helpers import render_template

import courses
from website.auth import current_user, is_teacher
import re
import utils
from config import config

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
    d = collections.defaultdict(lambda: 'Unknown Exception')
    d.update(**self.data.get('en', {}).get(section, {}))
    d.update(**self.data.get(language, {}).get(section, {}))
    return d


def render_code_editor_with_tabs(request, course, level_number, menu, translations, version, loaded_program, adventures, adventure_name):

  if os.path.isfile(f'coursedata/quiz/quiz_questions_lvl{level_number}.yaml'):
    quiz_data = utils.load_yaml(f'coursedata/quiz/quiz_questions_lvl{level_number}.yaml')
    quiz_data_level = quiz_data['level']
  else:
    quiz_data_level = 0

  sublevel = None
  if isinstance (level_number, str) and re.match ('\d+-\d+', level_number):
    sublevel     = int (level_number [level_number.index ('-') + 1])
    level_number = int (level_number [0:level_number.index ('-')])

  defaults = course.get_default_text(level_number, sublevel)

  if not defaults:
    abort(404)

  if course.custom:
    adventures = [x for x in adventures if x['short_name'] in course.adventures]

  arguments_dict = {}

  # Meta stuff
  arguments_dict['course'] = course
  arguments_dict['level_nr'] = str(level_number)
  arguments_dict['sublevel'] = str(sublevel) if (sublevel) else None
  arguments_dict['lang'] = course.language
  arguments_dict['level'] = defaults.level
  arguments_dict['prev_level'] = int(level_number) - 1 if int(level_number) > 1 else None
  arguments_dict['next_level'] = int(level_number) + 1 if int(level_number) < course.max_level() else None
  arguments_dict['menu'] = menu
  arguments_dict['latest'] = version
  arguments_dict['selected_page'] = 'code'
  arguments_dict['page_title'] = f'Level {level_number} – Hedy'
  arguments_dict['auth'] = translations.get_translations (course.language, 'Auth')
  arguments_dict['username'] = current_user(request) ['username']
  arguments_dict['is_teacher'] = is_teacher(request)
  arguments_dict['loaded_program'] = loaded_program
  arguments_dict['adventures'] = adventures
  arguments_dict['adventure_name'] = adventure_name
  arguments_dict['quiz_data_level'] = quiz_data_level
  arguments_dict['quiz_enabled'] = config['quiz-enabled'] and course.language == 'nl'

  # Translations
  arguments_dict.update(**translations.get_translations(course.language, 'ui'))

  # Actual assignment
  arguments_dict.update(**attr.asdict(defaults))

  return render_template("code-page.html", **arguments_dict)
