import os
import hedy
from website.yaml_file import YamlFile
import utils
import unittest
from tests.Tester import HedyTester, Snippet
from parameterized import parameterized

# file is called tests_z_ so they are executed last
# because programs are more of a priority than level defaults, which change less and take longer to run

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

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

                        command_text_short = command['name'] if 'name' in command.keys() else command['explanation'][0:10]
                        Hedy_snippets.append(
                            Snippet(filename=file, level=level, field_name='command ' + command_text_short + ' demo_code',
                                    code=command['demo_code']))
                except:
                    print(f'Problem reading commands yaml for {lang} level {level}')


    return Hedy_snippets

Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../../content/commands')]

lang = None #useful if you want to test just 1 language
if lang:
    Hedy_snippets = [(name, snippet) for (name, snippet) in Hedy_snippets if snippet.language == lang]

# We replace the code snippet placeholders with actual keywords to the code is valid: {print} -> print
keywords = YamlFile.for_file('../../content/keywords/en.yaml').to_dict()
for snippet in Hedy_snippets:
    snippet[1].code = snippet[1].code.format(**keywords)


class TestsCommandPrograms(unittest.TestCase):

    @parameterized.expand(Hedy_snippets)
    def test_defaults(self, name, snippet):
        if snippet is not None:
            print(snippet.code)
            result = HedyTester.validate_Hedy_code(snippet)
            self.assertTrue(result)





