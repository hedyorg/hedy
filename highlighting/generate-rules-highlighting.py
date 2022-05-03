import os
import re
import yaml
import json

# import rules from files
from rules_automaton import rule_level1, rule_level2, rule_level3
from rules_list import ruleALL

# destinations of files containing syntax highlighting rules
OUTPUT_PATH = "highlighting/highlightingRules/highlighting-{}.json"

# Files containing translations of keywords
KEYWORDS_PATH = 'content/keywords/'
KEYWORDS_PATTERN = '(\w+).yaml'


# Functions that collect all the rules, for all levels, of a given language
def generateRules(currentLang):
    return [
        { 'name': 'level1' , 'rules': rule_level1(currentLang) },
        { 'name': 'level2' , 'rules': rule_level2(currentLang) },
        { 'name': 'level3' , 'rules': rule_level3(currentLang) },
        { 'name': 'level4' , 'rules': ruleALL(currentLang, 4) },
        { 'name': 'level5' , 'rules': ruleALL(currentLang, 5) },
        { 'name': 'level6' , 'rules': ruleALL(currentLang, 6) },
        { 'name': 'level7' , 'rules': ruleALL(currentLang, 7) },
        { 'name': 'level8' , 'rules': ruleALL(currentLang, 8) },
        { 'name': 'level9' , 'rules': ruleALL(currentLang, 9) },
        { 'name': 'level10', 'rules': ruleALL(currentLang, 10) },
        { 'name': 'level11', 'rules': ruleALL(currentLang, 11) },
        { 'name': 'level12', 'rules': ruleALL(currentLang, 12) },
        { 'name': 'level13', 'rules': ruleALL(currentLang, 13) },
        { 'name': 'level14', 'rules': ruleALL(currentLang, 14) },
        { 'name': 'level15', 'rules': ruleALL(currentLang, 15) },
        { 'name': 'level16', 'rules': ruleALL(currentLang, 16) },
        { 'name': 'level17', 'rules': ruleALL(currentLang, 17) },
        { 'name': 'level18', 'rules': ruleALL(currentLang, 18) },
    ]

# Function to get the translations of the keywords
def get_Traduction(KEYWORDS_PATH, KEYWORDS_PATTERN):
    tmp = {}

    listLanguageFile = os.listdir(KEYWORDS_PATH)

    for languageFile in listLanguageFile:
        languageCode = re.search(KEYWORDS_PATTERN,languageFile).group(1)

        keywords_file = open(os.path.join(KEYWORDS_PATH, languageFile), newline="", encoding='utf-8')

        tmp[languageCode] = yaml.safe_load(keywords_file)

    Result = {}
    for languageCode in tmp:
        Result[languageCode] = {}
        for keyword in tmp[languageCode] :
            Result[languageCode][keyword] = "({}|{})".format(tmp[languageCode][keyword], tmp['en'][keyword])

    return Result

def validate_ruleset(LEVELS):
  """Confirm that the generated syntax highlighting rules are valid, throw an error if not."""
  errors = 0
  for level in LEVELS:
    for rulename, rules in level['rules'].items():
      for rule in rules:
        r = re.compile(rule['regex'])

        group_count = r.groups if r.groups > 0 else 1
        token_count = len(rule['token']) if isinstance(rule['token'], list) else 1

        if group_count != token_count:
          print(f'ERROR: In {level["name"]}, rule \'{rulename}\': regex \'{rule["regex"]}\' has {group_count} capturing subgroups, but \'token\' has {token_count} elements: {repr(rule["token"])}')
          errors += 1

  if errors > 0:
    raise RuntimeError(f'{errors} rules are invalid')


os.chdir(os.path.dirname(__file__) +"/..")

LanguageKeywords = get_Traduction(KEYWORDS_PATH,KEYWORDS_PATTERN)

for languageCode in LanguageKeywords:

    print("Generation of syntax highlighting rules for {:.<10}".format(languageCode), end="")

    # List of rules by level
    LEVELS = generateRules(LanguageKeywords[languageCode])
    validate_ruleset(LEVELS)

    # Saving the rules in the corresponding file
    fileLangSyntax = open(OUTPUT_PATH.format(languageCode),"w")
    fileLangSyntax.write(json.dumps(LEVELS,indent=4))
    fileLangSyntax.close()

    print(" Done !")

