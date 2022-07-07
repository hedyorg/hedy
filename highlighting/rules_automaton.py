from definition import *

# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions
def rule_level1():
    return add_extra_rule({
    "start" : [{
            'regex': START_LINE + K("ask"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + K("print"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + K("echo"),
            'token': ["text",'keyword'], 
            'next': 'value',
        },{
            'regex': START_LINE + K("forward"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + K("turn"),
            'token': ["text",'keyword'],
            'next': 'direction',
        },{
            'regex': START_LINE + K("color"),
            'token': ["text",'keyword'],
            'next': 'color',
        }],
    "value" : [],
    "color" : [{
            'regex': "(" + \
                    K("black",True)  + "|" +\
                    K("gray",True)   + "|" +\
                    K("white",True)  + "|" +\
                    K("green",True)  + "|" +\
                    K("blue",True)   + "|" +\
                    K("purple",True) + "|" +\
                    K("brown",True)  + "|" +\
                    K("pink",True)   + "|" +\
                    K("red",True)    + "|" +\
                    K("orange",True) + "|" +\
                    K("yellow",True) + \
                ")",
            'token': ["keyword"],
            'next': 'color',
        }],
    "direction" : [{
            'regex': "(" +\
                    K("right",True) + "|" +\
                    K("left",True) +\
                ")",
            'token': ["keyword"],
            'next': 'direction',
        }]
    })

def rule_level2() :
    return add_extra_rule({
    "start" : [{
            'regex': START_LINE + K("print"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + WORD + SPACE + K("is") + SPACE + K("ask"),
            'token': ["text","text","text",'keyword',"text","keyword"],
            'next': 'value',
        },{
            'regex': START_LINE + WORD + SPACE + K("is"),
            'token': ["text","text","text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + K("sleep"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + K("forward"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + K("turn"),
            'token': ["text",'keyword'],
            'next': 'value',
        }],
    "value" : []
    })

def rule_level3():
    return add_extra_rule({"start" : [{
        'regex': START_LINE + WORD + SPACE + K("is") + "( *)" + K("ask"),
        'token': ["text",'text','text','keyword','text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + WORD + SPACE + K("is"),
        'token': ["text",'text','text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + K("print") ,
        'token': ['text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + K("turn") ,
        'token': ['text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + K("sleep") ,
        'token': ['text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + K("forward") ,
        'token': ['text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + K("add"),
        'token': ["text",'keyword'],
        'next': 'valAdd',
    },{
        'regex': START_LINE + K("remove"),
        'token': ["text",'keyword'],
        'next': 'valRemove',
    }],
    "value" : [{
        'regex': START_WORD + K("at") + SPACE + K("random") ,
        'token': ['text','keyword','keyword','keyword'],
        'next': 'value',
    },{
        'regex': START_WORD + K("at") ,
        'token': ['text','keyword'],
        'next': 'value',
    }],
    "valAdd"    : [{
        'regex': START_WORD + K("to_list") ,
        'token': ['text','keyword'],
        'next': 'valueTo',
    }],
    "valueTo" : [],
    "valRemove" : [{
        'regex': START_WORD + K("from") ,
        'token': ['text','keyword'],
        'next': 'valueFrom',
    }],
    "valueFrom" : [],
    })

def add_extra_rule(automaton):
    for state in automaton:
        if state != "start":
            automaton[state].insert(0,{
                'regex': "(^|$)",
                'token': ["text"],
                'next': 'start',
            })
        automaton[state].insert(0,{
            'regex': "#.*$",
            'token': "comment",
            'next': 'start',
        })
        automaton[state].insert(0,{
            'regex': "_\\?_",
            'token': "invalid",
            'next': state,
        })
        automaton[state].insert(0,{
            'regex': '(^| )(_)(?= |$)',
            'token': ['text','invalid'],
            'next': state,
        })
    return automaton
