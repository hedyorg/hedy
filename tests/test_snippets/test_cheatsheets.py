import os
import unittest
import pickle

from parameterized import parameterized

import hedy
from tests.Tester import HedyTester, Snippet, get_list_from_pickle, get_snippets_env_var
from website.yaml_file import YamlFile

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

unique_snippets_table = set()


def collect_snippets(path, hashes_saved=set(), only_new_snippets=False):
    Hedy_snippets = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
    for file in files:
        lang = file.split(".")[0]
        file = os.path.join(path, file)
        yaml = YamlFile.for_file(file)

        for level in yaml:
            level_number = int(level)
            if level_number > hedy.HEDY_MAX_LEVEL:
                print('content above max level!')
            else:
                try:
                    # commands.k.demo_code
                    for k, command in enumerate(yaml[level]):
                        # test only unique snippets
                        if not hash(command['demo_code']) in unique_snippets_table:
                            unique_snippets_table.add(hash(command['demo_code']))
                            command_text_short = \
                                command['name'] if 'name' in command.keys()\
                                else command['explanation'][0:10]

                            snippet = Snippet(
                                filename=file,
                                level=level,
                                field_name='command ' +
                                command_text_short +
                                ' demo_code',
                                code=command['demo_code'])
                            if not only_new_snippets or snippet.hash not in hashes_saved:
                                Hedy_snippets.append(snippet)
                except BaseException:
                    print(f'Problem reading commands yaml for {lang} level {level}')

    return Hedy_snippets


hashes_saved = get_list_from_pickle('cheatsheet_hashes.pkl')
only_new_snippets = get_snippets_env_var()

Hedy_snippets = [(s.name, s) for s in collect_snippets(
    path='../../content/cheatsheets',
    hashes_saved=hashes_saved,
    only_new_snippets=only_new_snippets)]
Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)

lang = None
# lang = 'nl' #useful if you want to test just 1 language
# if lang:
#     Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.language[:2] == lang]


# This allows filtering out languages locally, but will throw an error
# on GitHub Actions (or other CI system) so nobody accidentally commits this.
if os.getenv('CI') and (lang):
    raise RuntimeError('Whoops, it looks like you left a snippet filter in!')


class TestsCheatsheetPrograms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_tests_passed = True
        cls.hashes_saved = hashes_saved
        cls.new_hashes = set()

    @parameterized.expand(Hedy_snippets, skip_on_empty=True)
    def test_cheatsheets_programs(self, name, snippet):
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
            with open('cheatsheet_hashes.pkl', 'wb') as f:
                pickle.dump(all_hashes, f)
