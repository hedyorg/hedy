import collections
from website.yaml_file import YamlFile
import attr
import glob
from os import path

from flask import g
from flask_helpers import render_template

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


def render_code_editor_with_tabs(level_defaults, max_level, level_number, translations, version, loaded_program, adventures, restrictions, adventure_name):
  user = current_user()

  if not level_defaults:
    return utils.page_404 (translations, user['username'], g.lang, translations.get_translations (g.lang, 'ui').get ('no_such_level'))


  arguments_dict = {}

  # Meta stuff
  arguments_dict['level_nr'] = str(level_number)
  arguments_dict['level'] = level_number
  arguments_dict['prev_level'] = int(level_number) - 1 if int(level_number) > 1 else None
  arguments_dict['next_level'] = int(level_number) + 1 if int(level_number) < max_level else None
  arguments_dict['example_programs'] = restrictions['example_programs']
  arguments_dict['hide_prev_level'] = restrictions['hide_prev_level']
  arguments_dict['hide_next_level'] = restrictions['hide_next_level']
  arguments_dict['menu'] = True
  arguments_dict['latest'] = version
  arguments_dict['selected_page'] = 'code'
  arguments_dict['page_title'] = f'Level {level_number} – Hedy'
  arguments_dict['auth'] = translations.get_translations (g.lang, 'Auth')
  arguments_dict['username'] = user['username']
  arguments_dict['is_teacher'] = is_teacher(user)
  arguments_dict['loaded_program'] = loaded_program
  arguments_dict['adventures'] = adventures
  arguments_dict['adventure_name'] = adventure_name

  # Translations
  arguments_dict.update(**translations.get_translations(g.lang, 'ui'))

  # Merge level defaults into adventures so it is rendered as the first tab
  arguments_dict.update(**attr.asdict(level_defaults))

  return render_template("code-page.html", **arguments_dict)
