import os
import re
import yaml
import json

# import rules from files
from rules_automaton import rule_level1, rule_level2, rule_level3
from rules_list import ruleALL
from definition import TRANSLATE_WORD

# destinations of files containing syntax highlighting rules
OUTPUT_PATH_HIGHLIGHT  = "highlighting/highlighting.json"
OUTPUT_PATH_TRADUCTION = "highlighting/highlighting-trad.json"

# Files containing translations of keywords
KEYWORDS_PATH = 'content/keywords/'
KEYWORDS_PATTERN = '(\w+).yaml'

# Functions that collect all the rules, for all levels, of a given language
def generateRules():
    return {
        'level1' : rule_level1(),
        'level2' : rule_level2(),
        'level3' : rule_level3(),
        'level4' : ruleALL(4),
        'level5' : ruleALL(5),
        'level6' : ruleALL(6),
        'level7' : ruleALL(7),
        'level8' : ruleALL(8),
        'level9' : ruleALL(9),
        'level10': ruleALL(10),
        'level11': ruleALL(11),
        'level12': ruleALL(12),
        'level13': ruleALL(13),
        'level14': ruleALL(14),
        'level15': ruleALL(15),
        'level16': ruleALL(16),
        'level17': ruleALL(17),
        'level18': ruleALL(18),
    }


def validate_ruleset(LEVELS):
    """Confirm that the generated syntax highlighting rules are valid, throw an error if not."""
    errors = 0
    for rulesByLevel in LEVELS.values():
        for rulesByState in rulesByLevel.values():
            for rule in rulesByState:
                r = re.compile(rule['regex'])
                group_count = r.groups if r.groups > 0 else 1
                token_count = len(rule['token']) if isinstance(rule['token'], list) else 1

                if group_count != token_count:
                    print(f'ERROR: In {level["name"]}, rule \'{rulename}\': regex \'{rule["regex"]}\' has {group_count} capturing subgroups, but \'token\' has {token_count} elements: {repr(rule["token"])}')
                    errors += 1
  
    if errors > 0:
        raise RuntimeError(f'{errors} rules are invalid')





# Function to get the translations of the keywords
def get_Traduction(KEYWORDS_PATH, KEYWORDS_PATTERN):
    tmp = {}

    listLanguageFile = os.listdir(KEYWORDS_PATH)

    for languageFile in listLanguageFile:
        languageCode = re.search(KEYWORDS_PATTERN,languageFile).group(1)

        keywords_file = open(os.path.join(KEYWORDS_PATH, languageFile), newline="", encoding='utf-8')

        yamlFile = yaml.safe_load(keywords_file)
        tmp[languageCode] = {}
        for k in yamlFile:
            if k in TRANSLATE_WORD:
                tmp[languageCode][k] = str(yamlFile[k])

    Result = {}
    for languageCode in tmp:
        Result[languageCode] = {}
        if languageCode == "en":
           for keyword in tmp[languageCode] :
               Result[languageCode][keyword] = "({})".format(tmp['en'][keyword])
        else:
           for keyword in tmp[languageCode] :
                if tmp[languageCode][keyword] != tmp['en'][keyword] :
                    Result[languageCode][keyword] = "({}|{})".format(tmp[languageCode][keyword], tmp['en'][keyword])
                else:
                    Result[languageCode][keyword] = "({})".format(tmp[languageCode][keyword])


    return Result



os.chdir(os.path.dirname(__file__) +"/..")



print("Generation of traductions.....................", end="")
LanguageKeywords = get_Traduction(KEYWORDS_PATH,KEYWORDS_PATTERN)
# Saving the rules in the corresponding file
fileLang = open(OUTPUT_PATH_TRADUCTION,"w")
fileLang.write(json.dumps(LanguageKeywords,indent=4))
fileLang.close()
print(" Done !")



print("Generation of syntax highlighting rules.......", end="")

# List of rules by level
LEVELS = generateRules()

validate_ruleset(LEVELS)

# Saving the rules in the corresponding file
fileSyntax = open(OUTPUT_PATH_HIGHLIGHT,"w")
fileSyntax.write(json.dumps(LEVELS,indent=4))
fileSyntax.close()

print(" Done !")

