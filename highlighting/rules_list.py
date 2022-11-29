from definition import (DIGIT, END_WORD, START_WORD, TOKEN_CONSTANT,
                        get_translated_keyword)
from list_keywords import LEVELS

# After the level 4
# so what is not in quotes is code,
# and any keyword in the code can be colored independently
# of what is around it, so we use a general function
# This general function uses LEVELS


def rule_all(level):

    # get keyword by level
    data_level = LEVELS[level]

    # initialize with extra rules
    list_rules = data_level["extra_rules"]

    # Rule for comments :
    list_rules.append({'regex': '#.*$', 'token': 'comment', 'next': 'start', 'unicode': True})

    # Rule for quoted string :
    # complete
    list_rules.append({'regex': '\"[^\"]*\"', 'token': 'constant.character', 'next': 'start', 'unicode': True})
    list_rules.append({'regex': "\'[^\']*\'", 'token': 'constant.character', 'next': 'start', 'unicode': True})

    # incomplete
    list_rules.append({'regex': '\"[^\"]*$', 'token': 'constant.character', 'next': 'start', 'unicode': True})
    list_rules.append({'regex': "\'[^\']*$", 'token': 'constant.character', 'next': 'start', 'unicode': True})

    # Rule for blanks marks :
    list_rules.append({'regex': '_\\?_', 'token': 'invalid', 'next': 'start', 'unicode': True})
    list_rules.append({'regex': '(^| )(_)(?= |$)', 'token': ['text', 'invalid'], 'next': 'start', 'unicode': True})

    # Rules for numbers
    if (data_level["number"]):
        if (data_level["number_with_decimal"]):
            number_regex = '(' + DIGIT + '*\\.?' + DIGIT + '+)'
        else:
            number_regex = '(' + DIGIT + '+)'

        list_rules.append({'regex': START_WORD + number_regex + END_WORD,
                          'token': ['text', 'variable'], 'next': 'start', 'unicode': True})

        # Special case of an number directly followed by a number
        for command in data_level["space_before"]:
            list_rules.append({
                'regex': START_WORD + get_translated_keyword(command) + number_regex + END_WORD,
                'token': ['text', 'keyword', 'variable'],
                'next': 'start',
                'unicode': True
            })

        for command in data_level["no_space"]:
            list_rules.append({
                'regex': get_translated_keyword(command) + number_regex + END_WORD,
                'token': ['keyword', 'variable'],
                'next': 'start',
                'unicode': True
            })

    # Rules for commands of space_before_and_after
    # These are the keywords that must be "alone" so neither preceded nor followed directly by a word
    for command in data_level["space_before_and_after"]:
        list_rules.append({
            'regex': START_WORD + get_translated_keyword(command) + END_WORD,
            'token': ["text", "keyword"],
            'next': "start",
            'unicode': True
        })

    # Rules for commands of no_space
    #  These are the keywords that are independent of the context (formerly the symbols
    # In particular, even if they are between 2 words, the syntax highlighting will select them
    for command in data_level["no_space"]:
        list_rules.append({
            'regex': get_translated_keyword(command),
            'token': ["keyword"],
            'next': "start",
            'unicode': True
        })

    # Rules for commands of space_before
    #  This category of keywords allows you to have keywords that are not preced
    # by another word, but that can be followed immediately by another word. (see the PR #2413)*/
    for command in data_level["space_before"]:
        list_rules.append({
            'regex': START_WORD + get_translated_keyword(command),
            'token': ["text", "keyword"],
            'next': "start",
            'unicode': True
        })

    # Rules for commands of space_after
    #  This category of keywords allows you to have keywords that can be preceded immediate
    # by another word, but that are not followed by another word.*/
    for command in data_level["space_after"]:
        list_rules.append({
            'regex': get_translated_keyword(command) + END_WORD,
            'token': ["keyword"],
            'next': "start",
            'unicode': True
        })

    # Rules for constants (colors, directions)
    for command in data_level['constant']:
        list_rules.append({
            'regex': START_WORD + get_translated_keyword(command) + END_WORD,
            'token': ["text", TOKEN_CONSTANT],
            'next': "start",
            'unicode': True
        })

    return {"start": list_rules}
