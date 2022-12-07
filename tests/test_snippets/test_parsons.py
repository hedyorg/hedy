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
        levels = yaml.get('levels')

        for level, content in levels.items():
            level_number = int(level)
            if level_number > hedy.HEDY_MAX_LEVEL:
                print('content above max level!')
            else:
                try:
                    for exercise_id, exercise in levels[level].items():
                        code = exercise.get('code')
                        # test only unique snippets
                        if not hash(code) in unique_snippets_table:
                            unique_snippets_table.add(hash(code))
                        Hedy_snippets.append(
                            Snippet(
                                filename=file,
                                level=level,
                                field_name=f"{exercise_id}",
                                code=code))
                except BaseException:
                    print(f'Problem reading commands yaml for {lang} level {level}')

    return Hedy_snippets


Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../content/parsons')]
Hedy_snippets = HedyTester.translate_keywords_in_snippets(Hedy_snippets)


class TestsParsonsPrograms(unittest.TestCase):

    @parameterized.expand(Hedy_snippets)
    def test_parsons(self, name, snippet):
        if snippet is not None:
            print(snippet.code)
            result = HedyTester.check_Hedy_code_for_errors(snippet)
            self.assertIsNone(result)
