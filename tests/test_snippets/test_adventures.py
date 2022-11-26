import os
import unittest

from parameterized import parameterized

import hedy
import utils
from tests.Tester import HedyTester, Snippet
from website.yaml_file import YamlFile

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

unique_snippets_table = set()
filtered_language = None
level = None


def collect_snippets(path, filtered_language=None):
    Hedy_snippets = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
    for f in files:
        lang = f.split(".")[0]
        if not filtered_language or (filtered_language and lang == filtered_language):
            f = os.path.join(path, f)
            yaml = YamlFile.for_file(f)

            for name, adventure in yaml['adventures'].items():
                # code in next sometimes uses examples from higher levels so is potentially wrong
                if not name == 'next':
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
                                # Can be used to catch more languages with example codes in the story_text
                                # feedback = f"Example code in story text {lang}, {adventure_name},
                                # {level_number}, not recommended!"
                                # print(feedback)
                                code_snippet_counter += 1
                                try:
                                    code = tag.contents[0].contents[0]
                                    if hash(code) in unique_snippets_table:

                                        continue
                                    else:
                                        unique_snippets_table.add(hash(code))
                                except BaseException:
                                    print("Code container is empty...")
                                    continue
                                Hedy_snippets.append(
                                    Snippet(
                                        f,
                                        level_number,
                                        adventure_name +
                                        ' snippet #' +
                                        str(code_snippet_counter),
                                        code,
                                        adventure_name))
                            # code snippets inside start_code
                            try:
                                start_code = level['start_code']
                                if hash(start_code) in unique_snippets_table:

                                    continue
                                else:
                                    unique_snippets_table.add(hash(start_code))
                                Hedy_snippets.append(Snippet(f, level_number, 'start_code', start_code, adventure_name))
                            except KeyError:
                                print(f'Problem reading startcode for {lang} level {level}')
                                pass
                            # Code snippets inside example code
                            try:
                                example_code = utils.markdown_to_html_tags(level['example_code'])
                            except Exception as E:
                                print(E)
                            for tag in example_code:
                                if tag.name != 'pre' or not tag.contents[0]:
                                    continue
                                code_snippet_counter += 1
                                try:
                                    code = tag.contents[0].contents[0]
                                    # test only unique snippets
                                    if hash(code) in unique_snippets_table:
                                        continue
                                    else:
                                        unique_snippets_table.add(hash(code))
                                except BaseException:
                                    print("Code container is empty...")
                                    continue
                                Hedy_snippets.append(
                                    Snippet(
                                        f,
                                        level_number,
                                        adventure_name +
                                        ' snippet #' +
                                        str(code_snippet_counter),
                                        code,
                                        adventure_name))

    return Hedy_snippets

# filtered_language = 'en'
# use this to filter on 1 lang, zh_Hans for Chinese, nb_NO for Norwegian, pt_PT for Portuguese
# filtered_language = 'en'


Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../content/adventures',
                                                       filtered_language=filtered_language)]

# level = 18
# if level:
#     Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.level == level]

# This allows filtering out languages locally, but will throw an error
# on GitHub Actions (or other CI system) so nobody accidentally commits this.
if os.getenv('CI') and (filtered_language or level):
    raise RuntimeError('Whoops, it looks like you left a snippet filter in!')


Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)


class TestsAdventurePrograms(unittest.TestCase):

    @parameterized.expand(Hedy_snippets)
    def test_adventures(self, name, snippet):
        if snippet is not None:
            print(snippet.code)
            result = HedyTester.check_Hedy_code_for_errors(snippet)
            self.assertIsNone(result)
