import os
import re
import utils
import hedy
import unittest

# Set the current directory to the root Hedy folder
os.chdir(os.path.join (os.getcwd (), __file__.replace (os.path.basename (__file__), '')))

path = '../coursedata/level-defaults'
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith ('.yaml')]

def check_code(filename, level, field_name, code):
    # We ignore empty code snippets
    if len(code) == 0:
        return True
    try:
        hedy.transpile(code, int(level))
    except Exception as E:
        if E.args[0] != 'Has Blanks':  # code with blanks is ok!
            filename_shorter = filename.split("/")[3]
            language = filename_shorter.split(".")[0]
            error = f'{language}: level #{level} - {field_name}. Error: {E.args[0]}'
            # We print the error for readability, since otherwise they get accumulated on a long list
            print (error)
            return error
    return True

class TestsLevelDefaultsPrograms(unittest.TestCase):

    def test_level_defaults_snippets(self):
        level_default_fails = []

        for file in files:
            file = os.path.join (path, file)
            yaml = utils.load_yaml_uncached (file)

            for level in yaml:
                # start_code
                result = check_code(file, level, 'start_code', yaml [level] ['start_code'])
                if result != True:
                    level_default_fails.append(result)
                # commands.k.demo_code
                for k, command in enumerate(yaml[level]['commands']):
                    command_text_short = command['explanation'][0:10]
                    result = check_code(file, level, 'command ' + command_text_short + ' demo_code', command['demo_code'])
                    if result != True:
                        level_default_fails.append(result)

                # code snippets inside intro_text
                code_snippet_counter = 0
                for tag in utils.markdown_to_html_tags (yaml [level] ['intro_text']):
                    if tag.name != 'pre' or not tag.contents [0]:
                        continue
                    code_snippet_counter += 1
                    result = check_code(file, level, 'intro_text snippet #' + str (code_snippet_counter), tag.contents [0].contents [0])
                    if result != True:
                        level_default_fails.append(result)

        self.assertEqual(0, len(level_default_fails))
