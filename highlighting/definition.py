# This file defines the special regexes

# list of symbols recognized as characters (with non-Latin characters)
CHARACTER = '0-9_A-Za-zÀ-ÿء-ي'

# defintion of word
WORD      = '([' + CHARACTER + "]+)"
# space
SPACE     = "( +)"

# beginning and end of one line, including space 
START_LINE = '(^ *)'
END_LINE = '( *$)'

# beginning and end of words
START_WORD = '(^| )'
END_WORD   = '(?![' + CHARACTER + '])'

