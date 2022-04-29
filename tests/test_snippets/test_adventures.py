import os
from website.yaml_file import YamlFile
import utils
import unittest
import hedy
from tests.Tester import HedyTester, Snippet
from parameterized import parameterized

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))


def collect_snippets(path):
  Hedy_snippets = []
  files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
  for f in files:
      lang = f.split(".")[0]
      f = os.path.join(path, f)
      yaml = YamlFile.for_file(f)

      for name, adventure in yaml['adventures'].items():
          if not name == 'next': # code in next sometimes uses examples from higher levels so is potentially wrong
            for level_number in adventure['levels']:
                if level_number > hedy.HEDY_MAX_LEVEL:
                    print('content above max level!')
                else:
                    level = adventure['levels'][level_number]
                    adventure_name = adventure['name']

                    code_snippet_counter = 0
                    # code snippets inside story_text
                    for tag in utils.markdown_to_html_tags(level['story_text']):
                        if tag.name != 'pre' or not tag.contents[0]:
                            continue
                        code_snippet_counter += 1
                        try:
                            code = tag.contents[0].contents[0]
                        except:
                            print("Code container is empty...")
                            continue
                        Hedy_snippets.append(Snippet(f, level_number, adventure_name + ' snippet #' + str(code_snippet_counter), code, adventure_name))

                    # start_code
                    try:
                        start_code = level['start_code']
                        Hedy_snippets.append(Snippet(f, level_number, 'start_code', start_code, adventure_name))

                    except KeyError:
                        print(f'Problem reading startcode for {lang} level {level}')
                        pass

  return Hedy_snippets

Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../content/adventures')]

# We replace the code snippet placeholders with actual keywords to the code is valid: {print} -> print
keywords = YamlFile.for_file('../../content/keywords/en.yaml').to_dict()
for snippet in Hedy_snippets:
    try:
        snippet[1].code = snippet[1].code.format(**keywords)
    except KeyError:
        print("This following snippet contains an invalid placeholder ...")
        print(snippet)

class TestsAdventurePrograms(unittest.TestCase):

  @parameterized.expand(Hedy_snippets)
  def test_adventures(self, name, snippet):
    if snippet is not None:
      print(snippet.code)
      result = HedyTester.validate_Hedy_code(snippet)
      self.assertTrue(result)
