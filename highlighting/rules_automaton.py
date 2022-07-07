from definition import *

# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions
def rule_level1():
    return {
    "start" : [{
            'regex': "#.*$",
            'token': "comment",
            'next': 'start',
        },{
            'regex': START_LINE + K("ask"),
            'token': ["text",'keyword'],
            'next': 'none',
        },{
            'regex': START_LINE + K("print"),
            'token': ["text",'keyword'],
            'next': 'none',
        },{
            'regex': START_LINE + K("echo"),
            'token': ["text",'keyword'],
            'next': 'none',
        },{
            'regex': START_LINE + K("forward"),
            'token': ["text",'keyword'],
            'next': 'none',
        },{
            'regex': START_LINE + K("turn"),
            'token': ["text",'keyword'],
            'next': 'direction',
        },{
            'regex': START_LINE + K("color"),
            'token': ["text",'keyword'],
            'next': 'color',
        }],
    "none" : [{
            'regex': "(^|$)",
            'token': ["text"],
            'next': 'start',
        },{
            'regex': "#.*$",
            'token': "comment",
            'next': 'start',
        }],
    "color" : [{
            'regex': "(^|$)",
            'token': ["text"],
            'next': 'start',
        },{
            'regex': "(" + \
                    K("purple",True) + "|" +\
                    K("red",True)    + "|" +\
                    K("black",True)  + "|" +\
                    K("blue",True)   + "|" +\
                    K("brown",True)  + "|" +\
                    K("gray",True)   + "|" +\
                    K("green",True)  + "|" +\
                    K("orange",True) + "|" +\
                    K("pink",True)   + "|" +\
                    K("white",True)  + "|" +\
                    K("yellow",True) + \
                ")",
            'token': ["keyword"],
            'next': 'color',
        },{
            'regex': "#.*$",
            'token': "comment",
            'next': 'start',
        }],
    "direction" : [{
            'regex': "(^|$)",
            'token': ["text"],
            'next': 'start',
        },{
            'regex': "(" +\
                    K("right",True) + "|" +\
                    K("left",True) +\
                ")",
            'token': ["keyword"],
            'next': 'direction',
        },{
            'regex': "#.*$",
            'token': "comment",
            'next': 'start',
        }]
    }


def rule_level2() :
    return {
    "start" : [{
            'regex': "#.*$",
            'token': "comment",
            'next': 'start',
        },{
            'regex': START_LINE + K("print"),
            'token': ["text",'keyword'],
            'next': 'none',
        },{
            'regex': START_LINE + WORD + SPACE + K("is") + SPACE + K("ask"),
            'token': ["text","text","text",'keyword',"text","keyword"],
            'next': 'none',
        },{
            'regex': START_LINE + WORD + SPACE + K("is"),
            'token': ["text","text","text",'keyword'],
            'next': 'none',
        },{
            'regex': START_LINE + K("sleep"),
            'token': ["text",'keyword'],
            'next': 'none',
        },{
            'regex': START_LINE + K("forward"),
            'token': ["text",'keyword'],
            'next': 'none',
        },{
            'regex': START_LINE + K("turn"),
            'token': ["text",'keyword'],
            'next': 'none',
        }],
    "none" : [{
            'regex': "(^|$)",
            'token': ["text"],
            'next': 'start',
        },{
            'regex': "#.*$",
            'token': "comment",
            'next': 'start',
        }]
    }

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
        'regex': START_LINE + K("remove") + "( *)(.*)" + SPACE + K("from") + "( *)$",
        'token': ["text",'keyword','text','text','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("remove") + "( *)(.*)$",
        'token': ["text",'keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("add") + "( *)(.*)" + SPACE + K("to_list") + "( *)"+ WORD +"$",
        'token': ["text",'keyword','text','text','text','keyword','text','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("add") + "( *)(.*)" + SPACE + K("to_list") + "( *)$",
        'token': ["text",'keyword','text','text','text','keyword','text'],
        'next': 'start',
    },{
        'regex': START_LINE + K("add") + "( *)(.*)$",
        'token': ["text",'keyword','text','text'],
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