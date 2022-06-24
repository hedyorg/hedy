import os

import hedy
from tests.Tester import Snippet
from website.yaml_file import YamlFile


def get_snippets():
    Hedy_snippets = []
    path = "content/parsons"
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
                                code += line
                            else:
                                break
                        Hedy_snippets.append(Snippet(filename=file, level=level, field_name="Parsons" + "#" + lang + "#" + exercise_id,code=code))
                except:
                    print(f'Problem reading commands yaml for {lang} level {level}')
    return Hedy_snippets

snippets = get_snippets()
print(snippets)