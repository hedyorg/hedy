import {LANG_en} from './syntaxLang-en';
import {LANG_es} from './syntaxLang-es';
import {LANG_nl} from './syntaxLang-nl';
import {LANG_ar} from './syntaxLang-ar';
import {LANG_fr} from './syntaxLang-fr';
import {LANG_hi} from './syntaxLang-hi';
import {LANG_tr} from './syntaxLang-tr';
import {LANG_id} from './syntaxLang-id';
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

switch(window.State.keyword_language){
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
  case 'id':
    currentLang = LANG_id;
    break;
  case 'nb_NO':
    currentLang = LANG_nb_NO;
    break;
  default:
    currentLang = LANG_en;
    break;
}

const COMMANDS: {[key:number]: {[key:string]: string[] }  } = {
  4 :{
    "cat1" : [
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
    "cat2" : [","],
    "cat3" : [],
  },
  5 :{
    "cat1" : [
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
    "cat2" : [","],
    "cat3" : [],
  },
  6 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+"],
    "cat3" : [],
  },
  7 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+"],
    "cat3" : [],
  },
  8 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+"],
    "cat3" : [],
  },
  9 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+"],
    "cat3" : [],
  },
  10 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+"],
    "cat3" : [],
  },
  11 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+"],
    "cat3" : [],
  },
  12 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+"],
    "cat3" : [],
  },
  13 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+"],
    "cat3" : [],
  },
  14 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+","<",">","!"],
    "cat3" : [],
  },
  15 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+","<",">","!"],
    "cat3" : [],
  },
  16 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]"],
    "cat3" : [],
  },
  17 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]",":"],
    "cat3" : [],
  },
  18 :{
    "cat1" : [
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
    "cat2" : [",","-","=","/","\\*","\\+","<",">","!","\\[","\\]",":","\\(","\\)"],
    "cat3" : [],
  },
}


// List of rules by level
const LEVELS = [
  { name: 'level1' , rules: {"start" : [ rule_level1() ] },},
  { name: 'level2' , rules: {"start" : [ rule_level2() ] },},
  { name: 'level3' , rules: {"start" : [ rule_level3() ] },},
  { name: 'level4' , rules: {"start" : [ ruleALL(4) ] },},
  { name: 'level5' , rules: {"start" : [ ruleALL(5) ] },},
  { name: 'level6' , rules: {"start" : [ ruleALL(6, true) ] },},
  { name: 'level7' , rules: {"start" : [ ruleALL(7, true) ] },},
  { name: 'level8' , rules: {"start" : [ ruleALL(8, true) ] },},
  { name: 'level9' , rules: {"start" : [ ruleALL(9, true) ] },},
  { name: 'level10', rules: {"start" : [ ruleALL(10, true) ] },},
  { name: 'level11', rules: {"start" : [ ruleALL(11, true) ] },},
  { name: 'level12', rules: {"start" : [ ruleALL(12, true, true) ] },},
  { name: 'level13', rules: {"start" : [ ruleALL(13, true, true) ] },},
  { name: 'level14', rules: {"start" : [ ruleALL(14, true, true) ] },},
  { name: 'level15', rules: {"start" : [ ruleALL(15, true, true) ] },},
  { name: 'level16', rules: {"start" : [ ruleALL(16, true, true) ] },},
  { name: 'level17', rules: {"start" : [ ruleALL(17, true, true) ] },},
  { name: 'level18', rules: {"start" : [ ruleALL(18, true, true) ] },},

];



/*
In the first levels, the strings are not yet well defined,
so we have to color them with respect to what is around,
so we use particular functions
*/

function rule_level1() {
  return [{
    regex: START_LINE + "(" + currentLang._ASK + ")(.*)$",
    token: ['text','keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._PRINT + ")(.*)$",
    token: ['text','keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._ECHO + ")(.*)$",
    token: ['text','keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._FORWARD + ")( *)([0-9]*)( *)$",
    token: ['text','keyword','text','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._FORWARD + ")( *)$",
    token: ['text','keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._TURN + ")( *)(" + WORD + ")( *)$",
    token: ['text','keyword','text','keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._TURN + ")( *)$",
    token: ['text','keyword','text'],
    next: 'start',
  },{
    regex: /#.*$/,
    token: 'comment',
    next: 'start',
  },{
    regex: /\_\?\_/,
    token: 'invalid',
    next: 'start',
  },{
    regex: '(^| )(_)(?=( |$))',
    token: ['text','invalid','text'],
    next: 'start',
  } ];
}

function rule_level2() {
  return [{
    regex: START_LINE + "("+WORD+ ")(" + SPACE + ")(" + currentLang._IS + ")( *)(" + currentLang._ASK + ")( *)(.*)$",
    token: ["text",'text','text','keyword','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "("+WORD+ ")(" + SPACE + ")(" + currentLang._IS + ")( *)(.*)$",
    token: ["text",'text','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._PRINT + ")(.*)$",
    token: ["text",'keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._SLEEP + ")(.*)$",
    token: ["text",'keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._TURN + ")(.*)$",
    token: ["text",'keyword','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._FORWARD + ")(.*)$",
    token: ["text",'keyword','text'],
    next: 'start',
  },{
    regex: /#.*$/,
    token: 'comment',
    next: 'start',
  },{
    regex: /\_\?\_/,
    token: 'invalid',
    next: 'start',
  },{
    regex: '(^| )(_)(?=( |$))',
    token: ['text','invalid','text'],
    next: 'start',
  } ];
}

function rule_level3() {
  return [{
    regex: START_LINE + "("+WORD+ ")(" + SPACE + ")(" + currentLang._IS + ")( *)(" + currentLang._ASK + ")( *)(.*)$",
    token: ["text",'text','text','keyword','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "("+WORD+ ")(" + SPACE + ")(" + currentLang._IS + ")( *)(.*)$",
    token: ["text",'text','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._REMOVE + ")( *)(.*)(" + SPACE + ")(" + currentLang._FROM + ")( *)("+ WORD +")$",
    token: ["text",'keyword','text','text','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + "(" + currentLang._ADD_LIST + ")( *)(.*)(" + SPACE + ")(" + currentLang._TO_LIST + ")( *)("+ WORD +")$",
    token: ["text",'keyword','text','text','text','keyword','text','text'],
    next: 'start',
  },{
    regex: START_LINE + currentLang._PRINT ,
    token: ['keyword'],
    next: 'start',
  },{
    regex: START_LINE + currentLang._TURN ,
    token: ['keyword'],
    next: 'start',
  },{
    regex: START_LINE + currentLang._SLEEP ,
    token: ['keyword'],
    next: 'start',
  },{
    regex: START_LINE + currentLang._FORWARD ,
    token: ['keyword'],
    next: 'start',
  },{
    regex: START_WORD + currentLang._AT + SPACE + currentLang._RANDOM ,
    token: ['keyword','text','keyword'],
    next: 'start',
  },{
    regex: START_WORD + currentLang._AT ,
    token: ['keyword'],
    next: 'start',
  },{
    regex: '\,',
    token: ['keyword'],
    next: 'start',
  },{
    regex: /#.*$/,
    token: 'comment',
    next: 'start',
  },{
    regex: /\_\?\_/,
    token: 'invalid',
    next: 'start',
  },{
    regex: '(^| )(_)(?=( |$))',
    token: ['text','invalid','text'],
    next: 'start',
  } ];
}



/*
In the following levels,
so what is not in quotes is code,
and any keyword in the code can be colored independently
of what is around it, so we use a general function
*/



function ruleALL(level:number, number = false, with_decimal = false ) {
  var list_rules = [];

  /* Rule for comments : */
  list_rules.push( {
    regex: /#.*$/,
    token: 'comment',
    next: 'start',
  } );

  /* Rule for quoted string : */
  list_rules.push( {
    regex: /\"[^\"]*\"/,
    token: 'constant.character',
    next: 'start',
  } );
  list_rules.push( {
    regex: /\'[^\']*\'/,
    token: 'constant.character',
    next: 'start',
  } );

  /* Rule for blanks marks : */
  list_rules.push( {
    regex: /\_\?\_/,
    token: 'invalid',
    next: 'start',
  });
  list_rules.push( {
    regex: '(^| )(_)(?=( |$))',
    token: ['text','invalid','text'],
    next: 'start',
  } );



  /* Rules for numbers */
  if (number) {
    if (with_decimal) {
        list_rules.push({
          regex: START_WORD + '[0-9]*\\.?[0-9]+' + END_WORD,
          token: 'variable', // it would be better to use `constant.numeric` but the color is the same as the text
          next: 'start',
        });
      } else {
        list_rules.push({
          regex: START_WORD + '[0-9]+' + END_WORD,
          token: 'variable', // it would be better to use `constant.numeric` but the color is the same as the text
          next: 'start',
        });
      }
  }

  /* Rules for commands of cat1 */
  for (const command in COMMANDS[level]["cat1"]) {
    list_rules.push({
      regex: START_WORD + COMMANDS[level]["cat1"][command] + END_WORD,
      token: "keyword",
      next: "start", 
    });
  }

  /* Rules for commands of cat2 */
  for (const command in COMMANDS[level]["cat2"]) {
    list_rules.push({
      regex: COMMANDS[level]["cat2"][command],
      token: "keyword",
      next: "start", 
    });
  }

  /*console.log(list_rules);*/
  return list_rules;
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
