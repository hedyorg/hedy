import os
from website.yaml_file import YamlFile
import utils
import unittest
import hedy
from tests.Tester import HedyTester, Snippet
from parameterized import parameterized

# file is called tests_z_ so they are executed last
# because programs are more of a priority than adventures, which change less and take longer to run

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))



def collect_snippets(path):
  Hedy_snippets = []
  files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
  for f in files:
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
                        code = tag.contents[0].contents[0]

                        Hedy_snippets.append(Snippet(f, level_number, adventure_name + ' snippet #' + str(code_snippet_counter), code, adventure_name))

                    # start_code
                    try:
                        start_code = level['start_code']
                        Hedy_snippets.append(Snippet(f, level_number, 'start_code', start_code, adventure_name))

                    except KeyError:
                        #TODO: create startcode not found error
                        pass

  return Hedy_snippets


Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../coursedata/adventures')]
# We replace the code snippet placeholders with actual keywords to the code is valid: {print} -> print
keywords = YamlFile.for_file('../../coursedata/keywords/en.yaml').to_dict()
for snippet in Hedy_snippets:
    snippet[1].code = snippet[1].code.format(**keywords)

class TestsAdventurePrograms(unittest.TestCase):

  @parameterized.expand(Hedy_snippets)
  def test_adventures(self, name, snippet):
    if snippet is not None:
      print(snippet.code)
      result = HedyTester.validate_Hedy_code(snippet)
      self.assertTrue(result)
