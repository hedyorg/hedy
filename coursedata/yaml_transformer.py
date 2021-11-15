import os
import copy
import utils
import yaml

def nop(s):
  return s

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


          transformed_dict[new_level] = old_content
        del transformed_dict[old_level]
        file_transformed = True

    if file_transformed:  #only write updated files
      with open(output_path + yaml_filesname_without_path, 'w') as f:
        f.write(utils.dump_yaml_rt(transformed_dict))

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
            transformed_dict['adventures'][akey]['levels'][new_level] = transformed_dict['adventures'][akey]['levels'][old_level]
          del transformed_dict['adventures'][akey]['levels'][old_level]
          file_transformed = True

    if file_transformed: #only write updated files
      with open(output_path + yaml_filesname_without_path, 'w') as f:
        f.write(utils.dump_yaml_rt(transformed_dict))

def transform_levels_in_all_YAMLs(old_level, new_level=None, function=nop):
  # Set the current directory to the root Hedy folder
  os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))
  transform_level_defaults(old_level, new_level, function)
  # WARNING: adventure do not properly use the transformer function yet!
  # transform_adventures(old_level, new_level=None, function=nop)

def transform_yaml_to_lark(overwrite=False):
  """Creates a lark file in ./grammars/ for  all yaml files located in ./coursedata/keywords/.

  Args:
      overwrite (bool, optional): Specifies if the current lark files for keywords should be overwritten. Defaults to False.
  """
  input_path = './coursedata/keywords/'
  output_path = './grammars/'
  
  yaml_languages = [f.replace('.yaml', '') for f in os.listdir(input_path) if
                     os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]
  
  lark_languages = [f.replace('keywords-', '').replace('.lark', '') for f in os.listdir(output_path) if
                     os.path.isfile(os.path.join(output_path, f)) and f.startswith('keywords')]

  for yaml_lang in yaml_languages:
    if yaml_lang in lark_languages:
      if not overwrite:
        continue
    yaml_filesname_with_path = os.path.join(input_path, yaml_lang + '.yaml')
    
    with open(yaml_filesname_with_path, 'r') as stream:
      yaml_dict = yaml.safe_load(stream)
      
    command_combinations = yaml_dict['commands']
    lark_filesname_with_path = os.path.join(output_path, 'keywords-' + yaml_lang + '.lark')
    
    with open(lark_filesname_with_path, 'w') as f:
      for command_combo in command_combinations:
        command = list(command_combo.keys())[0]
        translation = command_combo[command]
        
        if command != "random":
            command_upper = command.upper()
            command = "_" + command_upper
        
        f.write(f'{command}: "{translation}" \n')

def remove_brackets(s):
  return s.replace('(', ' ').replace(')', '')

transform_yaml_to_lark(True)
# transform_levels_in_all_YAMLs("13-old", 14, remove_brackets)