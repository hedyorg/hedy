import collections
import attr

from flask import jsonify, render_template, abort, redirect
import courses

class Translations:
  def __init__(self):
    self.data = courses.load_yaml('coursedata/texts.yaml')

  def get_translations(self, language, section):
    # Merge with English when lacking translations
    # Start from a defaultdict
    d = collections.defaultdict(lambda: '???')
    d.update(**self.data.get('en', {}).get(section, {}))
    d.update(**self.data.get(language, {}).get(section, {}))
    return d


def render_assignment_editor(course, assignment_number, menu, translations, version):
  assignment = course.get_assignment(assignment_number)
  if not assignment:
    abort(404)

  arguments_dict = {}

  # Meta stuff
  arguments_dict['course'] = course
  arguments_dict['assignment_nr'] = str(assignment_number)
  arguments_dict['level'] = assignment.level
  arguments_dict['lang'] = course.language
  arguments_dict['next_assignment'] = int(assignment_number) + 1 if int(assignment_number) < course.max_level() else None
  arguments_dict['menu'] = menu
  arguments_dict['latest'] = version
  arguments_dict['selected_page'] = 'code'
  arguments_dict['page_title'] = f'Level {assignment_number} – Hedy'
  arguments_dict['docs'] = [attr.asdict(d) for d in assignment.docs]

  # Translations
  arguments_dict.update(**translations.get_translations(course.language, 'ui'))

  # Actual assignment
  arguments_dict.update(**attr.asdict(assignment))

  return render_template("code-page.html", **arguments_dict)


def render_assignment_docs(doc_type, course, assignment_number, menu, translations):
  assignment = course.get_assignment(assignment_number)
  if not assignment:
    abort(404)

  arguments_dict = {}

  # Meta stuff
  arguments_dict['course'] = course
  arguments_dict['assignment_nr'] = str(assignment_number)
  arguments_dict['pagetitle'] = f'Level {assignment_number}'
  arguments_dict['lang'] = course.language
  arguments_dict['selected_page'] = doc_type
  arguments_dict['docs'] = [attr.asdict(d) for d in assignment.docs]

  # Translations
  arguments_dict.update(**translations.get_translations(course.language, 'ui'))

  # print(repr(assignment_number), course.docs)

  doc = course.docs.get(int(assignment_number), doc_type)
  if not doc:
    # Redirect to code page. Nasty 'import' here to work around
    # cyclic imports.
    import app
    return redirect(app.hedy_link(assignment_number))

  arguments_dict['mkd'] = doc.markdown
  arguments_dict['menu'] = menu
  arguments_dict['page_title'] = f'Level {assignment_number} – ' + doc.front_matter.get('title', '') + ' – Hedy'

  return render_template("per-level-text.html", **arguments_dict)