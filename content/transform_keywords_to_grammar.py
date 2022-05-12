import collections
import os
import yaml

def extract_Lark_grammar_from_yaml():
    """Creates a lark file in ../grammars/ for  all yaml files located in ../content/keywords/.
    If a keyword is not yet translated, it will use the English translation of the keyword

    Args:
        only_new_lang (bool, optional): Specifies if only a lark file should be created for a new keyword language or for all languages. Defaults to True.
    """
    input_path = '../content/keywords/'
    current_grammar_path = '../grammars/'
    yaml_languages = [f.replace('.yaml', '') for f in os.listdir(input_path) if
                      os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]

    template_lark = os.path.join(current_grammar_path, 'keywords-template.lark')
    with open(template_lark, 'r', encoding='utf-8') as f:
        template = f.read()

    for yaml_lang in yaml_languages:
        yaml_filesname_with_path = os.path.join(input_path, yaml_lang + '.yaml')
        default_yaml_with_path = os.path.join(input_path, 'en' + '.yaml')

        with open(default_yaml_with_path, 'r', encoding='utf-8') as stream:
            en_command_combinations = yaml.safe_load(stream)

        with open(yaml_filesname_with_path, 'r', encoding='utf-8') as stream:
            command_combinations = yaml.safe_load(stream)

        # Create an empty dictionary -> fill with english keywords overwrite all translated once
        translations = collections.defaultdict(lambda: 'Unknown Exception')
        translations.update(en_command_combinations)
        translations.update(command_combinations)

        translated_template = template.format(**translations)

        lark_filesname_with_path = os.path.join(current_grammar_path, 'keywords-' + yaml_lang + '.lark')

        with open(lark_filesname_with_path, 'w', encoding='utf-8') as f:
            f.write(translated_template)

extract_Lark_grammar_from_yaml()