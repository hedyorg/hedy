import os
import unittest

from parameterized import parameterized

import hedy
from tests.Tester import HedyTester, Snippet
from website.yaml_file import YamlFile

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

unique_snippets_table = set()


def collect_snippets(path):
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
                        command_text_short = command['name'] if 'name' in command.keys(
                        ) else command['explanation'][0:10]
                        Hedy_snippets.append(
                            Snippet(
                                filename=file,
                                level=level,
                                field_name='command ' +
                                command_text_short +
                                ' demo_code',
                                code=command['demo_code']))
                except BaseException:
                    print(f'Problem reading commands yaml for {lang} level {level}')

    return Hedy_snippets


Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../content/cheatsheets')]
Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)

lang = None
# lang = 'fi' #useful if you want to test just 1 language
# if lang:
#     Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.language[:2] == lang]


# This allows filtering out languages locally, but will throw an error
# on GitHub Actions (or other CI system) so nobody accidentally commits this.
if os.getenv('CI') and (lang):
    raise RuntimeError('Whoops, it looks like you left a snippet filter in!')


class TestsCommandPrograms(unittest.TestCase):

    @parameterized.expand(Hedy_snippets)
    def test_defaults(self, name, snippet):
        if snippet is not None:
            print(snippet.code)
            result = HedyTester.check_Hedy_code_for_errors(snippet)
            self.assertIsNone(result)
