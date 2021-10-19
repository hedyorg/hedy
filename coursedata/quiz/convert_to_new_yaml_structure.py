import sys
from ruamel import yaml
from pathlib import Path
from ruamel.yaml import YAML
import ruamel.yaml
from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString


def get_original_quiz(level_source):
    filename = f'en_quiz_questions_lvl{level_source}.yaml'
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.explicit_start = True
    yaml.default_flow_style = False
    quiz_data = yaml.load(Path(filename))
    quiz_data = rewrite_quiz_to_new_structure(quiz_data)
    quiz_data.yaml_add_eol_comment('# <- double quotes added', 'foo', column=20)
    yaml.dump(quiz_data, Path(filename))


def rewrite_quiz_to_new_structure(quiz_data):
    for nr in range(len(quiz_data['questions'])):
        q_nr = nr+1
        if quiz_data['questions'][q_nr-1].get(q_nr):
            options_array = []
            index = 0
            for options in quiz_data['questions'][q_nr - 1].get(q_nr)['mp_choice_options']:
                option_obj = []
                for options_key, options_value in options.items():
                    option_obj.append({DoubleQuotedScalarString(options_key):DoubleQuotedScalarString(options_value)})
                options_array.append({index: option_obj})
                index += 1
            quiz_data['questions'][q_nr - 1].get(q_nr)['mp_choice_options'] = options_array
    return quiz_data


get_original_quiz(1)