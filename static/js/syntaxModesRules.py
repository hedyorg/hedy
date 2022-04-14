
# extension of \w
# A-z is different from A-Za-z (see an ascii table)
CHARACTER = '0-9_A-Za-zÀ-ÿء-ي' 
WORD      = '[' + CHARACTER + "]+"
SPACE     = " +"

START_LINE = '(^ *)'
START_WORD = '(^| )'
END_WORD   = '(?![' + CHARACTER + '])'


# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions

def rule_level1(keywordLang):
    return [{
        'regex': START_LINE + "(" + keywordLang["ASK"] + ")(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["PRINT"] + ")(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["ECHO"] + ")(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["COLOR"] + ")(" + END_WORD + ")(.*)$",
        'token': ['text','keyword','text','text'],
        'next': 'start',
    }, {
        'regex': START_LINE + "(" + keywordLang["COLOR"] + ")(" + SPACE + ")(" + WORD + ")( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["FORWARD"] + ")(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["TURN"] + ")( *)(" + keywordLang["LEFT"] + ")( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["TURN"] + ")( *)(" + keywordLang["RIGHT"] + ")( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["TURN"] + ")(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': '#.*$',
        'token': 'comment',
        'next': 'start',
    },{
        'regex': '_\\?_',
        'token': 'invalid',
        'next': 'start',
    },{
        'regex': '(^| )(_)(?= |$)',
        'token': ['text','invalid'],
        'next': 'start',
    } ]

def rule_level2(keywordLang) :
    return [{
        'regex': START_LINE + "("+WORD+ ")(" + SPACE + ")(" + keywordLang["IS"] + ")( *)(" + keywordLang["ASK"] + ")(.*)$",
        'token': ["text",'text','text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "("+WORD+ ")(" + SPACE + ")(" + keywordLang["IS"] + ")( *)(.*)$",
        'token': ["text",'text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["PRINT"] + ")(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["SLEEP"] + ")(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["TURN"] + ")(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["FORWARD"] + ")(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': '#.*$',
        'token': 'comment',
        'next': 'start',
    },{
        'regex': '_\\?_',
        'token': 'invalid',
        'next': 'start',
    },{
        'regex': '(^| )(_)(?= |$)',
        'token': ['text','invalid'],
        'next': 'start',
    } ]

def rule_level3(keywordLang):
    return [{
        'regex': START_LINE + "("+WORD+ ")(" + SPACE + ")(" + keywordLang["IS"] + ")( *)(" + keywordLang["ASK"] + ")(.*)$",
        'token': ["text",'text','text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "("+WORD+ ")(" + SPACE + ")(" + keywordLang["IS"] + ")( *)(.*)$",
        'token': ["text",'text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["REMOVE"] + ")( *)(.*)(" + SPACE + ")(" + keywordLang["FROM"] + ")( *)("+ WORD +")$",
        'token': ["text",'keyword','text','text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + "(" + keywordLang["ADD_LIST"] + ")( *)(.*)(" + SPACE + ")(" + keywordLang["TO_LIST"] + ")( *)("+ WORD +")$",
        'token': ["text",'keyword','text','text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["PRINT"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["TURN"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["SLEEP"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["FORWARD"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_WORD + keywordLang["AT"] + SPACE + keywordLang["RANDOM"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_WORD + keywordLang["AT"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': '#.*$',
        'token': 'comment',
        'next': 'start',
    },{
        'regex': '_\\?_',
        'token': 'invalid',
        'next': 'start',
    },{
        'regex': '(^| )(_)(?= |$)',
        'token': ['text','invalid'],
        'next': 'start',
    } ]


# transform "IF" in current language "if", "si", etc...
def translate(keywordLang, keywordsLevel):
    if type(keywordsLevel) == str:
        if keywordsLevel in keywordLang:
            return keywordLang[keywordsLevel]
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


# In the following levels,
# so what is not in quotes is code,
# and any keyword in the code can be colored independently
# of what is around it, so we use a general function

def ruleALL(keywordLang, keywordsLevel, number = False, with_decimal = False ):

    # generation of keyword by level
    keywordLangByLevel = translate(keywordLang,keywordsLevel)

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
    if (number) :
        if (with_decimal) :
            numberRegex = START_WORD + '[0-9]*\\.?[0-9]+' + END_WORD
        else:
            numberRegex = START_WORD + '[0-9]+' + END_WORD

        list_rules.append({'regex':numberRegex, 'token': 'variable', 'next':'start'} )

        # Special case of an number directly followed by a number 
        for command in keywordLangByLevel["SP_K"]: 
            list_rules.append({
                'regex': START_WORD + "("+ command + ')([0-9]+)' + END_WORD,
                'token': ['text','keyword','variable'],
                'next': 'start',
            })

        for command in keywordLangByLevel["K"]:
            list_rules.append({
                'regex': "(" + command + ')([0-9]+)' + END_WORD,
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

    return list_rules


# This variable lists all the keywords in each level, i.e. everything that should be displayed in red (of type `keyword`)
# 
# There are several categories of keywords: 
# - SP_K_SP
#   These are the keywords that must be "alone" so neither preceded nor followed directly by a word 
# 
# - K
#   These are the keywords that are independent of the context (formerly the symbols).
#   In particular, even if they are between 2 words, the syntax highlighting will select them
# 
# - SP_K
#   This category of keywords allows you to have keywords that are not preceded
#   by another word, but that can be followed immediately by another word. (see the PR #2413)
# 
# - K_SP
#   This category of keywords allows you to have keywords that can be preceded immediately
#   by another word, but that are not followed by another word.
KEYWORDS = {
    4 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM"],
        "K"       : [","],
        "SP_K"    : ["PRINT","ASK","SLEEP","FORWARD","TURN","RANDOM"],
        "K_SP"    : [],
    },
    5 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","ELSE"],
        "K"       : [","],
        "SP_K"    : ["PRINT","ASK","SLEEP","FORWARD","TURN","RANDOM"],
        "K_SP"    : [],
    },
    6 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","ELSE"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["PRINT","ASK","SLEEP","FORWARD","TURN","RANDOM"],
        "K_SP"    : [],
    },
    7 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","ELSE","REPEAT","TIMES"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["PRINT","ASK","SLEEP","FORWARD","TURN","RANDOM"],
        "K_SP"    : [],
    },
    8 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","REPEAT"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["PRINT","ASK","SLEEP","FORWARD","TURN","RANDOM","ELSE","TIMES"],
        "K_SP"    : [],
    },
    9 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","REPEAT"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["PRINT","ASK","SLEEP","FORWARD","TURN","RANDOM","ELSE","TIMES"],
        "K_SP"    : [],
    },
    10 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","REPEAT","FOR"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["PRINT","ASK","SLEEP","FORWARD","TURN","RANDOM","ELSE","TIMES"],
        "K_SP"    : [],
    },
    11 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","FOR","RANGE","TO"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["PRINT","ASK","SLEEP","RANDOM","ELSE"],
        "K_SP"    : [],
    },
    12 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","FOR","RANGE","TO"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["PRINT","ASK","SLEEP","RANDOM","ELSE"],
        "K_SP"    : [],
    },
    13 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","FOR","RANGE","TO","AND","OR"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["PRINT","ASK","SLEEP","RANDOM","ELSE"],
        "K_SP"    : [],
    },
    14 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","FOR","RANGE","TO","AND","OR","ELSE"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!"],
        "SP_K"    : ["PRINT","ASK","SLEEP","RANDOM"],
        "K_SP"    : [],
    },
    15 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","FOR","RANGE","TO","AND","OR","WHILE"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!"],
        "SP_K"    : ["PRINT","ASK","SLEEP","RANDOM","ELSE"],
        "K_SP"    : [],
    },
    16 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","ELSE","FOR","RANGE","TO","AND","OR","WHILE"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]"],
        "SP_K"    : ["PRINT","ASK","SLEEP","RANDOM"],
        "K_SP"    : [],
    },
    17 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","ELSE","FOR","RANGE","TO","AND","OR","WHILE"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]",":"],
        "SP_K"    : ["PRINT","ASK","SLEEP","RANDOM"],
        "K_SP"    : ["ELIF"],
    },
    18 :{
        "SP_K_SP" : ["IS","AT","ADD_LIST","TO_LIST","REMOVE","FROM","IN","IF","ELSE","FOR","RANGE","TO","AND","OR","WHILE","INPUT"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]",":","\\(","\\)"],
        "SP_K"    : ["PRINT","SLEEP","RANDOM"],
        "K_SP"    : ["ELIF"],
    },
}


def generateRules(currentLang,KEYWORDS):
    return [
        { 'name': 'level1' , 'rules': {"start" : rule_level1(currentLang) },},
        { 'name': 'level2' , 'rules': {"start" : rule_level2(currentLang) },},
        { 'name': 'level3' , 'rules': {"start" : rule_level3(currentLang) },},
        { 'name': 'level4' , 'rules': {"start" : ruleALL(currentLang, KEYWORDS[4] ) },},
        { 'name': 'level5' , 'rules': {"start" : ruleALL(currentLang, KEYWORDS[5] ) },},
        { 'name': 'level6' , 'rules': {"start" : ruleALL(currentLang, KEYWORDS[6] , True) },},
        { 'name': 'level7' , 'rules': {"start" : ruleALL(currentLang, KEYWORDS[7] , True) },},
        { 'name': 'level8' , 'rules': {"start" : ruleALL(currentLang, KEYWORDS[8] , True) },},
        { 'name': 'level9' , 'rules': {"start" : ruleALL(currentLang, KEYWORDS[9] , True) },},
        { 'name': 'level10', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[10] , True) },},
        { 'name': 'level11', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[11] , True) },},
        { 'name': 'level12', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[12] , True, True) },},
        { 'name': 'level13', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[13] , True, True) },},
        { 'name': 'level14', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[14] , True, True) },},
        { 'name': 'level15', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[15] , True, True) },},
        { 'name': 'level16', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[16] , True, True) },},
        { 'name': 'level17', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[17] , True, True) },},
        { 'name': 'level18', 'rules': {"start" : ruleALL(currentLang, KEYWORDS[18] , True, True) },},
    ]










import os


di = os.path.dirname(__file__)
if di == "" : di = "."
listLanguageFile = os.listdir(di + "/keywordTranslation")
if "syntaxLang-template.json" in listLanguageFile:
    del listLanguageFile[listLanguageFile.index("syntaxLang-template.json")]

import re
import json

for languageFile in listLanguageFile:

    langageCode = re.search("syntaxLang-(\w+).json",languageFile).group(1)
    print("Generations of syntax coloring rules for {:.<8}".format(langageCode), end="")

    fileLang = open(di + "/keywordTranslation/" + languageFile,"r")
    currentLang = json.load(fileLang)
    fileLang.close()

    # List of rules by level
    LEVELS = generateRules(currentLang,KEYWORDS)

    namefileLangSyntax = di + "/syntax/highlighting-{}.json".format(langageCode)

    fileLangSyntax = open(namefileLangSyntax,"w")
    fileLangSyntax.write(json.dumps(LEVELS,indent=4))
    fileLangSyntax.close()

    print("Done !")

