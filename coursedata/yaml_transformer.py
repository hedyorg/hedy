# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'C:\hedy')

import hedy_translation

from pathlib import Path
import os
import copy
import utils
import yaml

def nop(s):
  return s


def transform_yaml_to_lark(only_new_lang=True):
  """Creates a lark file in ./grammars/ for  all yaml files located in ./coursedata/keywords/.
  If a keyword is not yet translated, it will use the English translation of the keyword

  Args:
      only_new_lang (bool, optional): Specifies if only a lark file should be created for a new language or for all languages. Defaults to True.
  """
  input_path = '../coursedata/keywords/'
  current_grammar_path = '../grammars/'
  output_path = '../grammars-transformed/'
  Path(output_path).mkdir(parents=True, exist_ok=True)

  yaml_languages = [f.replace('.yaml', '') for f in os.listdir(input_path) if
                    os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]

  lark_languages = [f.replace('keywords-', '').replace('.lark', '') for f in os.listdir(current_grammar_path) if
                    os.path.isfile(os.path.join(current_grammar_path, f)) and f.startswith('keywords')]

  for yaml_lang in yaml_languages:
    if yaml_lang in lark_languages:
      if only_new_lang:
        continue
    yaml_filesname_with_path = os.path.join(input_path, yaml_lang + '.yaml')
    default_yaml_with_path = os.path.join(input_path, 'en' + '.yaml')

    with open(default_yaml_with_path, 'r') as stream:
      default_command_combinations = yaml.safe_load(stream)

    with open(yaml_filesname_with_path, 'r') as stream:
      command_combinations = yaml.safe_load(stream)

    lark_filesname_with_path = os.path.join(output_path, 'keywords-' + yaml_lang + '.lark')

    with open(lark_filesname_with_path, 'w+') as f:
      list_of_translations = []
      
      for command, translation in command_combinations.items():      
        if translation == '':
          translation = default_command_combinations[command]
          
        if yaml_lang != 'en':
          if translation in list_of_translations:
            raise ValueError(f'{translation} is a duplicate translation. This is not desired when creating lark files')
          else:
            list_of_translations.append(translation)
        
        if command != 'random':
          command_upper = command.upper()
          command = '_' + command_upper

        f.write(f'{command}: "{translation}" \n')

def transform_level_defaults(old_level, new_level=None, function=nop):
  input_path = '../coursedata/level-defaults'
  output_path = '../coursedata/level-defaults-transformed/'
  yaml_filesnames = [f for f in os.listdir(input_path) if
                     os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]

  for yaml_filesname_without_path in yaml_filesnames:
    file_transformed = False
    yaml_filesname_with_path = os.path.join(input_path, yaml_filesname_without_path)

    yaml_dict = utils.load_yaml_rt(yaml_filesname_with_path)
    transformed_dict = copy.deepcopy(yaml_dict)
    for level in yaml_dict:
      if level == old_level:
        if new_level != None:
          old_content = transformed_dict[old_level]
          old_content['start_code'] = function(old_content['start_code'])

          # transfor code locations incl. demo_code and start_code
          for c in old_content['commands']:
            c['demo_code'] = function(c['demo_code'])

          transformed_dict[new_level] = copy.deepcopy(old_content)
        del transformed_dict[old_level]
        file_transformed = True

    if file_transformed:  #only write updated files
      sorted_dict = {}
      for key in sorted(transformed_dict):
        sorted_dict[key] = transformed_dict[key]

      with open(output_path + yaml_filesname_without_path, 'w') as f:
        f.write(utils.dump_yaml_rt(sorted_dict))

def transform_adventures(old_level, new_level=None, function=nop):
  input_path = '../coursedata/adventures'
  output_path = '../coursedata/adventures-transformed/'
  yaml_filesnames = [f for f in os.listdir(input_path) if
                     os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]

  for yaml_filesname_without_path in yaml_filesnames:
    file_transformed = False
    yaml_filesname_with_path = os.path.join(input_path, yaml_filesname_without_path)

    yaml_dict = utils.load_yaml_rt(yaml_filesname_with_path)
    transformed_dict = copy.deepcopy(yaml_dict)

    for akey, adventure in yaml_dict['adventures'].items():
      for level in adventure['levels']:
        if level == old_level:
          if new_level != None:
            transformed_dict['adventures'][akey]['levels'][new_level] = copy.deepcopy(transformed_dict['adventures'][akey]['levels'][old_level])
          # del transformed_dict['adventures'][akey]['levels'][old_level]
          file_transformed = True

    if file_transformed: #only write updated files
      with open(output_path + yaml_filesname_without_path, 'w') as f:
        f.write(utils.dump_yaml_rt(transformed_dict))

def transform_levels_in_all_YAMLs(old_level, new_level=None, function=nop):
  # Set the current directory to the root Hedy folder
  os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))
  transform_level_defaults(old_level, new_level, function)
  # WARNING: adventure do not properly use the transformer function yet!
  # transform_adventures(old_level, new_level, function=nop)


def remove_brackets(s):
  return s.replace('(', ' ').replace(')', '')

# transform_yaml_to_lark(False)
# transform_levels_in_all_YAMLs('colon', 17)

def translate_story_text(level, story_text, from_lang, to_lang)
  story_text_list = story_text.splitlines()
  transformed_story_text = []
  translating = False
  translate_list = []
  
  for line in story_text_list:
    line_list = line.split()
        
    for index, word in enumerate(line_list):
      if word.startswith('`') and word.endswith('`'):
        translated_word = word 
        transformed_story_text.append(translated_word)
      
      if word == '```':
        if not translating:
          translating = True
        else:
          text_to_be_translated = ''.join(translate_list)
          translated_text = hedy_translation.translate_keywords(text_to_be_translated)
          translating = False
      
      if translating: 
        if index != len(line_list):
          translate_list.append(word + ' ')
      else:
        if index != len(line_list):
          transformed_story_text.append(word + ' ')
    
    if translating:
      translate_list.append('\n')
      
    transformed_story_text.append('\n')  
  
  
  print(''.join(transformed_story_text))    


def transform_yaml_keywords(lang = 'all'):
  input_path = './coursedata/adventures'
  output_path = './coursedata/adventures-transformed/'
  Path(output_path).mkdir(parents=True, exist_ok=True)

  yaml_filesnames = [f for f in os.listdir(input_path) if
                     os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]

  for filename in yaml_filesnames:
    if filename == lang + '.yaml' or lang == 'all':      
      yaml_filesnames_with_path = os.path.join(input_path, filename)

      with open(yaml_filesnames_with_path, 'r') as stream:
        yaml_dict = yaml.safe_load(stream)

      for adventure, adventure_values in yaml_dict['adventures'].items():
        levels = adventure_values['levels']
        for level_number, level_value in levels.items():
          story_text = level_value['story_text']
          start_code = level_value['start_code']
          if level_number == 1 and adventure == 'story':
            translate_story_text(level_number, story_text, 'en', filename)
          # translate_start_code(level_number, start_code)
                  
transform_yaml_keywords('en')

  # def translate_start_code(level, story_text):