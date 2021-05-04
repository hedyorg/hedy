import collections
import attr
import glob
import flask
from os import path

from flask import jsonify, render_template, abort, redirect
import courses
from auth import current_user
import utils

class Translations:
  def __init__(self):
    self._data = None

  @property
  def data(self):
    # In debug mode, always reload all translations
    if self._data is None or utils.flask_in_debug_mode():
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


def render_assignment_editor(request, course, level_number, assignment_number, menu, translations, version, loaded_program, adventure_assignments):
  assignment = course.get_assignment(level_number, assignment_number)
  if not assignment:
    abort(404)

  arguments_dict = {}

  # Meta stuff
  arguments_dict['course'] = course
  arguments_dict['level_nr'] = str(level_number)
  arguments_dict['assignment_nr'] = assignment.step  # Give this a chance to be 'None'
  arguments_dict['lang'] = course.language
  arguments_dict['level'] = assignment.level
  arguments_dict['prev_level'] = int(level_number) - 1 if int(level_number) > 1 else None
  arguments_dict['next_level'] = int(level_number) + 1 if int(level_number) < course.max_level() else None
  arguments_dict['next_assignment'] = int(assignment_number) + 1 if int(assignment_number) < course.max_step(level_number) else None
  arguments_dict['menu'] = menu
  arguments_dict['latest'] = version
  arguments_dict['selected_page'] = 'code'
  arguments_dict['page_title'] = f'Level {level_number} – Hedy'
  arguments_dict['docs'] = [attr.asdict(d) for d in assignment.docs]
  arguments_dict['auth'] = translations.data [course.language] ['Auth']
  arguments_dict['username'] = current_user(request) ['username']
  arguments_dict['loaded_program'] = loaded_program
  arguments_dict['adventure_assignments'] = adventure_assignments

  # Translations
  arguments_dict.update(**translations.get_translations(course.language, 'ui'))

  # Actual assignment
  arguments_dict.update(**attr.asdict(assignment))

  # Add markdowns to docs
  for doc in arguments_dict ['docs']:
    doc ['markdown'] = (course.docs.get(int(level_number), doc ['slug']) or {'markdown': ''}).markdown

  return render_template("code-page.html", **arguments_dict)

def render_adventure(adventure_name, adventure, course, request, lang, level_number, menu, translations, version, loaded_program):

  arguments_dict = {}

  arguments_dict['lang'] = lang
  arguments_dict['level_nr'] = str(level_number)
  arguments_dict['level'] = level_number
  arguments_dict['prev_level'] = level_number - 1 if level_number - 1 in adventure ['levels'] else None
  arguments_dict['next_level'] = level_number + 1 if level_number + 1 in adventure ['levels'] else None
  arguments_dict['menu'] = menu
  arguments_dict['latest'] = version
  arguments_dict['selected_page'] = 'code'
  arguments_dict['page_title'] = f'Adventure mode: {adventure ["name"]} {level_number} – Hedy'
  arguments_dict['auth'] = (translations.data.get (lang) or translations.data ['en']) ['Auth']
  arguments_dict['username'] = current_user(request) ['username']
  arguments_dict['loaded_program'] = loaded_program
  arguments_dict['adventure_name'] = adventure_name
  arguments_dict['full_adventure_name'] = adventure ['name']

  # Translations
  arguments_dict.update(**translations.get_translations(lang, 'ui'))

  # Actual assignment
  for key, value in adventure ['levels'] [level_number].items ():
    arguments_dict [key] = value

  if not 'story_text' in arguments_dict:
    arguments_dict ['story_text'] = ''
  if not 'story_commands' in arguments_dict:
    arguments_dict ['story_commands'] = []

  # We use the intro_text and commands from the corresponding Hedy level, if they are not present in the adventure
  hedy_course = course.get_assignment(level_number, None)
  if not 'intro_text' in arguments_dict:
    arguments_dict ['intro_text'] = hedy_course.intro_text
  if not 'commands' in arguments_dict:
    arguments_dict ['commands'] = hedy_course.commands

  return render_template("code-page.html", **arguments_dict)
