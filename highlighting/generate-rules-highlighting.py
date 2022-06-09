import os
import re
import yaml
import json

# import rules from files
from rules_automaton import rule_level1, rule_level2, rule_level3
from rules_list import rule_all
from definition import TRANSLATE_WORD

# destinations of files containing syntax highlighting rules
OUTPUT_PATH_HIGHLIGHT  = "highlighting/highlighting.json"
OUTPUT_PATH_TRANSLATION = "highlighting/highlighting-trad.json"

# Files containing translations of keywords
KEYWORDS_PATH = 'content/keywords/'
KEYWORDS_PATTERN = '(\w+).yaml'

# Functions that collect all the rules, for all levels, of a given language
def generate_rules():
    return [
        { 'name': 'level1' , 'rules': rule_level1() },
        { 'name': 'level2' , 'rules': rule_level2() },
        { 'name': 'level3' , 'rules': rule_level3() },
        { 'name': 'level4' , 'rules': rule_all(4) },
        { 'name': 'level5' , 'rules': rule_all(5) },
        { 'name': 'level6' , 'rules': rule_all(6) },
        { 'name': 'level7' , 'rules': rule_all(7) },
        { 'name': 'level8' , 'rules': rule_all(8) },
        { 'name': 'level9' , 'rules': rule_all(9) },
        { 'name': 'level10', 'rules': rule_all(10) },
        { 'name': 'level11', 'rules': rule_all(11) },
        { 'name': 'level12', 'rules': rule_all(12) },
        { 'name': 'level13', 'rules': rule_all(13) },
        { 'name': 'level14', 'rules': rule_all(14) },
        { 'name': 'level15', 'rules': rule_all(15) },
        { 'name': 'level16', 'rules': rule_all(16) },
        { 'name': 'level17', 'rules': rule_all(17) },
        { 'name': 'level18', 'rules': rule_all(18) },
    ]


def validate_ruleset(levels):
  """Confirm that the generated syntax highlighting rules are valid, throw an error if not."""
  errors = 0
  for level in levels:
    for state, rules in level['rules'].items():
      for rule in rules:
        r = re.compile(rule['regex'])

        if r.groups == 0:
            if type(rule["token"]) != str:
                raise ValueError(f"In {level['name']}, state \'{state}\': if regex has no groups, token must be a string. In this rule.\n{rule}")
                errors += 1

        else:
            if type(rule["token"]) != list :
                raise ValueError(f"In {level['name']}, state \'{state}\': if regex has groups, token must be a list. In this rule.\n{rule}")
                errors += 1

            else:
                if r.groups != len(rule["token"]):
                    raise ValueError(f"In {level['name']}, state \'{state}\': number of groups in the regex is different from the number of tokens. In this rule.\n{rule}")
                    errors += 1


  if errors > 0:
    raise RuntimeError(f'{errors} rules are invalid')





# Function to get the translations of the keywords
def get_translations(KEYWORDS_PATH, KEYWORDS_PATTERN):
    tmp = {}

    digits = {}

    list_language_file = os.listdir(KEYWORDS_PATH)

    for language_file in list_language_file:
        language_code = re.search(KEYWORDS_PATTERN,language_file).group(1)

        keywords_file = open(os.path.join(KEYWORDS_PATH, language_file), newline="", encoding='utf-8')

        yaml_file = yaml.safe_load(keywords_file)
        tmp[language_code] = {}
        digits[language_code] = []
        for k in yaml_file:
            if str(k) in TRANSLATE_WORD:
                tmp[language_code][str(k)] = str(yaml_file[k])
            elif str(k) in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                digits[language_code].append(str(yaml_file[k]))


    result = {}
    for language_code in sorted(tmp.keys()):
        result[language_code] = {}
        if language_code == "en":
           for keyword in sorted(tmp[language_code].keys()) :
               result[language_code][keyword] = "{}".format(tmp['en'][keyword])
        else:
           for keyword in sorted(tmp[language_code].keys()) :
                word = tmp[language_code][keyword]
                if word != tmp['en'][keyword] :

                    # special case for arabic 'underscore'
                    if language_code == "ar":
                        ch = "\u0640*"
                        word = ch + ch.join(list(word)) + ch


                    result[language_code][keyword] = "{}|{}".format(word, tmp['en'][keyword])
                else:
                    result[language_code][keyword] = "{}".format(tmp['en'][keyword])

    # add digits
    for language_code in sorted(tmp.keys()):
        result[language_code]["DIGIT"] = []
        for d in digits["en"]:
            if d not in result[language_code]["DIGIT"]:
                result[language_code]["DIGIT"].append(d)
        
        for d in digits[language_code]:
            if d not in result[language_code]["DIGIT"]:
                result[language_code]["DIGIT"].append(d)

        result[language_code]["DIGIT"] = "".join(result[language_code]["DIGIT"])

    return result



os.chdir(os.path.dirname(__file__) +"/..")



print("Generation of translations.....................", end="")
language_keywords = get_translations(KEYWORDS_PATH, KEYWORDS_PATTERN)
# Saving the rules in the corresponding file
file_lang = open(OUTPUT_PATH_TRANSLATION, "w")
file_lang.write(json.dumps(language_keywords, indent=4))
file_lang.close()
print(" Done !")



print("Generation of syntax highlighting rules........", end="")

# List of rules by level
levels = generate_rules()

validate_ruleset(levels)

# Saving the rules in the corresponding file
file_syntax = open(OUTPUT_PATH_HIGHLIGHT,"w")
file_syntax.write(json.dumps(levels,indent=4))
file_syntax.close()

print(" Done !")

