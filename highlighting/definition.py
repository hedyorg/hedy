# This file defines the special regexes

# list of symbols recognized as characters (with non-Latin characters)
CHARACTER = '0-9_A-Za-zÀ-ÿء-ي' 
WORD      = '([' + CHARACTER + "]+)"
SPACE     = "( +)"

START_LINE = '(^ *)'
START_WORD = '(^| )'
END_WORD   = '(?![' + CHARACTER + '])'

