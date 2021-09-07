import os
import re
import utils
import hedy
import unittest

# Set the current directory to the root Hedy folder
os.chdir(os.path.join (os.getcwd (), __file__.replace (os.path.basename (__file__), '')))

path = '../coursedata/adventures'
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith ('.yaml')]

def check_code(f, level, field_name, code, adventure_name):
    # We ignore empty code snippets
    if len(code) == 0:
        return True
    try:
        hedy.transpile(code, int(level))
    except Exception as E:
        if E.args[0] != 'Has Blanks':  # code with blanks is ok!
            error = f'Invalid {field_name} in file {f} level #{level} adventure {adventure_name}. Error: {E.args[0]}'
            print(error)
            return error
    return True

class TestsAdventurePrograms(unittest.TestCase):

    def test_adventure_snippets(self):
        adventure_fails = []

        for f in files:
            f = os.path.join (path, f)
            yaml = utils.load_yaml_uncached (f)

            for adventure in yaml ['adventures'].values ():
                for level_number in adventure ['levels']:
                    level = adventure ['levels'] [level_number]
                    adventure_name = adventure['name']

                    # start_code
                    result = check_code (f, level_number, 'start_code', level ['start_code'], adventure_name)
                    if result != True:
                        adventure_fails.append(result)

                    code_snippet_counter = 0
                    # code snippets inside story_text
                    for tag in utils.markdown_to_html_tags (level ['story_text']):
                        if tag.name != 'pre' or not tag.contents [0]:
                            continue
                        code_snippet_counter += 1
                        code = tag.contents [0].contents [0]
                        result = check_code (f, level_number, 'story_text code snippet #' + str (code_snippet_counter), code, adventure_name)
                        if result != True:
                            adventure_fails.append(result)

        self.assertEqual([],adventure_fails)
