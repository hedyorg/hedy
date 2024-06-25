# This file defines the special regexes

# list of symbols recognized as characters (with non-Latin characters)
CHARACTER = '[\\p{Lu}\\p{Ll}\\p{Lt}\\p{Lm}\\p{Lo}\\p{Nl}_\\p{Mn}\\p{Mc}\\p{Nd}\\p{Pc}·]'

# definition of word
WORD = '(' + CHARACTER + "+)"
# space
SPACE = "( +)"

# beginning and end of one line, including space
START_LINE = '(^ *)'
END_LINE = '( *$)'

# beginning and end of words
START_WORD = '(^| )'
END_WORD = '(?!' + CHARACTER + ')'

DIGIT = '[__DIGIT__]'

TRANSLATE_WORDS = [
    "add",
    "and",
    "ask",
    "at",
    "black",
    "blue",
    "brown",
    "call",
    "clear",
    "color",
    "comma",
    "def",
    "define",
    "echo",
    "elif",
    "else",
    "false",
    "False",
    "for",
    "forward",
    "from",
    "gray",
    "green",
    "if",
    "in",
    "input",
    "is",
    "left",
    "length",
    "not_in",
    "or",
    "orange",
    "pink",
    "play",
    "pressed",
    "print",
    "purple",
    "random",
    "range",
    "red",
    "remove",
    "repeat",
    "return",
    "right",
    "sleep",
    "step",
    "times",
    "to_list",
    "to",
    "true",
    "True",
    "turn",
    "while",
    "white",
    "with",
    "yellow",
]


TOKEN_CONSTANT = "text"
