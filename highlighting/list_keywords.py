from definition import SPACE, START_WORD, get_translated_keyword

# extra rules for ask
ask_after_is = {
    "regex": START_WORD + get_translated_keyword("is") + SPACE + get_translated_keyword("ask"),
    "token": ["text", "keyword", "text", "keyword"]
}

ask_after_equal = {
    "regex": "(=)" + SPACE + get_translated_keyword("ask"),
    "token": ["keyword", "text", "keyword"]
}


# This variable lists all the keywords in each level, i.e. everything that should be displayed in red (of type `keyword`)
#
# There are several categories of keywords:
# - space_before_and_after
#   These are the keywords that must be "alone" so neither preceded nor followed directly by a word
#
# - no_space
#   These are the keywords that are independent of the context (formerly the symbols).
#   In particular, even if they are between 2 words, the syntax highlighting will select them
#
# - space_before
#   This category of keywords allows you to have keywords that are not preceded
#   by another word, but that can be followed immediately by another word. (see the PR #2413)
#
# - space_after
#   This category of keywords allows you to have keywords that can be preceded immediately
#   by another word, but that are not followed by another word.
#
# - constant
#   list of level constants (direction and colors) not used yet (highlighted in white)
#
# - number & number_with_decimal
#   2 booleans to indicate if the level recognizes numbers, and if so, if it recognizes decimal numbers
#
# - extra_rules
#   Some additional rules that will be added to reduce over highlighting

LEVELS = {
    4: {  # not used
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "color"],
        "no_space": ["comma"],
        "space_before": ["print", "sleep", "forward", "turn", "random"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "number": False,
        "number_with_decimal": False,
        "extra_rules": [ask_after_is]
    },
    5: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "else", "color"],
        "no_space": ["comma"],
        "space_before": ["print", "sleep", "forward", "turn", "random"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": False,
        "number_with_decimal": False,
        "extra_rules": [ask_after_is]
    },
    6: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "else", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+"],
        "space_before": ["print", "sleep", "forward", "turn", "random"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": False,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    7: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "else", "repeat", "times", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+"],
        "space_before": ["print", "sleep", "forward", "turn", "random"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": False,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    8: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "else", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": False,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    9: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "else", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": False,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    10: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "repeat", "for", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "else", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": False,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    11: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "for", "range", "to", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "else", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": False,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    12: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "for", "range", "to", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "else", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": True,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    13: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "for", "range", "to", "and", "or", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "else", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": True,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    14: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "for", "range", "to", "and", "or", "else", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+", "<", ">", "!"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": True,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    15: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "for", "range", "to", "and", "or", "while", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+", "<", ">", "!"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "else", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": True,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    16: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "else", "for", "range", "to", "and", "or", "while", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+", "<", ">", "!", "\\[", "\\]"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "times"],
        "space_after": [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": True,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    17: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "else", "for", "range", "to", "and", "or", "while", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+", "<", ">", "!", "\\[", "\\]", ":"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "times"],
        "space_after": ["elif"],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": True,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
    18: {
        "space_before_and_after": ["is", "at", "add", "to_list", "remove", "from", "in", "if", "else", "for", "range", "to", "and", "or", "while", "input", "repeat", "color"],
        "no_space": ["comma", "-", "=", "/", "\\*", "\\+", "<", ">", "!", "\\[", "\\]", ":", "\\(", "\\)"],
        "space_before": ["print", "sleep", "forward", "turn", "random", "times"],
        "space_after": ["elif"],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "event": ["pressed"],
        "number": True,
        "number_with_decimal": True,
        "extra_rules": [ask_after_is, ask_after_equal]
    },
}
