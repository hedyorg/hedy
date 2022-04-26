from pathlib import Path
import os
import yaml

def extract_Lark_grammar_from_yaml(only_new_lang=True):
  """Creates a lark file in ../grammars/ for  all yaml files located in ../content/keywords/.
  If a keyword is not yet translated, it will use the English translation of the keyword

  Args:
      only_new_lang (bool, optional): Specifies if only a lark file should be created for a new keyword language or for all languages. Defaults to True.
  """
  input_path = '../content/keywords/'
  current_grammar_path = '../grammars/'
  output_path = '../grammars-transformed/'
  Path(output_path).mkdir(parents=True, exist_ok=True)

  yaml_languages = [f.replace('.yaml', '') for f in os.listdir(input_path) if
                    os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]

  lark_languages = [f.replace('keywords-', '').replace('.lark', '') for f in os.listdir(current_grammar_path) if
                    os.path.isfile(os.path.join(current_grammar_path, f)) and f.startswith('keywords')]

  new_languages = [l for l in yaml_languages if not l in lark_languages]

  for yaml_lang in new_languages:
    yaml_filesname_with_path = os.path.join(input_path, yaml_lang + '.yaml')
    default_yaml_with_path = os.path.join(input_path, 'en' + '.yaml')

    with open(default_yaml_with_path, 'r', encoding='utf-8') as stream:
      en_command_combinations = yaml.safe_load(stream)

    with open(yaml_filesname_with_path, 'r', encoding='utf-8') as stream:
      command_combinations = yaml.safe_load(stream)

    lark_filesname_with_path = os.path.join(output_path, 'keywords-' + yaml_lang + '.lark')

    with open(lark_filesname_with_path, 'w+', encoding='utf-8') as f:
      list_of_translations = []
      
      for command, translation in command_combinations.items():   
        en_translation = en_command_combinations[command]
        
        if translation == '':
          translation = en_translation
          
        if yaml_lang != 'en':
          if translation in list_of_translations:
            print(f'Warning! {translation} is a duplicate translation. This is not desired when creating lark files')
          else:
            list_of_translations.append(translation)

        if type(command) != int:
          # numbers should be skipped (fh apr. 22 TODO: TBH I am not sure why they are even in the yaml?)

          lowercase_commands = ['random', 'left', 'right', 'black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow']
          # random, left and right and colors are tokens and need to be printed as they are
          # other rules need to be UPPERCASE and start with _
          if command not in lowercase_commands:
              command_upper = command.upper()
              command = '_' + command_upper

          # something to add to all lines to modify rules
          ending = "_SPACE?"
          if translation != en_translation:
              f.write(f'{command}: ("{translation}" | "{en_translation}") {ending}\n')
          else:
              f.write(f'{command}: "{translation}" {ending}\n')

extract_Lark_grammar_from_yaml(True)