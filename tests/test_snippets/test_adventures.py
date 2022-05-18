import os
from website.yaml_file import YamlFile
import utils
import unittest
import hedy
from tests.Tester import HedyTester, Snippet
from parameterized import parameterized
from hedy_content import ALL_KEYWORD_LANGUAGES

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

def translate_keywords_in_snippets(snippets):
    # fill keyword dict for all keyword languages
    keyword_dict = {}
    for lang in ALL_KEYWORD_LANGUAGES:
        keyword_dict[lang] = YamlFile.for_file(f'../../content/keywords/{lang}.yaml').to_dict()
        for k, v in keyword_dict[lang].items():
            if type(v) == str and "|" in v:
                # when we have several options, pick the first one as default
                keyword_dict[lang][k] = v.split('|')[0]
    english_keywords = YamlFile.for_file(f'../../content/keywords/en.yaml').to_dict()

    # We replace the code snippet placeholders with actual keywords to the code is valid: {print} -> print
    for snippet in snippets:
        try:
            if snippet[1].language in ALL_KEYWORD_LANGUAGES.keys():
                snippet[1].code = snippet[1].code.format(**keyword_dict[snippet[1].language])
            else:
                snippet[1].code = snippet[1].code.format(**english_keywords)
        except KeyError:
            print("This following snippet contains an invalid placeholder ...")
            print(snippet)

    return snippets

Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../content/adventures')]

# lang = 'ar' #useful if you want to test just 1 language
# if lang:
#     Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.language[:2] == lang]
#
# level = 15
# if level:
#     Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.level == level]

Hedy_snippets = translate_keywords_in_snippets(Hedy_snippets)

class TestsAdventurePrograms(unittest.TestCase):

  @parameterized.expand(Hedy_snippets)
  def test_adventures(self, name, snippet):
    if snippet is not None:
      print(snippet.code)
      result = HedyTester.validate_Hedy_code(snippet)
      self.assertTrue(result)
