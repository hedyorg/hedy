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
            Result[languageCode][keyword] = "{}|{}".format(tmp[languageCode][keyword], tmp['en'][keyword])

    return Result



os.chdir(os.path.dirname(__file__) +"/..")

LanguageKeywords = get_Traduction(KEYWORDS_PATH,KEYWORDS_PATTERN)

for languageCode in LanguageKeywords:

    print("Generations of syntax highlighting rules for {:.<10}".format(languageCode), end="")

    # List of rules by level
    LEVELS = generateRules(LanguageKeywords[languageCode])

    # Saving the rules in the corresponding file
    fileLangSyntax = open(OUTPUT_PATH.format(languageCode),"w")
    fileLangSyntax.write(json.dumps(LEVELS,indent=4))
    fileLangSyntax.close()

    print(" Done !")

