import os
import re
import utils
import hedy

path = 'coursedata/adventures'
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith ('.yaml')]

def test_code (f, level, field_name, code):
    # We ignore empty code snippets
    if len (code) == 0:
        return
    try:
        hedy.transpile (code, int (level))
    except:
        print ('Invalid ' + field_name + ' in file ' + f + ', level ' + str (level), code + '\n\n')

for f in files:
    f = os.path.join (path, f)
    yaml = utils.load_yaml_uncached (f)
    for adventure in yaml ['adventures']:
        for level in yaml ['adventures'] [adventure] ['levels']:
            test_code (f, level, 'start_code', yaml ['adventures'] [adventure] ['levels'] [level] ['start_code'])

            # story_text (between triple backticks)
            splitted_story_text = re.split (r'\s*```\n', yaml ['adventures'] [adventure] ['levels'] [level] ['story_text'])
            for k, part in enumerate (splitted_story_text):
                if k % 2 == 0:
                    continue
                # Only the odd parts of the text are code snippets
                test_code (f, level, 'story_text code snippet #' + str (int ((k - 1) / 2) + 1), part)
