
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
KEYWORDS = {
    4 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from"],
        "K"       : [","],
        "SP_K"    : ["print","ask","sleep","forward","turn","random"],
        "K_SP"    : [],
    },
    5 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else"],
        "K"       : [","],
        "SP_K"    : ["print","ask","sleep","forward","turn","random"],
        "K_SP"    : [],
    },
    6 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","ask","sleep","forward","turn","random"],
        "K_SP"    : [],
    },
    7 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","repeat","times"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","ask","sleep","forward","turn","random"],
        "K_SP"    : [],
    },
    8 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","repeat"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","ask","sleep","forward","turn","random","else","times"],
        "K_SP"    : [],
    },
    9 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","repeat"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","ask","sleep","forward","turn","random","else","times"],
        "K_SP"    : [],
    },
    10 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","repeat","for"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","ask","sleep","forward","turn","random","else","times"],
        "K_SP"    : [],
    },
    11 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","repeat"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","ask","sleep","random","else","times"],
        "K_SP"    : [],
    },
    12 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","repeat"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","ask","sleep","random","else","times"],
        "K_SP"    : [],
    },
    13 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","and","or","repeat"],
        "K"       : [",","-","=","/","\\*","\\+"],
        "SP_K"    : ["print","ask","sleep","random","else","times"],
        "K_SP"    : [],
    },
    14 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","and","or","else","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!"],
        "SP_K"    : ["print","ask","sleep","random","times"],
        "K_SP"    : [],
    },
    15 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","for","range","to","and","or","while","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!"],
        "SP_K"    : ["print","ask","sleep","random","else","times"],
        "K_SP"    : [],
    },
    16 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","for","range","to","and","or","while","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]"],
        "SP_K"    : ["print","ask","sleep","random","times"],
        "K_SP"    : [],
    },
    17 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","for","range","to","and","or","while","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]",":"],
        "SP_K"    : ["print","ask","sleep","random","times"],
        "K_SP"    : ["elif"],
    },
    18 :{
        "SP_K_SP" : ["is","at","add","to_list","remove","from","in","if","else","for","range","to","and","or","while","input","repeat"],
        "K"       : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]",":","\\(","\\)"],
        "SP_K"    : ["print","sleep","random","times"],
        "K_SP"    : ["elif"],
    },
}

# Rules concerning numbers (recognized or not, with or without decimals)
NUMBERS = {
    4  : {"number" : False , "number_with_decimal": False },
    5  : {"number" : False , "number_with_decimal": False },
    6  : {"number" : True  , "number_with_decimal": False },
    7  : {"number" : True  , "number_with_decimal": False },
    8  : {"number" : True  , "number_with_decimal": False },
    9  : {"number" : True  , "number_with_decimal": False },
    10 : {"number" : True  , "number_with_decimal": False },
    11 : {"number" : True  , "number_with_decimal": False },
    12 : {"number" : True  , "number_with_decimal": True  },
    13 : {"number" : True  , "number_with_decimal": True  },
    14 : {"number" : True  , "number_with_decimal": True  },
    15 : {"number" : True  , "number_with_decimal": True  },
    16 : {"number" : True  , "number_with_decimal": True  },
    17 : {"number" : True  , "number_with_decimal": True  },
    18 : {"number" : True  , "number_with_decimal": True  }
}