import os
import re
import utils
import hedy
import unittest

path = '../coursedata/adventures'
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith ('.yaml')]


class TestsLevel1(unittest.TestCase):
  level = 1

  def check_code(self, f, level, field_name, code):
      # We ignore empty code snippets
      if len(code) == 0:
          return True
      try:
          hedy.transpile(code, int(level))
      except Exception as E:
          if E.args[0] != 'Has Blanks':  # code with blanks is ok!
              return 'Invalid ' + field_name + ' in file ' + f + ', level ' + str(level) + code

      return True

  def test_adventure_snippets(self):
    for f in files:
      f = os.path.join (path, f)
      yaml = utils.load_yaml_uncached (f)

      adventure_fails = []

      for adventure in yaml ['adventures']:
        for level in yaml ['adventures'] [adventure] ['levels']:

          result = self.check_code (f, level, 'start_code', yaml ['adventures'] [adventure] ['levels'] [level] ['start_code'])
          if result != True:
            adventure_fails.append(result)

          # story_text (between triple backticks)
          splitted_story_text = re.split (r'\s*```\n', yaml ['adventures'] [adventure] ['levels'] [level] ['story_text'])
          for k, part in enumerate (splitted_story_text):
            if k % 2 == 0:
              continue
            # Only the odd parts of the text are code snippets
            result = self.check_code (f, level, 'story_text code snippet #' + str (int ((k - 1) / 2) + 1), part)
            if result != True:
              adventure_fails.append(result)

    self.assertEqual([],adventure_fails)
