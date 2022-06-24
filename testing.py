import os
import hedy
from website.yaml_file import YamlFile
import unittest
from tests.Tester import HedyTester, Snippet
from parameterized import parameterized
from hedy_content import ALL_KEYWORD_LANGUAGES

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
                        lines = exercise.get('code_lines')
                        code = ""
                        # The lines have a letter: A: ..., B:...., C:....
                        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                            line = lines.get(letter)
                            if line:
                                code += line + "\n"
                            else:
                                break
                        if hash(code) in unique_snippets_table:
                            print("Identical code already being tested...")
                            continue
                        else:
                            unique_snippets_table.add(hash(code))
                        Hedy_snippets.append(Snippet(filename=file, level=level, field_name=f"{exercise_id}", code=code))
                except:
                    print(f'Problem reading commands yaml for {lang} level {level}')


    return Hedy_snippets

def translate_keywords_in_snippets(snippets):
    # fill keyword dict for all keyword languages
    keyword_dict = {}
    for lang in ALL_KEYWORD_LANGUAGES:
        keyword_dict[lang] = YamlFile.for_file(f'content/keywords/{lang}.yaml').to_dict()
        for k, v in keyword_dict[lang].items():
            if type(v) == str and "|" in v:
                # when we have several options, pick the first one as default
                keyword_dict[lang][k] = v.split('|')[0]

    english_keywords = YamlFile.for_file(f'content/keywords/en.yaml').to_dict()

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


Hedy_snippets = [(s.name, s) for s in collect_snippets(path='content/parsons')]
Hedy_snippets = translate_keywords_in_snippets(Hedy_snippets)


class TestsParsonsPrograms(unittest.TestCase):

    @parameterized.expand(Hedy_snippets)
    def test_parsons(self, name, snippet):
        if snippet is not None:
            print(snippet.code)
            result = HedyTester.validate_Hedy_code(snippet)
            self.assertTrue(result)