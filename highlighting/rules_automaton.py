from definition import *

# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions
def rule_level1():
    return add_extra_rule({
    "start" : [{
            'regex': START_LINE + translate("ask"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + translate("print"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + translate("echo"),
            'token': ["text",'keyword'], 
            'next': 'value',
        },{
            'regex': START_LINE + translate("forward"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + translate("turn"),
            'token': ["text",'keyword'],
            'next': 'direction',
        },{
            'regex': START_LINE + translate("color"),
            'token': ["text",'keyword'],
            'next': 'color',
        }],
    "value" : [],
    "color" : [{
            'regex': "(" + \
                    translate("black",True)  + "|" +\
                    translate("gray",True)   + "|" +\
                    translate("white",True)  + "|" +\
                    translate("green",True)  + "|" +\
                    translate("blue",True)   + "|" +\
                    translate("purple",True) + "|" +\
                    translate("brown",True)  + "|" +\
                    translate("pink",True)   + "|" +\
                    translate("red",True)    + "|" +\
                    translate("orange",True) + "|" +\
                    translate("yellow",True) + \
                ")",
            'token': [TOKEN_CONSTANT],
        }],
    "direction" : [{
            'regex': "(" +\
                    translate("right",True) + "|" +\
                    translate("left",True) +\
                ")",
            'token': [TOKEN_CONSTANT],
        }]
    })

def rule_level2() :
    return add_extra_rule({
    "start" : [{
            'regex': START_LINE + translate("print"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + WORD + SPACE + translate("is") + SPACE + translate("ask"),
            'token': ["text","text","text",'keyword',"text","keyword"],
            'next': 'value',
        },{
            'regex': START_LINE + WORD + SPACE + translate("is"),
            'token': ["text","text","text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + translate("sleep"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + translate("forward"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + translate("turn"),
            'token': ["text",'keyword'],
            'next': 'value',
        },{
            'regex': START_LINE + translate("color"),
            'token': ["text",'keyword'],
            'next': 'value',
        }],
    "value" : [{
            'regex': "(" +\
                    translate("black",True) + "|" +\
                    translate("blue",True) + "|" +\
                    translate("brown",True) + "|" +\
                    translate("gray",True) + "|" +\
                    translate("green",True) + "|" +\
                    translate("orange",True) + "|" +\
                    translate("pink",True) + "|" +\
                    translate("purple",True) + "|" +\
                    translate("red",True) + "|" +\
                    translate("white",True) + "|" +\
                    translate("yellow",True) +\
                ")",
            'token': [TOKEN_CONSTANT],
        }]
    })

def rule_level3():
    return add_extra_rule({"start" : [{
        'regex': START_LINE + WORD + SPACE + translate("is") + "( *)" + translate("ask"),
        'token': ["text",'text','text','keyword','text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + WORD + SPACE + translate("is"),
        'token': ["text",'text','text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + translate("print") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + translate("turn") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + translate("sleep") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + translate("forward") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + translate("add"),
        'token': ["text",'keyword'],
        'next': 'valAdd',
    },{
        'regex': START_LINE + translate("remove"),
        'token': ["text",'keyword'],
        'next': 'valRemove',
    },{
        'regex': START_LINE + translate("color"),
        'token': ["text",'keyword'],
        'next': 'value',
    }],
    "value" : [{
        'regex': START_WORD + translate("at") + SPACE + translate("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + translate("at") ,
        'token': ['text','keyword'],
    },{
        'regex': translate("comma") ,
        'token': ['keyword'],
    },{
        'regex': "(" +\
                translate("black",True) + "|" +\
                translate("blue",True) + "|" +\
                translate("brown",True) + "|" +\
                translate("gray",True) + "|" +\
                translate("green",True) + "|" +\
                translate("orange",True) + "|" +\
                translate("pink",True) + "|" +\
                translate("purple",True) + "|" +\
                translate("red",True) + "|" +\
                translate("white",True) + "|" +\
                translate("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueExpr" : [{
        'regex': START_WORD + translate("at") + SPACE + translate("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + translate("at") ,
        'token': ['text','keyword'],
    }],
    "valAdd"    : [{
        'regex': START_WORD + translate("to_list") ,
        'token': ['text','keyword'],
        'next': 'valueTo',
    },{
        'regex': "(" +\
                translate("black",True) + "|" +\
                translate("blue",True) + "|" +\
                translate("brown",True) + "|" +\
                translate("gray",True) + "|" +\
                translate("green",True) + "|" +\
                translate("orange",True) + "|" +\
                translate("pink",True) + "|" +\
                translate("purple",True) + "|" +\
                translate("red",True) + "|" +\
                translate("white",True) + "|" +\
                translate("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueTo" : [],
    "valRemove" : [{
        'regex': START_WORD + translate("from") ,
        'token': ['text','keyword'],
        'next': 'valueFrom',
    },{
        'regex': "(" +\
                translate("black",True) + "|" +\
                translate("blue",True) + "|" +\
                translate("brown",True) + "|" +\
                translate("gray",True) + "|" +\
                translate("green",True) + "|" +\
                translate("orange",True) + "|" +\
                translate("pink",True) + "|" +\
                translate("purple",True) + "|" +\
                translate("red",True) + "|" +\
                translate("white",True) + "|" +\
                translate("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueFrom" : [],
    })


def rule_level4():
    return add_extra_rule({"start" : [{
        'regex': START_LINE + WORD + SPACE + translate("is") + "( *)" + translate("ask"),
        'token': ["text",'text','text','keyword','text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + WORD + SPACE + translate("is"),
        'token': ["text",'text','text','keyword'],
        'next': 'value',
    },{
        'regex': START_LINE + translate("print") ,
        'token': ['text','keyword'],
        'next': 'valueExpr',
    },{
        'regex': START_LINE + translate("turn") ,
        'token': ['text','keyword'],
        'next': 'valueSimple',
    },{
        'regex': START_LINE + translate("sleep") ,
        'token': ['text','keyword'],
        'next': 'valueSimple',
    },{
        'regex': START_LINE + translate("forward") ,
        'token': ['text','keyword'],
        'next': 'valueSimple',
    },{
        'regex': START_LINE + translate("color"),
        'token': ["text",'keyword'],
        'next': 'valueSimple',
    },{
        'regex': START_LINE + translate("add"),
        'token': ["text",'keyword'],
        'next': 'valAdd',
    },{
        'regex': START_LINE + translate("remove"),
        'token': ["text",'keyword'],
        'next': 'valRemove',
    }],
    "value" : [{
        'regex': START_WORD + translate("at") + SPACE + translate("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + translate("at") ,
        'token': ['text','keyword'],
    },{
        'regex': translate("comma") ,
        'token': ['keyword'],
    },{
        'regex': "(" +\
                translate("black",True) + "|" +\
                translate("blue",True) + "|" +\
                translate("brown",True) + "|" +\
                translate("gray",True) + "|" +\
                translate("green",True) + "|" +\
                translate("orange",True) + "|" +\
                translate("pink",True) + "|" +\
                translate("purple",True) + "|" +\
                translate("red",True) + "|" +\
                translate("white",True) + "|" +\
                translate("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueExpr" : [{
        'regex': START_WORD + translate("at") + SPACE + translate("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + translate("at") ,
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
        'regex': START_WORD + translate("at") + SPACE + translate("random") ,
        'token': ['text','keyword','keyword','keyword'],
    },{
        'regex': START_WORD + translate("at") ,
        'token': ['text','keyword'],
    },{
        'regex': "(" +\
                translate("black",True) + "|" +\
                translate("blue",True) + "|" +\
                translate("brown",True) + "|" +\
                translate("gray",True) + "|" +\
                translate("green",True) + "|" +\
                translate("orange",True) + "|" +\
                translate("pink",True) + "|" +\
                translate("purple",True) + "|" +\
                translate("red",True) + "|" +\
                translate("white",True) + "|" +\
                translate("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valAdd"    : [{
        'regex': START_WORD + translate("to_list") ,
        'token': ['text','keyword'],
        'next': 'valueTo',
    },{
        'regex': "(" +\
                translate("black",True) + "|" +\
                translate("blue",True) + "|" +\
                translate("brown",True) + "|" +\
                translate("gray",True) + "|" +\
                translate("green",True) + "|" +\
                translate("orange",True) + "|" +\
                translate("pink",True) + "|" +\
                translate("purple",True) + "|" +\
                translate("red",True) + "|" +\
                translate("white",True) + "|" +\
                translate("yellow",True) +\
            ")",
        'token': [TOKEN_CONSTANT],
    }],
    "valueTo" : [],
    "valRemove" : [{
        'regex': START_WORD + translate("from") ,
        'token': ['text','keyword'],
        'next': 'valueFrom',
    },{
        'regex': "(" +\
                translate("black",True) + "|" +\
                translate("blue",True) + "|" +\
                translate("brown",True) + "|" +\
                translate("gray",True) + "|" +\
                translate("green",True) + "|" +\
                translate("orange",True) + "|" +\
                translate("pink",True) + "|" +\
                translate("purple",True) + "|" +\
                translate("red",True) + "|" +\
                translate("white",True) + "|" +\
                translate("yellow",True) +\
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
