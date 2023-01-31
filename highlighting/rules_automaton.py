from definition import (END_WORD, SPACE, START_LINE, START_WORD,
                        TOKEN_CONSTANT, WORD, get_translated_keyword)


# In the first levels, the strings are not yet well defined,
# so we have to color them with respect to what is around,
# so we use particular functions
def rule_level1():
    return add_extra_rule({
        "start": [{
            'regex': START_LINE + get_translated_keyword("ask"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("print"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("echo"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("forward"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("turn"),
            'token': ["text", 'keyword'],
            'next': 'direction',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("color"),
            'token': ["text", 'keyword'],
            'next': 'color',
            'unicode': True
        }],
        "value": [],
        "color": [{
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }],
        "direction": [{
            'regex': "(" +
            get_translated_keyword("right", True) + "|" +
            get_translated_keyword("left", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }]
    })


def rule_level2():
    return add_extra_rule({
        "start": [{
            'regex': START_LINE + get_translated_keyword("print"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + WORD + SPACE + get_translated_keyword("is") + SPACE + get_translated_keyword("ask"),
            'token': ["text", "text", "text", 'keyword', "text", "keyword"],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + WORD + SPACE + get_translated_keyword("is"),
            'token': ["text", "text", "text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("sleep"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("forward"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("turn"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }, {
            'regex': START_LINE + get_translated_keyword("color"),
            'token': ["text", 'keyword'],
            'next': 'value',
            'unicode': True
        }],
        "value": [{
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }]
    })


def rule_level3():
    return add_extra_rule({"start": [{
        'regex': START_LINE + WORD + SPACE + get_translated_keyword("is") + "( *)" + get_translated_keyword("ask"),
        'token': ["text", 'text', 'text', 'keyword', 'text', 'keyword'],
        'next': 'valueExpr',
        'unicode': True
    }, {
        'regex': START_LINE + WORD + SPACE + get_translated_keyword("is"),
        'token': ["text", 'text', 'text', 'keyword'],
        'next': 'value',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("print"),
        'token': ['text', 'keyword'],
        'next': 'valueExpr',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("turn"),
        'token': ['text', 'keyword'],
        'next': 'valueExpr',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("sleep"),
        'token': ['text', 'keyword'],
        'next': 'valueExpr',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("forward"),
        'token': ['text', 'keyword'],
        'next': 'valueExpr',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("add"),
        'token': ["text", 'keyword'],
        'next': 'valAdd',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("remove"),
        'token': ["text", 'keyword'],
        'next': 'valRemove',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("color"),
        'token': ["text", 'keyword'],
        'next': 'value',
        'unicode': True
    }],
        "value": [{
            'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random"),
            'token': ['text', 'keyword', 'keyword', 'keyword'],
            'unicode': True
        }, {
            'regex': START_WORD + get_translated_keyword("at") + END_WORD,
            'token': ['text', 'keyword'],
            'unicode': True
        }, {
            'regex': get_translated_keyword("comma"),
            'token': ['keyword'],
            'unicode': True
        }, {
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }],
        "valueExpr": [{
            'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random"),
            'token': ['text', 'keyword', 'keyword', 'keyword'],
            'unicode': True
        }, {
            'regex': START_WORD + get_translated_keyword("at") + END_WORD,
            'token': ['text', 'keyword'],
            'unicode': True
        }],
        "valAdd": [{
            'regex': START_WORD + get_translated_keyword("to_list") + END_WORD,
            'token': ['text', 'keyword'],
            'next': 'valueTo',
            'unicode': True
        }, {
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }],
        "valueTo": [],
        "valRemove": [{
            'regex': START_WORD + get_translated_keyword("from") + END_WORD,
            'token': ['text', 'keyword'],
            'next': 'valueFrom',
            'unicode': True
        }, {
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }],
        "valueFrom": [],
    })


def rule_level4():
    return add_extra_rule({"start": [{
        'regex': START_LINE + WORD + SPACE + get_translated_keyword("is") + "( *)" + get_translated_keyword("ask"),
        'token': ["text", 'text', 'text', 'keyword', 'text', 'keyword'],
        'next': 'valueExpr',
        'unicode': True
    }, {
        'regex': START_LINE + WORD + SPACE + get_translated_keyword("is"),
        'token': ["text", 'text', 'text', 'keyword'],
        'next': 'value',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("print"),
        'token': ['text', 'keyword'],
        'next': 'valueExpr',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("turn"),
        'token': ['text', 'keyword'],
        'next': 'valueSimple',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("sleep"),
        'token': ['text', 'keyword'],
        'next': 'valueSimple',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("forward"),
        'token': ['text', 'keyword'],
        'next': 'valueSimple',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("color"),
        'token': ["text", 'keyword'],
        'next': 'valueSimple',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("add"),
        'token': ["text", 'keyword'],
        'next': 'valAdd',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("remove"),
        'token': ["text", 'keyword'],
        'next': 'valRemove',
        'unicode': True
    }, {
        'regex': START_LINE + get_translated_keyword("clear"),
        'token': ['text', 'event'],
        'unicode': True
    }],
        "value": [{
            'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random"),
            'token': ['text', 'keyword', 'keyword', 'keyword'],
            'unicode': True
        }, {
            'regex': START_WORD + get_translated_keyword("at") + END_WORD,
            'token': ['text', 'keyword'],
            'unicode': True
        }, {
            'regex': get_translated_keyword("comma"),
            'token': ['keyword'],
            'unicode': True
        }, {
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }],
        "valueExpr": [{
            'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random"),
            'token': ['text', 'keyword', 'keyword', 'keyword'],
            'unicode': True
        }, {
            'regex': START_WORD + get_translated_keyword("at") + END_WORD,
            'token': ['text', 'keyword'],
            'unicode': True
        }, {
            'regex': '\"[^\"]*\"',
            'token': 'constant.character',
            'unicode': True
        }, {
            'regex': "\'[^\']*\'",
            'token': 'constant.character',
            'unicode': True
        }, {
            'regex': '\"[^\"]*$',
            'token': 'constant.character',
            'next': 'start',
            'unicode': True
        }, {
            'regex': "\'[^\']*$",
            'token': 'constant.character',
            'next': 'start',
            'unicode': True
        }],
        "valueSimple": [{
            'regex': START_WORD + get_translated_keyword("at") + SPACE + get_translated_keyword("random"),
            'token': ['text', 'keyword', 'keyword', 'keyword'],
            'unicode': True
        }, {
            'regex': START_WORD + get_translated_keyword("at") + END_WORD,
            'token': ['text', 'keyword'],
            'unicode': True
        }, {
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }],
        "valAdd": [{
            'regex': START_WORD + get_translated_keyword("to_list") + END_WORD,
            'token': ['text', 'keyword'],
            'next': 'valueTo',
            'unicode': True
        }, {
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }],
        "valueTo": [],
        "valRemove": [{
            'regex': START_WORD + get_translated_keyword("from") + END_WORD,
            'token': ['text', 'keyword'],
            'next': 'valueFrom',
            'unicode': True
        }, {
            'regex': "(" +
            get_translated_keyword("black", True) + "|" +
            get_translated_keyword("blue", True) + "|" +
            get_translated_keyword("brown", True) + "|" +
            get_translated_keyword("gray", True) + "|" +
            get_translated_keyword("green", True) + "|" +
            get_translated_keyword("orange", True) + "|" +
            get_translated_keyword("pink", True) + "|" +
            get_translated_keyword("purple", True) + "|" +
            get_translated_keyword("red", True) + "|" +
            get_translated_keyword("white", True) + "|" +
            get_translated_keyword("yellow", True) +
            ")",
            'token': [TOKEN_CONSTANT],
            'unicode': True
        }],
        "valueFrom": [],
    })


def add_extra_rule(automaton):
    for state in automaton:
        if state != "start":
            automaton[state].insert(0, {
                'regex': "(^|$)",
                'token': ["text"],
                'next': 'start',
            })
        automaton[state].insert(0, {
            'regex': "#.*$",
            'token': "comment",
            'next': 'start',
        })
        automaton[state].insert(0, {
            'regex': "_\\?_",
            'token': "invalid",
            'next': state,
        })
        automaton[state].insert(0, {
            'regex': '(^| )(_)(?= |$)',
            'token': ['text', 'invalid'],
            'next': state,
        })
    return automaton
