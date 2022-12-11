import pickle
import os
import unittest


from parameterized import parameterized

import hedy
import utils
from tests.Tester import HedyTester, Snippet, get_list_from_pickle, get_snippets_env_var
from website.yaml_file import YamlFile

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

unique_snippets_table = set()
filtered_language = None
level = None


def collect_snippets(path, hashes_saved=set(), filtered_language=None, only_new_snippets=False):
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
                                except BaseException:
                                    print("Code container is empty...")
                                    continue
                                if not hash(code) in unique_snippets_table:
                                    unique_snippets_table.add(hash(code))
                                    snippet = Snippet(
                                        filename=f,
                                        level=level_number,
                                        field_name=adventure_name + ' snippet #' + str(code_snippet_counter),
                                        code=code,
                                        adventure_name=adventure_name)
                                    if not only_new_snippets or snippet.hash not in hashes_saved:
                                        Hedy_snippets.append(snippet)

                            # code snippets inside start_code
                            try:
                                start_code = level['start_code']
                                if not hash(start_code) in unique_snippets_table:
                                    unique_snippets_table.add(hash(start_code))
                                    snippet = Snippet(
                                        filename=f,
                                        level=level_number,
                                        field_name='start_code',
                                        code=start_code,
                                        adventure_name=adventure_name)
                                    if not only_new_snippets or snippet.hash not in hashes_saved:
                                        Hedy_snippets.append(snippet)

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
                                except BaseException:
                                    print("Code container is empty...")
                                    continue

                                    # test only unique snippets
                                if not hash(code) in unique_snippets_table:
                                    unique_snippets_table.add(hash(code))
                                    snippet = Snippet(
                                        filename=f,
                                        level=level_number,
                                        field_name=adventure_name + ' snippet #' + str(code_snippet_counter),
                                        code=code,
                                        adventure_name=adventure_name)
                                    if not only_new_snippets or snippet.hash not in hashes_saved:
                                        Hedy_snippets.append(snippet)

    return Hedy_snippets


# filtered_language = 'nl'
# use this to filter on 1 lang, zh_Hans for Chinese, nb_NO for Norwegian, pt_PT for Portuguese

only_new_snippets = get_snippets_env_var()

hashes_saved = get_list_from_pickle('adventure_hashes.pkl')

Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../content/adventures',
                                                       filtered_language=filtered_language,
                                                       hashes_saved=hashes_saved,
                                                       only_new_snippets=only_new_snippets)]

# level = 18
# if level:
#     Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.level == level]

# This allows filtering out languages locally, but will throw an error
# on GitHub Actions (or other CI system) so nobody accidentally commits this.
if os.getenv('CI') and (filtered_language or level):
    raise RuntimeError('Whoops, it looks like you left a snippet filter in!')

Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)


class TestsAdventurePrograms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_tests_passed = True
        cls.hashes_saved = hashes_saved
        cls.new_hashes = set()

    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_adventures(self, name, snippet):

        if snippet is not None:
            result = HedyTester.check_Hedy_code_for_errors(snippet)
            if result is not None:
                print(f'\n----\n{snippet.code}\n----')
                print(f'in language {snippet.language} from level {snippet.level} gives error:')
                print(result)
                self.all_tests_passed = False
            else:
                # test passed? save hash!
                self.new_hashes.add(snippet.hash)

            self.assertIsNone(result)  # this looks weird after the is not None but is used by the test runner!

    @classmethod
    def tearDownClass(cls):
        if cls.all_tests_passed:
            # fetch already saved hashes
            all_hashes = cls.hashes_saved | cls.new_hashes  # and merge in the new ones
            with open('adventure_hashes.pkl', 'wb') as f:
                pickle.dump(all_hashes, f)
