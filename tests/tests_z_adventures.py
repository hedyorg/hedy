import os
import re
from website.yaml_file import YamlFile
import utils
import hedy
import unittest

# file is called tests_z_ so they are executed last
# because programs are more of a priority than adventures, which change less and take longer to run

# Set the current directory to the root Hedy folder
os.chdir(os.path.join (os.getcwd (), __file__.replace (os.path.basename (__file__), '')))

path = '../coursedata/adventures'
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith ('.yaml')]


class TestsAdventurePrograms(unittest.TestCase):

    def test_adventure_snippets(self):
        adventure_fails = []

        for f in files:
            f = os.path.join(path, f)
            yaml = YamlFile.for_file(f)

            for adventure in yaml['adventures'].values ():
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
                            code_snippet_counter += 1
                            code = tag.contents[0].contents[0]

                            result = check_code(f, level_number, 'story_text code snippet #' + str (code_snippet_counter), code, adventure_name)
                            if result != True:
                                adventure_fails.append(result)

                        # start_code
                        try:
                            start_code = level['start_code']
                            result = check_code(f, level_number, 'start_code', start_code, adventure_name)
                            if result != True:
                                adventure_fails.append(result)
                        except KeyError:
                            #create startcode not found error
                            message = f'Adventure {adventure_name} misses start_code at level {level_number}'
                            adventure_fails.append(message)
                            print(message)

        self.assertEqual(0, len(adventure_fails))
