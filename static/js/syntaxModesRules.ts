import {LANG_en} from './syntaxLang-en';
import {LANG_es} from './syntaxLang-es';
import {LANG_nl} from './syntaxLang-nl';
import {LANG_ar} from './syntaxLang-ar';
import {LANG_fr} from './syntaxLang-fr';
import {LANG_hi} from './syntaxLang-hi';
import {LANG_tr} from './syntaxLang-tr';
import {LANG_nb_NO} from './syntaxLang-nb_NO';


// A bunch of code expects a global "State" object. Set it here if not
// set yet.
if (!window.State) {
window.State = {};
}


// extension of \w
// A-z is different from A-Za-z (see an ascii table)
const CHARACTER = '0-9_A-Za-zÀ-ÿء-ي'; 
const WORD      = '[' + CHARACTER + "]+";
const SPACE     = " +";


// replacement of \b (or rather \m and \M )
// to detect the beginning and the end of a word without selecting them
// https://www.regular-expressions.info/wordboundaries.html
/*const START_WORD = '(?<![' + CHARACTER + '])(?=[' + CHARACTER + '])';*/
/*const END_WORD = '(?<=[' + CHARACTER + '])(?![' + CHARACTER + '])';*/

const START_LINE = '(^ *)';


const START_WORD = '(^| )';
const END_WORD = '(?![' + CHARACTER + '])';

// Contains the current keywords based on the current language
var currentLang: {
  _PRINT: string;
  _IS: string;
  _ASK: string;
  _ECHO: string;
  _FORWARD: string;
  _TURN: string;
  _LEFT: string;
  _RIGHT: string;
  _SLEEP: string;
  _ADD_LIST: string;
  _TO_LIST: string;
  _REMOVE: string;
  _FROM: string;
  _AT: string;
  _RANDOM: string;
  _IN: string;
  _IF: string;
  _ELSE: string;
  _AND: string;
  _REPEAT: string;
  _TIMES: string;
  _FOR: string;
  _RANGE: string;
  _TO: string;
  _STEP: string;
  _ELIF: string;
  _INPUT: string;
  _OR: string;
  _WHILE: string;
  _LENGTH: string;
};

switch(window.State.lang){
  case 'nl':
    currentLang = LANG_nl;
    break;
  case 'ar':
    currentLang = LANG_ar;
    break;
  case 'es':
    currentLang = LANG_es;
    break;
  case 'fr':
    currentLang = LANG_fr;
    break;
  case 'tr':
    currentLang = LANG_tr;
    break;
  case 'hi':
    currentLang = LANG_hi;
    break;
  case 'nb_NO':
    currentLang = LANG_nb_NO;
    break;
  default:
    currentLang = LANG_en;
    break;
}


// Lists of keywords by level
const COMMANDS: {[key:number]: string[]} = {
  4 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
  ],
  5 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
  ],
  6 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
  ],
  7 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._TIMES,
  ],
  8 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._TIMES,
  ],
  9 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._TIMES,
  ],
  10 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._TIMES,
    currentLang._FOR,
  ],
  11 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._FOR,
    currentLang._RANGE,
    currentLang._TO,
  ],
  12 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._FOR,
    currentLang._RANGE,
    currentLang._TO,
  ],
  13 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._FOR,
    currentLang._RANGE,
    currentLang._TO,
    currentLang._AND,
    currentLang._OR,
  ],
  14 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._FOR,
    currentLang._RANGE,
    currentLang._TO,
    currentLang._AND,
    currentLang._OR,
  ],
  15 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._FOR,
    currentLang._RANGE,
    currentLang._TO,
    currentLang._AND,
    currentLang._OR,
    currentLang._WHILE,
  ],
  16 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._FOR,
    currentLang._RANGE,
    currentLang._TO,
    currentLang._AND,
    currentLang._OR,
    currentLang._WHILE,
  ],
  17 :[
    currentLang._ASK,
    currentLang._IS,
    currentLang._PRINT,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._FOR,
    currentLang._RANGE,
    currentLang._TO,
    currentLang._AND,
    currentLang._OR,
    currentLang._WHILE,
    currentLang._ELIF,
  ],
  18 :[
    currentLang._IS,
    currentLang._PRINT,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
    currentLang._ADD_LIST,
    currentLang._TO_LIST,
    currentLang._REMOVE,
    currentLang._FROM,
    currentLang._IN,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._FOR,
    currentLang._RANGE,
    currentLang._TO,
    currentLang._AND,
    currentLang._OR,
    currentLang._WHILE,
    currentLang._ELIF,
    currentLang._INPUT,
  ],
}


// List of rules by level
const LEVELS = [
  {
    name: 'level1',
    rules: {
        "start" : [
          rule_blank(),
          rule_level1(),
        ]
    },
  },
  {
    name: 'level2',
    rules: {
        "start" : [
          rule_blank(),
          rule_level2(),
        ]
    },
  },
  {
    name: 'level3',
    rules: {
        "start" : [
          rule_blank(),
          rule_level3(),
        ]
    },
  },
  {
    name: 'level4',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(4),
          rule_symbols('\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level5',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(5),
          rule_symbols('\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level6',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(6),
          rule_symbols('\-\+\=\/\*\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level7',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(7),
          rule_symbols('\-\+\=\/\*\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level8',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(8),
          rule_symbols('\-\+\=\/\*\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level9',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(9),
          rule_symbols('\-\+\=\/\*\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level10',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(10),
          rule_symbols('\-\+\=\/\*\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level11',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(11),
          rule_symbols('\-\+\=\/\*\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level12',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(12),
          rule_symbols('\-\+\=\/\*\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level13',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(13),
          rule_symbols('\-\+\=\/\*\,'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level14',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(14),
          rule_symbols('\-\+\=\/\*\,\<\>\!'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level15',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(15),
          rule_symbols('\-\+\=\/\*\,\<\>\!'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level16',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(16),
          rule_symbols('\-\+\=\/\*\,\<\>\!\\[\\]'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level17',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(17),
          rule_symbols('\-\+\=\/\*\,\<\>\!\\[\\]\:'),
          rule_blank(),
        ]
    },
  },
  {
    name: 'level18',
    rules: {
        "start" : [
          rule_string(),
          rule_keywords(18),
          rule_symbols('\-\+\=\/\*\,\<\>\!\\[\\]\\(\\)'),
          rule_blank(),
        ]
    },
  },
];



/*
In the first levels, the strings are not yet well defined,
so we have to color them with respect to what is around,
so we use particular functions
*/

function rule_level1() {
  return [{
    regex: START_LINE + "(" + currentLang._ASK + ")(" + END_WORD + ")(.*)$",
    token: ['text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._PRINT + ")(" + END_WORD + ")(.*)$",
    token: ['text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._ECHO + ")(" + END_WORD + ")(.*)$",
    token: ['text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._FORWARD + ")(" + SPACE + ")([0-9]*)( *)$",
    token: ['text','keyword','text','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._FORWARD + ")( *)$",
    token: ['text','keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._TURN + ")(" + SPACE + ")(" + WORD + ")( *)$",
    token: ['text','keyword','text','keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._TURN + ")( *)$",
    token: ['text','keyword','text'],
    next: 'start',
  }];
}

function rule_level2() {
  return [{
    regex: START_LINE + "("+WORD+ ")(" + SPACE + ")(" + currentLang._IS + ")(" + SPACE + ")(" + currentLang._ASK + ")(" + SPACE + ")(.*)$",
    token: ["text",'text','text','keyword','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "("+WORD+ ")(" + SPACE + ")(" + currentLang._IS + ")(" + SPACE + ")(.*)$",
    token: ["text",'text','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._PRINT + ")(" + END_WORD + ")(.*)$",
    token: ["text",'keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._SLEEP + ")(" + END_WORD + ")(.*)$",
    token: ["text",'keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._TURN + ")(" + END_WORD + ")(.*)$",
    token: ["text",'keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._FORWARD + ")(" + END_WORD + ")(.*)$",
    token: ["text",'keyword','text','text'],
    next: 'start',
  }];
}

function rule_level3() {
  return [{
    regex: START_LINE + "("+WORD+ ")(" + SPACE + ")(" + currentLang._IS + ")(" + SPACE + ")(" + currentLang._ASK + ")(" + SPACE + ")(.*)$",
    token: ["text",'text','text','keyword','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "("+WORD+ ")(" + SPACE + ")(" + currentLang._IS + ")(" + SPACE + ")(.*)$",
    token: ["text",'text','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._REMOVE + ")(" + SPACE + ")(.*)(" + SPACE + ")(" + currentLang._FROM + ")(" + SPACE + ")("+ WORD +")$",
    token: ["text",'keyword','text','text','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._ADD_LIST + ")(" + SPACE + ")(.*)(" + SPACE + ")(" + currentLang._TO_LIST + ")(" + SPACE + ")("+ WORD +")$",
    token: ["text",'keyword','text','text','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + currentLang._PRINT + END_WORD,
    token: ['keyword'],
    next: 'start',
  },{
    regex: START_LINE + currentLang._TURN + END_WORD,
    token: ['keyword'],
    next: 'start',
  },{
    regex: START_LINE + currentLang._SLEEP + END_WORD,
    token: ['keyword'],
    next: 'start',
  },{
    regex: START_LINE + currentLang._FORWARD + END_WORD,
    token: ['keyword'],
    next: 'start',
  },{
    regex: START_WORD + currentLang._AT + SPACE + currentLang._RANDOM + END_WORD,
    token: ['keyword','text','keyword'],
    next: 'start',
  },{
    regex: START_WORD + currentLang._AT + END_WORD,
    token: ['keyword'],
    next: 'start',
  },{
    regex: '\,',
    token: ['keyword'],
    next: 'start',
  }];
}



/*
In the following levels,
so what is not in quotes is code,
and any keyword in the code can be colored independently
of what is around it, so we use a general function
*/

/* A symbol is different from a keyword, because a keyword must be surrounded by a beginning and an end.
While a symbol will be recognized independently of its surrounding */
function rule_keywords(level : number) {
  var rules = [];
  for (const command in COMMANDS[level]) {
    rules.push({
      regex: START_WORD + COMMANDS[level][command] + END_WORD,
      token: "keyword",
      next: "start", 
    })
  }
  return rules;
}

function rule_symbols(symbols : string) {
  return {
    regex: "[" + symbols + "]",
    token: "keyword", 
    next: "start",
  };
}

function rule_string() {
  return [{
    regex: /\"[^\"]*\"/,
    token: 'constant.character',
    next: 'start',
  },{
    regex: /\'[^\']*\'/,
    token: 'constant.character',
    next: 'start',
  }];
}



function rule_blank() {
  /* 'invalid' corresponds to a style predefined by monokai */
  return [{
    regex: /\_\?\_/,
    token: 'invalid',
    next: 'start',
  },{
    regex: '(^| )(_)(?=( |$))',
    token: ['text','invalid','text'],
    next: 'start',
  }];
}



// Only do this work if the 'define' function is actually available at runtime.
// If not, this script got included on a page that didn't include the Ace
// editor. No point in continuing if that is the case.
if ((window as any).define) {

  // Define the modes based on the level definitions above
  for (const level of LEVELS) {

    // This is a local definition of the file 'ace/mode/level1.js', etc.
    define('ace/mode/' + level.name, [], function(require, exports, _module) {
      var oop = require('ace/lib/oop');
      var TextMode = require('ace/mode/text').Mode;
      var TextHighlightRules = require('ace/mode/text_highlight_rules').TextHighlightRules;

      function ThisLevelHighlightRules(this: any) {
        this.$rules = level.rules;
        //console.log(this.$rules);
        this.normalizeRules();
      };
      oop.inherits(ThisLevelHighlightRules, TextHighlightRules);

      function Mode(this: any) {
        this.HighlightRules = ThisLevelHighlightRules;
      };
      oop.inherits(Mode, TextMode);

      exports.Mode = Mode;
    });
  }
}
