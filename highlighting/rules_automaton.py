from definition import *

# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions
def rule_level1():
    return add_extra_rule({
    "start" : [{
            'regex': START_LINE + get_translated_keyword("ask"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + get_translated_keyword("print"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + get_translated_keyword("echo"),
            'token': ["text",'keyword'], 
            'next': 'value',
        },{
            'regex': START_LINE + get_translated_keyword("forward"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + get_translated_keyword("turn"),
            'token': ["text",'keyword'],
            'next': 'direction',
        },{
            'regex': START_LINE + get_translated_keyword("color"),
            'token': ["text",'keyword'],
            'next': 'color',
        }],
    "value" : [],
    "color" : [{
            'regex': "(" + \
                    get_translated_keyword("black",True)  + "|" +\
                    get_translated_keyword("gray",True)   + "|" +\
                    get_translated_keyword("white",True)  + "|" +\
                    get_translated_keyword("green",True)  + "|" +\
                    get_translated_keyword("blue",True)   + "|" +\
                    get_translated_keyword("purple",True) + "|" +\
                    get_translated_keyword("brown",True)  + "|" +\
                    get_translated_keyword("pink",True)   + "|" +\
                    get_translated_keyword("red",True)    + "|" +\
                    get_translated_keyword("orange",True) + "|" +\
                    get_translated_keyword("yellow",True) + \
                ")",
            'token': [TOKEN_CONSTANT],
        }],
    "direction" : [{
            'regex': "(" +\
                    get_translated_keyword("right",True) + "|" +\
                    get_translated_keyword("left",True) +\
                ")",
            'token': [TOKEN_CONSTANT],
        }]
    })

def rule_level2() :
    return add_extra_rule({
    "start" : [{
            'regex': START_LINE + get_translated_keyword("print"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + WORD + SPACE + get_translated_keyword("is") + SPACE + get_translated_keyword("ask"),
            'token': ["text","text","text",'keyword',"text","keyword"],
            'next': 'value',
        },{
            'regex': START_LINE + WORD + SPACE + get_translated_keyword("is"),
            'token': ["text","text","text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + get_translated_keyword("sleep"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + get_translated_keyword("forward"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + get_translated_keyword("turn"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + get_translated_keyword("color"),
            'token': ["text",'keyword'],
            'next': 'value',
        }],
    "value" : [{
            'regex': "(" +\
                    get_translated_keyword("black",True) + "|" +\
                    get_translated_keyword("blue",True) + "|" +\
                    get_translated_keyword("brown",True) + "|" +\
                    get_translated_keyword("gray",True) + "|" +\
                    get_translated_keyword("green",True) + "|" +\
                    get_translated_keyword("orange",True) + "|" +\
                    get_translated_keyword("pink",True) + "|" +\
                    get_translated_keyword("purple",True) + "|" +\
                    get_translated_keyword("red",True) + "|" +\
                    get_translated_keyword("white",True) + "|" +\
                    get_translated_keyword("yellow",True) +\
                ")",
            'token': [TOKEN_CONSTANT],
        }]
    })

def rule_level3():
    return add_extra_rule({"start" : [{
        'regex': START_LINE + WORD + SPACE + get_translated_keyword("is") + "( *)" + get_translated_keyword("ask"),
        'token': ["text",'text','text','keyword','text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + WORD + SPACE + get_translated_keyword("is"),
        'token': ["text",'text','text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + get_translated_keyword("print") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + get_translated_keyword("turn") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + get_translated_keyword("sleep") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + get_translated_keyword("forward") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + get_translated_keyword("add"),
        'token': ["text",'keyword'],
        'next': 'valAdd',
    },{
        'regex': START_LINE + get_translated_keyword("remove"),
        'token': ["text",'keyword'],
        'next': 'valRemove',
    },{
        'regex': START_LINE + get_translated_keyword("color"),
        'token': ["text",'keyword'],
        'next': 'value',
    }],
    "value" : [{
        'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + get_translated_keyword("at") ,
        'token': ['text','keyword'],
    },{
        'regex': get_translated_keyword("comma") ,
        'token': ['keyword'],
    },{
        'regex': "(" +\
                get_translated_keyword("black",True) + "|" +\
                get_translated_keyword("blue",True) + "|" +\
                get_translated_keyword("brown",True) + "|" +\
                get_translated_keyword("gray",True) + "|" +\
                get_translated_keyword("green",True) + "|" +\
                get_translated_keyword("orange",True) + "|" +\
                get_translated_keyword("pink",True) + "|" +\
                get_translated_keyword("purple",True) + "|" +\
                get_translated_keyword("red",True) + "|" +\
                get_translated_keyword("white",True) + "|" +\
                get_translated_keyword("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueExpr" : [{
        'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + get_translated_keyword("at") ,
        'token': ['text','keyword'],
    }],
    "valAdd"    : [{
        'regex': START_WORD + get_translated_keyword("to_list") ,
        'token': ['text','keyword'],
        'next': 'valueTo',
    },{
        'regex': "(" +\
                get_translated_keyword("black",True) + "|" +\
                get_translated_keyword("blue",True) + "|" +\
                get_translated_keyword("brown",True) + "|" +\
                get_translated_keyword("gray",True) + "|" +\
                get_translated_keyword("green",True) + "|" +\
                get_translated_keyword("orange",True) + "|" +\
                get_translated_keyword("pink",True) + "|" +\
                get_translated_keyword("purple",True) + "|" +\
                get_translated_keyword("red",True) + "|" +\
                get_translated_keyword("white",True) + "|" +\
                get_translated_keyword("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueTo" : [],
    "valRemove" : [{
        'regex': START_WORD + get_translated_keyword("from") ,
        'token': ['text','keyword'],
        'next': 'valueFrom',
    },{
        'regex': "(" +\
                get_translated_keyword("black",True) + "|" +\
                get_translated_keyword("blue",True) + "|" +\
                get_translated_keyword("brown",True) + "|" +\
                get_translated_keyword("gray",True) + "|" +\
                get_translated_keyword("green",True) + "|" +\
                get_translated_keyword("orange",True) + "|" +\
                get_translated_keyword("pink",True) + "|" +\
                get_translated_keyword("purple",True) + "|" +\
                get_translated_keyword("red",True) + "|" +\
                get_translated_keyword("white",True) + "|" +\
                get_translated_keyword("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueFrom" : [],
    })


def rule_level4():
    return add_extra_rule({"start" : [{
        'regex': START_LINE + WORD + SPACE + get_translated_keyword("is") + "( *)" + get_translated_keyword("ask"),
        'token': ["text",'text','text','keyword','text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + WORD + SPACE + get_translated_keyword("is"),
        'token': ["text",'text','text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + get_translated_keyword("print") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + get_translated_keyword("turn") ,
        'token': ['text','keyword'],
        'next': 'valueSimple',
    },{
        'regex': START_LINE + get_translated_keyword("sleep") ,
        'token': ['text','keyword'],
        'next': 'valueSimple',
    },{
        'regex': START_LINE + get_translated_keyword("forward") ,
        'token': ['text','keyword'],
        'next': 'valueSimple',
    },{
        'regex': START_LINE + get_translated_keyword("color"),
        'token': ["text",'keyword'],
        'next': 'valueSimple',
    },{
        'regex': START_LINE + get_translated_keyword("add"),
        'token': ["text",'keyword'],
        'next': 'valAdd',
    },{
        'regex': START_LINE + get_translated_keyword("remove"),
        'token': ["text",'keyword'],
        'next': 'valRemove',
    }],
    "value" : [{
        'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + get_translated_keyword("at") ,
        'token': ['text','keyword'],
    },{
        'regex': get_translated_keyword("comma") ,
        'token': ['keyword'],
    },{
        'regex': "(" +\
                get_translated_keyword("black",True) + "|" +\
                get_translated_keyword("blue",True) + "|" +\
                get_translated_keyword("brown",True) + "|" +\
                get_translated_keyword("gray",True) + "|" +\
                get_translated_keyword("green",True) + "|" +\
                get_translated_keyword("orange",True) + "|" +\
                get_translated_keyword("pink",True) + "|" +\
                get_translated_keyword("purple",True) + "|" +\
                get_translated_keyword("red",True) + "|" +\
                get_translated_keyword("white",True) + "|" +\
                get_translated_keyword("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueExpr" : [{
        'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + get_translated_keyword("at") ,
        'token': ['text','keyword'],
    },{
        'regex': '\"[^\"]*\"',
        'token': 'constant.character',
    },{
        'regex': "\'[^\']*\'",
        'token': 'constant.character',
    },{
        'regex': '\"[^\"]*$',
        'token': 'constant.character',
        'next' : 'start'
    },{
        'regex': "\'[^\']*$",
        'token': 'constant.character',
        'next' : 'start'
    }],
    "valueSimple":[{
        'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + get_translated_keyword("at") ,
        'token': ['text','keyword'],
    },{
        'regex': "(" +\
                get_translated_keyword("black",True) + "|" +\
                get_translated_keyword("blue",True) + "|" +\
                get_translated_keyword("brown",True) + "|" +\
                get_translated_keyword("gray",True) + "|" +\
                get_translated_keyword("green",True) + "|" +\
                get_translated_keyword("orange",True) + "|" +\
                get_translated_keyword("pink",True) + "|" +\
                get_translated_keyword("purple",True) + "|" +\
                get_translated_keyword("red",True) + "|" +\
                get_translated_keyword("white",True) + "|" +\
                get_translated_keyword("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valAdd"    : [{
        'regex': START_WORD + get_translated_keyword("to_list") ,
        'token': ['text','keyword'],
        'next': 'valueTo',
    },{
        'regex': "(" +\
                get_translated_keyword("black",True) + "|" +\
                get_translated_keyword("blue",True) + "|" +\
                get_translated_keyword("brown",True) + "|" +\
                get_translated_keyword("gray",True) + "|" +\
                get_translated_keyword("green",True) + "|" +\
                get_translated_keyword("orange",True) + "|" +\
                get_translated_keyword("pink",True) + "|" +\
                get_translated_keyword("purple",True) + "|" +\
                get_translated_keyword("red",True) + "|" +\
                get_translated_keyword("white",True) + "|" +\
                get_translated_keyword("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueTo" : [],
    "valRemove" : [{
        'regex': START_WORD + get_translated_keyword("from") ,
        'token': ['text','keyword'],
        'next': 'valueFrom',
    },{
        'regex': "(" +\
                get_translated_keyword("black",True) + "|" +\
                get_translated_keyword("blue",True) + "|" +\
                get_translated_keyword("brown",True) + "|" +\
                get_translated_keyword("gray",True) + "|" +\
                get_translated_keyword("green",True) + "|" +\
                get_translated_keyword("orange",True) + "|" +\
                get_translated_keyword("pink",True) + "|" +\
                get_translated_keyword("purple",True) + "|" +\
                get_translated_keyword("red",True) + "|" +\
                get_translated_keyword("white",True) + "|" +\
                get_translated_keyword("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
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
