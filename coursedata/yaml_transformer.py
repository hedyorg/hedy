import os
import copy
import utils

def transform_level_defaults(transformations):
  input_path = '../coursedata/level-defaults'
  output_path = '../coursedata/level-defaults-transformed/'
  yaml_filesnames = [f for f in os.listdir(input_path) if
                     os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]
  for yaml_filesname_without_path in yaml_filesnames:

    yaml_filesname_with_path = os.path.join(input_path, yaml_filesname_without_path)

    yaml_dict = utils.load_yaml_rt(yaml_filesname_with_path)
    transformed_dict = copy.deepcopy(yaml_dict)
    for level in yaml_dict:
      for old_level, new_level in transformations:
        if level == old_level:
          transformed_dict[new_level] = transformed_dict[old_level]
          del transformed_dict[old_level]

    with open(output_path + yaml_filesname_without_path, 'w') as f:
      f.write(utils.dump_yaml_rt(transformed_dict))

def transform_adventures(transformations):
  input_path = '../coursedata/adventures'
  output_path = '../coursedata/adventures-transformed/'
  yaml_filesnames = [f for f in os.listdir(input_path) if
                     os.path.isfile(os.path.join(input_path, f)) and f.endswith('.yaml')]

  for yaml_filesname_without_path in yaml_filesnames:
    yaml_filesname_with_path = os.path.join(input_path, yaml_filesname_without_path)

    yaml_dict = utils.load_yaml_rt(yaml_filesname_with_path)
    transformed_dict = copy.deepcopy(yaml_dict)

    for akey, adventure in yaml_dict['adventures'].items():
      for level in adventure['levels']:
        for old_level, new_level in transformations:
          if level == old_level:
            transformed_dict['adventures'][akey]['levels'][new_level] = transformed_dict['adventures'][akey]['levels'][old_level]
            del transformed_dict['adventures'][akey]['levels'][old_level]

    with open(output_path + yaml_filesname_without_path, 'w') as f:
      f.write(utils.dump_yaml_rt(transformed_dict))

def transform_levels_in_all_YAMLs(transformations):
  # Set the current directory to the root Hedy folder
  os.chdir(os.path.join(os.getcwd(), __file__.replace(os.path.basename(__file__), '')))
  transform_level_defaults(transformations)
  # transform_adventures(transformations)





tranformations = [(17, 12)]
transform_levels_in_all_YAMLs(tranformations)