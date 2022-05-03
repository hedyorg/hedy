from definition import *

# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions


def rule_level1(keywordLang):
    return {"start" : [{
        'regex': START_LINE + keywordLang["ask"] + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["print"] + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["echo"] + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["color"] + END_WORD + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    }, {
        'regex': START_LINE + keywordLang["color"] + SPACE + WORD + "( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["forward"] + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["turn"] + "( *)" + keywordLang["left"] + "( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["turn"] + "( *)" + keywordLang["right"] + "( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["turn"] + "(.*)$",
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
    } ]}


def rule_level2(keywordLang) :
    return {"start" : [{
        'regex': START_LINE + WORD + SPACE + keywordLang["is"] + "( *)" + keywordLang["ask"] + "(.*)$",
        'token': ["text",'text','text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + WORD + SPACE + keywordLang["is"] + "( *)(.*)$",
        'token': ["text",'text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["print"] + "(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["sleep"] + "(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["turn"] + "(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["forward"] + "(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': '#(.*)$',
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
    } ]}

def rule_level3(keywordLang):
    return {"start" : [{
        'regex': START_LINE + WORD + SPACE + keywordLang["is"] + "( *)" + keywordLang["ask"] + "(.*)$",
        'token': ["text",'text','text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + WORD + SPACE + keywordLang["is"] + "( *)(.*)$",
        'token': ["text",'text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["remove"] + "( *)(.*)" + SPACE + keywordLang["from"] + "( *)"+ WORD +"$",
        'token': ["text",'keyword','text','text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["add"] + "( *)(.*)" + SPACE + keywordLang["to_list"] + "( *)"+ WORD +"$",
        'token': ["text",'keyword','text','text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["print"] ,
        'token': ['text','keyword'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["turn"] ,
        'token': ['text','keyword'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["sleep"] ,
        'token': ['text','keyword'],
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["forward"] ,
        'token': ['text','keyword'],
        'next': 'start',
    },{
        'regex': START_WORD + keywordLang["at"] + SPACE + keywordLang["random"] ,
        'token': ['text','keyword','keyword','keyword'],
        'next': 'start',
    },{
        'regex': START_WORD + keywordLang["at"] ,
        'token': ['text','keyword'],
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
    } ]}

