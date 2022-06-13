# This file defines the special regexes

# list of symbols recognized as characters (with non-Latin characters)
CHARACTER = '0-9_A-Za-zÀ-ÿء-ي'

# definition of word
WORD      = '([' + CHARACTER + "]+)"
# space
SPACE     = "( +)"

# beginning and end of one line, including space 
START_LINE = '(^ *)'
END_LINE = '( *$)'

# beginning and end of words
START_WORD = '(^| )'
END_WORD   = '(?![' + CHARACTER + '])'

DIGIT = '[__DIGIT__]'

TRANSLATE_WORD = [
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
	"length"
]

def K(word, withoutGroup = False):
	if withoutGroup:
		if word in TRANSLATE_WORD:
			return "__"+word+"__"
		else:
			return word
	else:
		if word in TRANSLATE_WORD:
			return "(__"+word+"__)"
		else:
			return "(" + word + ")"
