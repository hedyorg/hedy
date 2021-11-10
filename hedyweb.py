import collections
import os

from website.yaml_file import YamlFile
import attr
import glob
from os import path

from flask import abort, session
from flask_helpers import render_template

import courses
from website.auth import current_user
import re
import utils
from config import config
from website import database
import hedy_content
from website.auth import current_user, is_teacher 
import re
import utils
from config import config

class Translations:
  def __init__(self):
    self.data = {}

    translations = glob.glob('coursedata/texts/*.yaml')
    for trans_file in translations:
      lang = path.splitext(path.basename(trans_file))[0]
      self.data[lang] = YamlFile.for_file(trans_file)

  def get_translations(self, language, section):
    # Merge with English when lacking translations
    # Start from a defaultdict
    d = collections.defaultdict(lambda: 'Unknown Exception')
    d.update(**self.data.get('en', {}).get(section, {}))
    d.update(**self.data.get(language, {}).get(section, {}))
    return d


def render_code_editor_with_tabs(request, level_defaults, lang, max_level, level_number, menu, translations, version, loaded_program, adventures, adventure_name):
  user = current_user()

  if not level_defaults:
    return utils.page_404 (translations, menu, user['username'], lang, translations.get_translations (lang, 'ui').get ('no_such_level'))


  if course.custom:
    adventures = [x for x in adventures if x['short_name'] in course.adventures]

  arguments_dict = {}

  # Meta stuff
  arguments_dict['level_nr'] = str(level_number)
  arguments_dict['sublevel'] = str(sublevel) if (sublevel) else None
  arguments_dict['lang'] = course.language
  arguments_dict['level'] = defaults.level
  arguments_dict['prev_level'] = int(level_number) - 1 if int(level_number) > 1 else None
  arguments_dict['next_level'] = int(level_number) + 1 if int(level_number) < course.max_level() else None
  arguments_dict['lock_level'] = (database.Database()).get_level(current_user (request) ['username']) 
  arguments_dict['menu'] = menu
  arguments_dict['latest'] = version
  arguments_dict['selected_page'] = 'code'
  arguments_dict['page_title'] = f'Level {level_number} – Hedy'
  arguments_dict['auth'] = translations.get_translations (lang, 'Auth')
  arguments_dict['username'] = user['username']
  arguments_dict['is_teacher'] = is_teacher(user)
  arguments_dict['loaded_program'] = loaded_program
  arguments_dict['adventures'] = adventures
  arguments_dict['adventure_name'] = adventure_name
  arguments_dict['quiz_data_level'] = quiz_data_level
  arguments_dict['quiz_enabled'] = config['quiz-enabled'] and course.language == 'nl'

  # level info 
  arguments_dict['level_info1'] = ['1', '2', '3', '4', '5', '6', '7', '8',
                                  '9', '10', '11', '12']
  arguments_dict['level_info2']   =  [ '13', '14', '15', '16','17']

  # Translations
  arguments_dict.update(**translations.get_translations(lang, 'ui'))

  # Merge level defaults into adventures so it is rendered as the first tab
  arguments_dict.update(**attr.asdict(level_defaults))

  return render_template("code-page.html", **arguments_dict)
