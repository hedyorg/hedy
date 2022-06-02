from definition import *

# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions

def rule_level1_old():
    return {"start" : [{
        'regex': START_LINE + K("ask") + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("print") + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("echo") + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("color") + END_WORD + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    }, {
        'regex': START_LINE + K("color") + SPACE + WORD + "( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("forward") + "(.*)$",
        'token': ['text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("turn") + "( *)" + K("left") + "( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("turn") + "( *)" + K("right") + "( *)$",
        'token': ['text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("turn") + "(.*)$",
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

def rule_level1():
    return {
    "start" : [{
        'regex': "#.*$",
        'token': "comment",
        'next': 'start',
    },{
        'regex': START_LINE + K("print"),
        'token': ["text",'keyword'],
        'next': 'string',
    },{
        'regex': START_LINE + K("ask"),
        'token': ["text",'keyword'],
        'next': 'string',
    },{
        'regex': START_LINE + K("echo"),
        'token': ["text",'keyword'],
        'next': 'string',
    },{
        'regex': START_LINE + K("forward"),
        'token': ["text",'keyword'],
        'next': 'string',
    },{
        'regex': START_LINE + K("turn"),
        'token': ["text",'keyword'],
        'next': 'angle',
    },{
        'regex': START_LINE + K("color"),
        'token': ["text",'keyword'],
        'next': 'color',
    }],
    "string" : [{
        'regex': "$",
        'token': ["text"],
        'next': 'start',
    },{
        'regex': "#.*$",
        'token': "comment",
        'next': 'start',
    }],
    "color" : [{
        'regex': "$",
        'token': ["text"],
        'next': 'start',
    },{
        'regex': K("purple"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("red"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("black"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("blue"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("brown"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("gray"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("green"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("orange"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("pink"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("white"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("yellow"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': "#.*$",
        'token': "comment",
        'next': 'start',
    }],
    "angle" : [{
        'regex': "$",
        'token': ["text"],
        'next': 'start',
    },{
        'regex': K("right"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': K("left"),
        'token': ["keyword"],
        'next': 'start',
    },{
        'regex': "#.*$",
        'token': "comment",
        'next': 'start',
    }]}


def rule_level2() :
    return {"start" : [{
        'regex': START_LINE + WORD + SPACE + K("is") + "( *)" + K("ask") + "(.*)$",
        'token': ["text",'text','text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + WORD + SPACE + K("is") + "( *)(.*)$",
        'token': ["text",'text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("print") + "(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("sleep") + "(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("turn") + "(.*)$",
        'token': ["text",'keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("forward") + "(.*)$",
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

def rule_level3():
    return {"start" : [{
        'regex': START_LINE + WORD + SPACE + K("is") + "( *)" + K("ask") + "(.*)$",
        'token': ["text",'text','text','keyword','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + WORD + SPACE + K("is") + "( *)(.*)$",
        'token': ["text",'text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("remove") + "( *)(.*)" + SPACE + K("from") + "( *)"+ WORD +"$",
        'token': ["text",'keyword','text','text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("add") + "( *)(.*)" + SPACE + K("to_list") + "( *)"+ WORD +"$",
        'token': ["text",'keyword','text','text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("print") ,
        'token': ['text','keyword'],
        'next': 'start',
    },{
        'regex': START_LINE + K("turn") ,
        'token': ['text','keyword'],
        'next': 'start',
    },{
        'regex': START_LINE + K("sleep") ,
        'token': ['text','keyword'],
        'next': 'start',
    },{
        'regex': START_LINE + K("forward") ,
        'token': ['text','keyword'],
        'next': 'start',
    },{
        'regex': START_WORD + K("at") + SPACE + K("random") ,
        'token': ['text','keyword','keyword','keyword'],
        'next': 'start',
    },{
        'regex': START_WORD + K("at") ,
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

