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
    "print",
    "ask",
    "echo",
    "forward",
    "turn",
    "color",
    "black",
    "blue",
    "brown",
    "gray",
    "green",
    "orange",
    "pink",
    "purple",
    "red",
    "white",
    "yellow",
    "right",
    "left",
    "is",
    "sleep",
    "add",
    "to_list",
    "remove",
    "from",
    "at",
    "random",
    "in",
    "if",
    "else",
    "and",
    "repeat",
    "times",
    "for",
    "range",
    "to",
    "step",
    "elif",
    "input",
    "or",
    "while",
    "length",
    "comma"
]


TOKEN_CONSTANT = "text"


def get_translated_keyword(word, withoutGroup=False):
    """ Function that allows to add double underscores around the keywords to be translated.
            The "__" are added before and after only if the keyword belongs to the list.

            - withoutGroup : bool, Add parentheses for make a group or not
    """
    if withoutGroup:
        if word in TRANSLATE_WORDS:
            return "__" + word + "__"
        else:
            return word
    else:
        if word in TRANSLATE_WORDS:
            return "(__" + word + "__)"
        else:
            return "(" + word + ")"
