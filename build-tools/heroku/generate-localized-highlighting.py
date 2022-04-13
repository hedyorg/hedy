#this script is used to generate localized syntax highlighting based on the keywords yaml

import os
import yaml

# Set the current directory to the root Hedy folder
os.chdir(os.path.join(os.path.dirname(__file__), '../..'))

language = 'id'

keywords_path = 'content/keywords/'
typescript_path = 'static/js/keywordTranslation'

keywords_file_path = os.path.join(keywords_path, f'{language}.yaml')
typescript_loc_file_path = os.path.join(typescript_path, f'syntaxLang-{language}.json')
typescript_template_file_path = os.path.join(typescript_path, f'syntaxLang-template.json')

with open(keywords_file_path, newline="", encoding='utf-8') as keywords_file:
    loc_keywords = yaml.safe_load(keywords_file)

with open(typescript_template_file_path, newline="", encoding='utf-8') as highlighting_template_file:
    highlighting_en = highlighting_template_file.readlines()

# copy the first line (docs)
highlighting_loc = []
highlighting_loc.append(highlighting_en[0])

# use the template for the other langs
for line in highlighting_en[1:-1]:
    line = line.format(**loc_keywords)
    highlighting_loc.append(line)

highlighting_loc.append('}')


with open(typescript_loc_file_path, newline="", encoding='utf-8', mode='w') as typescript_loc_file:
    typescript_loc_file.writelines(highlighting_loc)


