from definition import *

# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions

def rule_level1(keywordLang):
    return { "start" : [
            {
                "regex": '[ac]',
                "token": 'keyword',
                "next": 'StateB',
            },{
                "regex": '[bc]',
                "token": 'constant.character',
                "next": 'StateA',
            },{
                "regex": '[^abcd]',
                "token": 'comment',
                "next": 'start',
            }
        ], "StateA" : [
            {
                "regex": '[^cg]',
                "token": 'invalid',
                "next": 'StateA',
            },{
                "regex": 'c',
                "token": 'keyword',
                "next": 'StateA',
            },{
                "regex":"$",
                "token":"invalid",
                "next":"StateE"
            }
        ],"StateB" : [{
                "regex": '[^c]',
                "token": 'variable',
                "next": 'StateB',
            },{
                "regex":"$",
                "token":"invalid",
                "next":"StateE"
            }
        ],"StateE" : [{
                "regex":"e",
                "token":"variable",
                "next":"start",
            },{
                "regex":"Test",
                "token":"comment",
            }
        ]
    }

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
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["turn"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["sleep"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_LINE + keywordLang["forward"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_WORD + keywordLang["at"] + SPACE + keywordLang["random"] ,
        'token': 'keyword',
        'next': 'start',
    },{
        'regex': START_WORD + keywordLang["at"] ,
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
    } ]}

