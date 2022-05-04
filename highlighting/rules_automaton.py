from definition import *

# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions

def rule_level1():
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

