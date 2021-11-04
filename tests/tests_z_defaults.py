import os
from website.yaml_file import YamlFile
import utils
import hedy
import unittest
from Tester import HedyTester

# file is called tests_z_ so they are executed last
# because programs are more of a priority than level defaults, which change less and take longer to run

# Set the current directory to the root Hedy folder
os.chdir(os.path.join (os.getcwd (), __file__.replace (os.path.basename (__file__), '')))

path = '../coursedata/level-defaults'
files =[f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith ('.yaml')]

class TestsLevelDefaultsPrograms(unittest.TestCase):

    def test_level_defaults_snippets(self):
        level_default_fails =[]

        for file in files:
            file = os.path.join (path, file)
            yaml = YamlFile.for_file(file)

            for level in yaml:
                # start_code
                result = HedyTester.validate_Hedy_code(file, level, 'start_code', yaml[level]['start_code'], 'level_defaults')
                if result != True:
                    level_default_fails.append(result)
                # commands.k.demo_code
                for k, command in enumerate(yaml[level]['commands']):
                    # todo: has a name now (again?)
                    command_text_short = command['explanation'][0:10]
                    result = HedyTester.validate_Hedy_code(file, level, 'command ' + command_text_short + ' demo_code', command['demo_code'], 'level_defaults')
                    if result != True:
                        level_default_fails.append(result)

                # code snippets inside intro_text
                code_snippet_counter = 0
                for tag in utils.markdown_to_html_tags (yaml[level]['intro_text']):
                    if tag.name != 'pre' or not tag.contents[0]:
                        continue
                    code_snippet_counter += 1
                    result = HedyTester.validate_Hedy_code(file, level, 'intro_text snippet #' + str (code_snippet_counter), tag.contents[0].contents[0], 'level_defaults')
                    if result != True:
                        level_default_fails.append(result)

        self.assertEqual(0, len(level_default_fails))
