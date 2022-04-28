from list_keywords import KEYWORDS, NUMBERS
from definition import *


# transform "IF" in current language "if", "si", etc...
def translate(keywordLang, keywordsLevel):
    if type(keywordsLevel) == str:
        if keywordsLevel in keywordLang:
            if "(" != keywordLang[keywordsLevel][0] and ")" != keywordLang[keywordsLevel][-1]:
                return "(" + keywordLang[keywordsLevel] + ")"
            else:
                return keywordLang[keywordsLevel]
        else:
            if "(" != keywordsLevel[0] and ")" != keywordsLevel[-1]:
                return "(" + keywordsLevel + ")"
            else:
                return keywordsLevel

    elif type(keywordsLevel) == list :
        L = []
        for sub in keywordsLevel:
            L.append(translate(keywordLang,sub))
        return L
    elif type(keywordsLevel) == dict:
        D = {}
        for key in keywordsLevel.keys():
            D[key] = translate(keywordLang,keywordsLevel[key])
        return D





# After the level 4
# so what is not in quotes is code,
# and any keyword in the code can be colored independently
# of what is around it, so we use a general function
# This general function uses 2 constants KEYWORDS and NUMBERS

def ruleALL(keywordLang, level):


    # generation of keyword by level
    keywordLangByLevel = translate(keywordLang,KEYWORDS[level])

    list_rules = []

    # Rule for comments :
    list_rules.append( { 'regex': '#.*$', 'token': 'comment', 'next': 'start' } )

    # Rule for quoted string :
    list_rules.append( { 'regex': '\"[^\"]*\"', 'token': 'constant.character', 'next': 'start' } )

    list_rules.append( { 'regex': "\'[^\']*\'", 'token': 'constant.character', 'next': 'start' } )

    # Rule for blanks marks :
    list_rules.append( { 'regex': '_\\?_', 'token': 'invalid', 'next': 'start' })
    list_rules.append( { 'regex': '(^| )(_)(?= |$)', 'token': ['text','invalid'], 'next': 'start' } )


    # Rules for numbers
    if (NUMBERS[level]["number"]) :
        if (NUMBERS[level]["number_with_decimal"]) :
            numberRegex = '([0-9]*\\.?[0-9]+)'
        else:
            numberRegex = '([0-9]+)'

        list_rules.append({'regex': START_WORD + numberRegex + END_WORD, 'token': 'variable', 'next':'start'} )

        # Special case of an number directly followed by a number 
        for command in keywordLangByLevel["SP_K"]: 
            list_rules.append({
                'regex': START_WORD + command + numberRegex + END_WORD,
                'token': ['text','keyword','variable'],
                'next': 'start',
            })

        for command in keywordLangByLevel["K"]:
            list_rules.append({
                'regex': command + numberRegex + END_WORD,
                'token': ['keyword','variable'],
                'next': 'start',
            })


    # Rules for commands of SP_K_SP 
    # These are the keywords that must be "alone" so neither preceded nor followed directly by a word 
    for command in keywordLangByLevel["SP_K_SP"]:
        list_rules.append({
            'regex': START_WORD + command + END_WORD,
            'token': "keyword",
            'next': "start", 
        })
    

    # Rules for commands of K 
    #  These are the keywords that are independent of the context (formerly the symbols
    # In particular, even if they are between 2 words, the syntax highlighting will select them
    for command in keywordLangByLevel["K"]:
        list_rules.append({
            'regex': command,
            'token': "keyword",
            'next': "start", 
        })

    # Rules for commands of SP_K 
    #  This category of keywords allows you to have keywords that are not preced
    # by another word, but that can be followed immediately by another word. (see the PR #2413)*/
    for command in keywordLangByLevel["SP_K"]:
        list_rules.append({
            'regex': START_WORD + command,
            'token': "keyword",
            'next': "start", 
        })

    # Rules for commands of K_SP 
    #  This category of keywords allows you to have keywords that can be preceded immediate
    # by another word, but that are not followed by another word.*/
    for command in keywordLangByLevel["K_SP"]:
        list_rules.append({
            'regex': command + END_WORD,
            'token': "keyword",
            'next': "start", 
        })

    return {"start" :list_rules}

