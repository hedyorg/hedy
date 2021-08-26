import os
import re
import utils
import hedy

path = 'coursedata/level-defaults'
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
    for level in yaml:
        # start_code
        test_code (f, level, 'start_code', yaml [level] ['start_code'])
        # commands.k.demo_code
        for k, command in enumerate (yaml [level] ['commands']):
            test_code (f, level, 'command #' + str (k + 1) + ' demo_code', command ['demo_code'])

        # intro_text (between triple backticks)
        splitted_intro = re.split (r'\s*```\n', yaml [level] ['intro_text'])
        for k, part in enumerate (splitted_intro):
            if k % 2 == 0:
                continue
            # Only the odd parts of the text are code snippets
            test_code (f, level, 'intro_text code snippet #' + str ((k - 1) / 2), part)
