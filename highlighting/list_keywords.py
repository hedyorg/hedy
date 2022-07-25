from definition import *

#extra rules for ask
ask_after_is = {
    "regex": START_WORD + K("is") + SPACE + K("ask"),
    "token": ["text","keyword","text","keyword"]
}

ask_after_equal = {
    "regex": "(=)" + SPACE + K("ask"),
    "token": ["keyword","text","keyword"]
}



# This variable lists all the keywords in each level, i.e. everything that should be displayed in red (of type `keyword`)
# 
# There are several categories of keywords: 
# - SP_K_SP
#   These are the keywords that must be "alone" so neither preceded nor followed directly by a word 
# 
# - K
#   These are the keywords that are independent of the context (formerly the symbols).
#   In particular, even if they are between 2 words, the syntax highlighting will select them
# 
# - SP_K
#   This category of keywords allows you to have keywords that are not preceded
#   by another word, but that can be followed immediately by another word. (see the PR #2413)
# 
# - K_SP
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
    4 :{ # not used
        "SP_K_SP" : ["is","at","add","to_list","remove","from","color"],
        "K"       : [","],
        "SP_K"    : ["print","sleep","forward","turn","random"],
        "K_SP"    : [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "number"  : False,
        "number_with_decimal": False,
        "extra_rules" : [ask_after_is]
    },
    5 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","color"],
        "K"       : [","],
        "SP_K"    : ["print","sleep","forward","turn","random"],
        "K_SP"    : [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "number"  : False,
        "number_with_decimal": False,
        "extra_rules" : [ask_after_is]
    },
    6 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","color"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","sleep","forward","turn","random"],
        "K_SP"    : [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "number"  : True,
        "number_with_decimal": False,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    7 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","repeat","times","color"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","sleep","forward","turn","random"],
        "K_SP"    : [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "number"  : True,
        "number_with_decimal": False,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    8 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","repeat","color"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","sleep","forward","turn","random","else","times"],
        "K_SP"    : [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "number"  : True,
        "number_with_decimal": False,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    9 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","repeat","color"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","sleep","forward","turn","random","else","times"],
        "K_SP"    : [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "number"  : True,
        "number_with_decimal": False,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    10 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","repeat","for","color"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","sleep","forward","turn","random","else","times"],
        "K_SP"    : [],
        "constant": ["black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "white", "yellow"],
        "number"  : True,
        "number_with_decimal": False,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    11 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","repeat"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","sleep","random","else","times"],
        "K_SP"    : [],
        "constant": [],
        "number"  : True,
        "number_with_decimal": False,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    12 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","repeat"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","sleep","random","else","times"],
        "K_SP"    : [],
        "constant": [],
        "number"  : True,
        "number_with_decimal": True ,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    13 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","and","or","repeat"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","sleep","random","else","times"],
        "K_SP"    : [],
        "constant": [],
        "number"  : True,
        "number_with_decimal": True ,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    14 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","and","or","else","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!"],
        "SP_K"    : ["print","sleep","random","times"],
        "K_SP"    : [],
        "constant": [],
        "number"  : True,
        "number_with_decimal": True ,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    15 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","and","or","while","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!"],
        "SP_K"    : ["print","sleep","random","else","times"],
        "K_SP"    : [],
        "constant": [],
        "number"  : True,
        "number_with_decimal": True ,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    16 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","for","range","to","and","or","while","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]"],
        "SP_K"    : ["print","sleep","random","times"],
        "K_SP"    : [],
        "constant": [],
        "number"  : True,
        "number_with_decimal": True ,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    17 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","for","range","to","and","or","while","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]",":"],
        "SP_K"    : ["print","sleep","random","times"],
        "K_SP"    : ["elif"],
        "constant": [],
        "number"  : True,
        "number_with_decimal": True ,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
    18 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","for","range","to","and","or","while","input","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]",":","\\(","\\)"],
        "SP_K"    : ["print","sleep","random","times"],
        "K_SP"    : ["elif"],
        "constant": [],
        "number"  : True,
        "number_with_decimal": True,
        "extra_rules" : [ask_after_is,ask_after_equal]
    },
}
