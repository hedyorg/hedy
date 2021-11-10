import os
import hedy
from website.yaml_file import YamlFile
import utils
import unittest
from Tester import HedyTester, Snippet
from parameterized import parameterized

# file is called tests_z_ so they are executed last
# because programs are more of a priority than level defaults, which change less and take longer to run

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))

def collect_snippets(path):
    Hedy_snippets = []
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.yaml')]
    for file in files:
        file = os.path.join(path, file)
        yaml = YamlFile.for_file(file)

        for level in yaml:
            try:
                level_number = int(level)
            except:
                continue #level nummer geen int -> dan is het oude content, bijv 10-old en is ok
            if level_number > hedy.HEDY_MAX_LEVEL:
                print('content above max level!')
            else:
                # start_code
                Hedy_snippets.append(Snippet(filename=file, level=level, field_name='start_code', code=yaml[level]['start_code']))

                # commands.k.demo_code
                for k, command in enumerate(yaml[level]['commands']):
                    # todo: at one point all commands should have names again!

                    command_text_short = command['name'] if 'name' in command.keys() else command['explanation'][0:10]
                    Hedy_snippets.append(
                        Snippet(filename=file, level=level, field_name='command ' + command_text_short + ' demo_code', code=command['demo_code']))

                # code snippets inside intro_text
                code_snippet_counter = 0
                for tag in utils.markdown_to_html_tags(yaml[level]['intro_text']):
                    if tag.name != 'pre' or not tag.contents[0]:
                        continue
                    code_snippet_counter += 1
                    Hedy_snippets.append(Snippet(filename=file, level=level, field_name='intro_text snippet #' + str(code_snippet_counter),
                                                 code=tag.contents[0].contents[0]))
    return Hedy_snippets


Hedy_snippets = [(s.name, s) for s in collect_snippets(path='../coursedata/level-defaults')]


class TestsLevelDefaultsPrograms(unittest.TestCase):

    @parameterized.expand(Hedy_snippets)
    def test_defaults(self, name, snippet):
        if snippet is not None:
            print(snippet.code)
            result = HedyTester.validate_Hedy_code(snippet)
            self.assertTrue(result)





