import collections
import copy
import json

from flask_babel import gettext

from website.yaml_file import YamlFile
import attr
import glob
from os import path
from flask import g
from flask_helpers import render_template
from website.auth import current_user, is_teacher
import utils

class AchievementTranslations:
  def __init__(self):
    self.data = {}

    translations = glob.glob('coursedata/achievements/*.yaml')
    for trans_file in translations:
      lang = path.splitext(path.basename(trans_file))[0]
      self.data[lang] = YamlFile.for_file(trans_file)

  def get_translations(self, language):
    d = collections.defaultdict(lambda: 'Unknown Exception')
    d.update(**self.data.get('en', {}))
    d.update(**self.data.get(language, {}))
    return d

class PageTranslations:
  def __init__(self, page):
    self.data = {}
    translations = glob.glob('coursedata/pages/' + page + '/*.yaml')
    for file in translations:
      lang = path.splitext(path.basename(file))[0]
      self.data[lang] = YamlFile.for_file(file)

  def exists(self):
    """Whether or not any content was found for this page."""
    return len(self.data) > 0

  def get_page_translations(self, language):
    d = collections.defaultdict(lambda: '')
    d.update(**self.data.get('en', {}))
    d.update(**self.data.get(language, {}))
    return d


def render_code_editor_with_tabs(level_defaults, commands, max_level, level_number, version, loaded_program, adventures, customizations, hide_cheatsheet, enforce_developers_mode, teacher_adventures, adventure_name):
  user = current_user()

  if not level_defaults:
    return utils.error_page(error=404,  ui_message=gettext('no_such_level'))


  arguments_dict = {}

  # Meta stuff
  arguments_dict['level_nr'] = str(level_number)
  arguments_dict['level'] = level_number
  arguments_dict['current_page'] = 'hedy'
  arguments_dict['prev_level'] = int(level_number) - 1 if int(level_number) > 1 else None
  arguments_dict['next_level'] = int(level_number) + 1 if int(level_number) < max_level else None
  arguments_dict['customizations'] = customizations
  arguments_dict['hide_cheatsheet'] = hide_cheatsheet
  arguments_dict['enforce_developers_mode'] = enforce_developers_mode
  arguments_dict['teacher_adventures'] = teacher_adventures
  arguments_dict['menu'] = True
  arguments_dict['latest'] = version
  arguments_dict['selected_page'] = 'code'
  arguments_dict['page_title'] = f'Level {level_number} – Hedy'
  arguments_dict['username'] = user['username']
  arguments_dict['is_teacher'] = is_teacher(user)
  arguments_dict['loaded_program'] = loaded_program
  arguments_dict['adventures'] = adventures
  arguments_dict['adventure_name'] = adventure_name

  # Merge level defaults into adventures so it is rendered as the first tab
  arguments_dict.update(**attr.asdict(level_defaults))

  return render_template("code-page.html", **arguments_dict)

def render_specific_adventure(level_defaults, level_number, adventure, prev_level, next_level):
    arguments_dict = {}

    # Meta stuff
    arguments_dict['specific_adventure'] = True
    arguments_dict['level_nr'] = str(level_number)
    arguments_dict['level'] = level_number
    arguments_dict['prev_level'] = prev_level
    arguments_dict['next_level'] = next_level
    arguments_dict['customizations'] = []
    arguments_dict['hide_cheatsheet'] = None
    arguments_dict['enforce_developers_mode'] = None
    arguments_dict['teacher_adventures'] = []
    arguments_dict['menu'] = True
    arguments_dict['latest'] = None
    arguments_dict['selected_page'] = 'code'
    arguments_dict['page_title'] = f'Level {level_number} – Hedy'
    arguments_dict['username'] = None
    arguments_dict['is_teacher'] = None
    arguments_dict['loaded_program'] = None
    arguments_dict['adventures'] = adventure
    arguments_dict['adventure_name'] = None

    # Merge level defaults into adventures so it is rendered as the first tab
    arguments_dict.update(**attr.asdict(level_defaults))

    return render_template("code-page.html", **arguments_dict)
