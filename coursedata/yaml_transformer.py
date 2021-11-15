import os
import copy
import utils

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
  # transform_level_defaults(old_level, new_level, function)
  # WARNING: adventure do not properly use the transformer function yet!
  transform_adventures(old_level, new_level, function=nop)


def remove_brackets(s):
  return s.replace('(', ' ').replace(')', '')

transform_levels_in_all_YAMLs(12, 13)