import {LANG_en} from './syntaxLang-en';
import {LANG_es} from './syntaxLang-es';
import {LANG_nl} from './syntaxLang-nl';
import {LANG_ar} from './syntaxLang-ar';
import {LANG_fr} from './syntaxLang-fr';

// A bunch of code expects a global "State" object. Set it here if not
// set yet.
if (!window.State) {
window.State = {};
}

// Defines a word with letters in any language
// TODO FH jan 2022: Now just does latin including accented and Arabic, needs to be
// improved for f.e. Hindi and Chinese

// extension of \w
const LETTER   = '[_0-9A-zÀ-ÿء-ي]';
const LETTER_WITHOUT_NUMBER   = '[_0-9A-zÀ-ÿء-ي]';

const SPACE    = " +";
const OPERATOR = '[\-\+\=\/\*]';
const LIST_SEPARATOR = '\,';


// replacement of \b (or rather \m and \M )
// https://www.regular-expressions.info/wordboundaries.html
const START_WORD = '(?<!' + LETTER + ')(?=' + LETTER + ')';
const END_WORD = '(?<=' + LETTER + ')(?!' + LETTER + ')';

const START_NUMBER = '(?<!' + LETTER_WITHOUT_NUMBER + ')(?=' + LETTER_WITHOUT_NUMBER + ')';
const END_NUMBER = '(?<=' + LETTER_WITHOUT_NUMBER + ')(?!' + LETTER_WITHOUT_NUMBER + ')';



// Contains the current keywords based on the current language
var currentLang: {
  _PRINT: string;
  _IS: string;
  _ASK: string;
  _ECHO: string;
  _FORWARD: string;
  _TURN: string;
  /*_LEFT : string;
  _RIGHT : string;*/
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
  default:
    currentLang = LANG_en;
    break;
}

// Lists of keywords by level
const COMMANDS = [
  [ // level 1 OK
    currentLang._FORWARD,
    currentLang._TURN,
    /*currentLang._LEFT,
    currentLang._RIGHT,*/
  ],
  [ // level 2 OK
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
  ],
  [ // level 3 OK
    currentLang._PRINT,
    currentLang._FORWARD,
    currentLang._TURN,
    currentLang._SLEEP,
    currentLang._AT,
    currentLang._RANDOM,
  ],
  [ // level 4 OK
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
  [ // level 5 OK
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
    currentLang._AND,
    currentLang._IF,
    currentLang._ELSE,
  ],
  [ // level 6 OK
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
    currentLang._AND,
    currentLang._IF,
    currentLang._ELSE,
  ],
  [ // level 6 OK
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
    currentLang._AND,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._TIMES,
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR,
    currentLang._OR
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR,
    currentLang._OR
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR,
    currentLang._OR,
    currentLang._WHILE
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR,
    currentLang._OR,
    currentLang._WHILE
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR,
    currentLang._OR,
    currentLang._WHILE,
    currentLang._ELIF
  ],
  [
    currentLang._PRINT,
    currentLang._ASK,
    currentLang._IS,
    currentLang._IN,
    currentLang._TURN,
    currentLang._FORWARD,
    currentLang._SLEEP,
    currentLang._ADD_LIST,
    currentLang._RANDOM,
    currentLang._AND,
    currentLang._REMOVE,
    currentLang._IF,
    currentLang._ELSE,
    currentLang._REPEAT,
    currentLang._FOR,
    currentLang._OR,
    currentLang._WHILE,
    currentLang._ELIF,
    currentLang._INPUT
  ],
]

// List of rules by level
const LEVELS = [
  {
    name: 'level1',
    rules: {
        "start" : [
          rule_ask(),
          rule_print(),
          rule_echo(),
          rule_keyword( 1),
        ]
    },
  },
  {
    name: 'level2',
    rules: {
        "start" : [
          rule_printWithVar(),
          rule_isAsk(),
          rule_is(),
          rule_keyword( 2),
        ]
    },
  },
  {
    name: 'level3',
    rules: {
        "start" : [
          rule_isAsk(),
          rule_addTo(),
          rule_removeFrom(),
          rule_keyword( 3),
          rule_listSeparator(),
        ]
    },
  },
  {
    name: 'level4',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword( 4),
          rule_listSeparator(),
        ]
    },
  },
  {
    name: 'level5',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword( 5),
          rule_listSeparator(),
        ]
    },
  },
  {
    name: 'level6',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword( 6),
          rule_listSeparator(),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level7',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword( 7),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level8and9',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword( 8),
          rule_operatorAndNumber(),
        ]
    },
  },

  {
    name: 'level10',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword(10),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level11and12',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword(11),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level13',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword(13),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level14',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword(14),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level15',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword(15),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level16',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword(16),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level17',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword(17),
          rule_operatorAndNumber(),
        ]
    },
  },
  {
    name: 'level18',
    rules: {
        "start" : [
          rule_string(),
          rule_keyword(18),
          rule_operatorAndNumber(),
        ]
    },
  },
];









/*
In the first levels, the strings are not yet well defined,
so we have to color them with respect to what is around,
so we use particular functions
*/

function rule_ask() {
  return {
    regex: "^(" + currentLang._ASK + ")(.*)$",
    token: ['keyword','constant.character'],
    next: 'start',
  };
}

function rule_print() {
  return {
    regex: "^(" + currentLang._PRINT + ")(.*)$",
    token: ['keyword','constant.character'],
    next: 'start',
  };
}

function rule_echo() {
  return {
    regex: "^(" + currentLang._ECHO + ")(.*)$",
    token: ['keyword','constant.character'],
    next: 'start',
  };
}


function rule_isAsk() {
  return {
    regex: "^("+LETTER+"*)(" + SPACE + ")(" + currentLang._IS +")(" + SPACE + ")(" + currentLang._ASK + ")(.*)$",
    token: ['text','text','keyword','text','keyword','constant.character'],
    next: 'start',
  };
}

function rule_is() {
  return {
    regex: "^("+LETTER+"*)(" + SPACE + ")(" + currentLang._IS +")(" + SPACE + ")(.*)$",
    token: ['text','text','keyword','text','constant.character'],
    next: 'start',
  };
}

function rule_printWithVar() {
  return {
    regex: "^(" + currentLang._PRINT + ")(.*)$",
    token: ['keyword','text'],
    next: 'start',
  };
}


function rule_addTo() {
  return {
    regex: "^(" + currentLang._ADD_LIST + ")(" + SPACE + ")(.*)(" + SPACE + ")(" + currentLang._TO + ")(" + SPACE + ")(.*)$",
    token: ['keyword','text','text','text','keyword','text','text'],
    next: 'start',
  };
}

function rule_removeFrom() {
  return {
    regex: "^(" + currentLang._REMOVE + ")(" + SPACE + ")(.*)(" + SPACE + ")(" + currentLang._FROM + ")(" + SPACE + ")(.*)$",
    token: ['keyword','text','text','text','keyword','text','text'],
    next: 'start',
  };
}


/*
In the following levels,
so what is not in quotes is code,
and any keyword in the code can be colored independently
of what is around it, so we use a general function
*/

function rule_keyword(level : number) {

  var rules = [];

  for (const command in COMMANDS[level-1]) {
    rules.push({
      regex: START_WORD + COMMANDS[level-1][command] + END_WORD,
      token: "keyword", 
    })
  }
  return rules;
}


function rule_string() {
  return {
    regex: /\'[^\']*\'/,
    token: 'constant.character',
    next: 'start',
  };
}


function rule_operatorAndNumber() {
  return [{
    regex: OPERATOR,
    token: 'keyword',
    next: 'start',
  },{
    regex: START_NUMBER + '[0-9]+' + END_NUMBER,
    token: 'variable', // it would be better to use `constant.numeric` but the color is the same as the text
    next: 'start',
  }];
}

function rule_listSeparator() {
  return {
    regex: LIST_SEPARATOR,
    token: 'keyword',
    next: 'start',
  };
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