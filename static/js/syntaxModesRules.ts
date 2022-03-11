import {LANG_en} from './syntaxLang-en';
import {LANG_es} from './syntaxLang-es';
import {LANG_nl} from './syntaxLang-nl';
import {LANG_ar} from './syntaxLang-ar';
import {LANG_fr} from './syntaxLang-fr';
import {LANG_hi} from './syntaxLang-hi';

// A bunch of code expects a global "State" object. Set it here if not
// set yet.
if (!window.State) {
window.State = {};
}

// Defines a word with letters in any language
// TODO FH jan 2022: Now just does latin including accented and Arabic, needs to be
// improved for f.e. Hindi and Chinese
var word = '[0-9A-zÀ-ÿء-ي]+';


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
  case 'hi':
    currentLang = LANG_hi;
    break;
  default:
    currentLang = LANG_en;
    break;
}

interface Rule {
  readonly regex: string;
  readonly token: string | string[];
  readonly next?: string;
}

type Rules = Record<string, Rule[]>;

// Basic highlighter rules we can use in most levels
// - Highlighters always begin in the 'start' state, and see line by line (no newlines!)
// - We try to recognize as many commands and tokens as possible in 'start', only deviating
//   to another state to avoid highlighting something.
// - 'expression_eol' is the state to contain arbitrary values that will always eat the rest of the line
// - 'gobble' is the state that will eat whatever is left in the line and go back to 'start'
function baseRules(): Rules {
  return {
    // gobble is a state in which we can read anything (.*), used after print
    gobble: [
      {
        regex: '.*',
        token: 'text',
        next: 'start',
      }
    ],

    // this function creates two rules, one to recognize strings and at random within a line (staying in the same state)
    // and one where it is recognized at the end of the line (going back to start)
    expression_eol: finishLine([
      {
        regex: "'[^']*'",
        token: 'constant.character',
      },
      {
        regex: currentLang._AT + ' ' + currentLang._RANDOM,
        token: 'keyword'
      },
      {
        regex: '$', // $ matches with end of line
        token: 'text',
      },
    ]),
  };
}

const LEVELS = [
  {
    name: 'level1',
    rules: pipe(baseRules(),
      rule_printSpace('gobble'),
      rule_turtle_left_right(),
      recognize('start', {
        regex: keywordWithSpace(currentLang._ECHO),
        token: 'keyword',
        next: 'gobble',
      }),
      recognize('start', {
        regex: keywordWithSpace(currentLang._ASK),
        token: 'keyword',
        next: 'gobble',
      }),
    ),
  },
  {
    // Adds variables
    name: 'level2',
    rules: pipe(baseRules(),
      rule_printSpace('expression_eol'),
      rule_isAsk('gobble'),
      rule_is('gobble'),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    // Adds lists and 'at random'
    // TODO (FH, jan 2022) add "add" and "remove" for lists
    name: 'level3',
    rules: pipe(baseRules(),
      rule_printSpace('expression_eol'),
      rule_isAsk('gobble'),
      rule_is('gobble'),
      rule_turtle(),
      rule_sleep(),
      rule_listManipulation(),
    ),
  },
  {
    // Adds quoted text
    name: 'level4',
    rules: pipe(baseRules(),
      rule_turtle(),
      rule_printSpace('expression_eol'),
      rule_isAsk(),
      rule_is(),
      rule_listManipulation(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    // Adds if
    name: 'level5',
    rules: pipe(baseRules(),
      rule_printSpace('expression_eol'),
      rule_isAsk(),
      rule_is(),
      rule_listManipulation(),
      rule_ifElseOneLine(),
      rule_expressions(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    // Adds arithmetic
    name: 'level6',
    rules: pipe(baseRules(),
      rule_printSpace('expression_eol'),
      rule_isAsk(),
      rule_listManipulation(),
      rule_is(),
      rule_ifElseOneLine(),
      rule_expressions(),
      rule_arithmetic(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
  // level 7 adds repeat x times
    name: 'level7',
    rules: pipe(baseRules(),
      rule_printSpace('expression_eol'),
      rule_isAsk(),
      rule_listManipulation(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_repeat(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    // Level 8 adds indented block
    // Level 9 adds doubly indented blocks
    name: 'level8and9',
    rules: pipe(baseRules(),
      rule_printSpace('expression_eol'),
      rule_isAsk(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_repeat(),
      rule_listManipulation(),
      rule_turtle(),
      rule_sleep(),
    ),
  },

  {
    // Replaces 'repeat' with 'for' over a list (for a in animals)
    name: 'level10',
    rules: pipe(baseRules(),
      rule_printSpace(),
      rule_isAsk(),
      rule_listManipulation(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_for(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    // Allows for with range
    name: 'level11and12',
    rules: pipe(baseRules(),
      rule_printSpace('expression_eol'),
      rule_isAsk(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_for(),
      rule_forRange(),
      rule_turtle(),
      rule_listManipulation(),
      rule_sleep(),
    ),
  },
// ----------------------------------------------------------------
//  Everything below this line hasn't been done yet
// ----------------------------------------------------------------
  {
    name: 'level13',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
      rule_listManipulation(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    name: 'level14',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
      rule_listManipulation(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    name: 'level15',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
      rule_turtle(),
      rule_listManipulation(),
      rule_sleep(),
    ),
  },
  {
    name: 'level16',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_listManipulation(),
      rule_forRangeParen(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    name: 'level17',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_listManipulation(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
  {
    name: 'level18',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_listManipulation(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
      rule_turtle(),
      rule_sleep(),
    ),
  },
];

/**
 * From a list of rules, duplicate all rules
 *
 * - 1 is the rule that's given
 * - 2 is the same rule, adding an '$' which returns to the 'start' state
 *
 * 2nd one comes first to have the right precedence.
 */
function finishLine(rules: Rule[]) {
  const ret = [];
  for (const rule of rules) {
    if (rule.regex) {
      ret.push({
        regex: rule.regex + '$',
        token: rule.token,
        next: 'start',
      });
    }
    ret.push(rule);
  }
  return ret;
}

/**
 * Add a single rule, or multiple rules, to a given state, or multiple states
 *
 * Examples:
 *
 * - recognize('start', { regex, token, next })
 * - recognize(['start', 'expression'], { regex, token, next })
 * - recognize('start', [{ ... }, {...}])
 */
function recognize(stateOrStates: string | string[], ruleOrRules: Rule | Rule[]) {
  return (rules: Rules) => {
    if (!Array.isArray(stateOrStates)) {
      stateOrStates = [stateOrStates];
    }

    for (const state of stateOrStates) {
      if (!rules[state]) {
        rules[state] = [];
      }
      if (Array.isArray(ruleOrRules)) {
        rules[state].push(...ruleOrRules);
      } else {
        rules[state].push(ruleOrRules);
      }
    }

    return rules;
  };
}

/**
 * comp(f1, f2, f3, ...)
 *
 * Returns f1 ○ f2 ○ f3 ○ ...
 */
function comp(...fns: Array<(x: any) => any>) {
  return (val: any) => {
    for (const fn of fns) {
      val = fn(val);
    }
    return val;
  };
}

/**
 * pipe(X, f1, f2, f3, ...)
 *
 * Returns ...(f3(f2(f1(X)))
 *
 * (Same as X |> f1 |> f2 |> f3 |> ...)
 */
function pipe(val: any, ...fns: Array<(x: any) => any>) {
  return comp(...fns)(val);
}

/**
 * Add a 'print' rule, going to the indicated 'next' state (start if omitted)
 */
function rule_printSpace(next?: string) {
  return recognize('start', {
    regex: keywordWithSpace(currentLang._PRINT),
    token: 'keyword',
    next: next ?? 'start',
  });
}

/**
 * Add an 'is ask' rule, going to the indicated 'next' state (expression_eol if omitted)
 */
function rule_isAsk(next?: string) {
  return recognize('start', {
    regex: '('+ word + ')( ' + currentLang._IS + ' ' + currentLang._ASK + ')',
    token: ['text', 'keyword'],
    next: next ?? 'expression_eol',
  });
}

/**
 * Add an 'is' rule, going to the indicated 'next' state (expression_eol if omitted)
 */
function rule_is(next?: string) {
  return recognize('start', {
    regex: '('+ word + ')( ' + currentLang._IS + ' )',
    token: ['text', 'keyword'],
    next: next ?? 'start',
  });
}

/**
 * Add a 'print' rule with brackets
 */
function rule_printParen() {
  return recognize('start', {
    regex: '(' + currentLang._PRINT + ')(\\()',
    token: ['keyword', 'paren.lparen'],
    next: 'start'
  });
}

function rule_turtle_left_right() {
    return comp(
      recognize('start', {
        regex: currentLang._TURN + ' (' + currentLang._LEFT + '|' + currentLang._RIGHT + ')?',
        token: 'keyword',
        next: 'start',
      }),
      recognize('start', {
        regex: currentLang._FORWARD,
        token: 'keyword',
        next: 'start',
      })
    )
}

function rule_turtle() {
    return comp(
      recognize('start', {
        regex: currentLang._TURN,
        token: 'keyword',
        next: 'start',
      }),
      recognize('start', {
        regex: currentLang._FORWARD,
        token: 'keyword',
        next: 'start',
      })
    )
}


function rule_sleep() {
  return recognize('start', {
      regex: currentLang._SLEEP,
      token: 'keyword',
      next: 'start',
    }
  )
}

/**
 * Add an 'is input' rule with brackets
 */
function rule_isInputParen() {
  return recognize('start', {
    regex: '('+ word + ')( ' + currentLang._IS + ' ' + currentLang._INPUT + ')(\\()',
    token: ['text', 'keyword', 'paren.lparen'],
    next: 'start'
  });
}

/**
 * Recognize expressions as part of the 'start' state
 */
function rule_expressions() {
  return comp(
    recognize('start', {
      regex: "'[^']*'",
      token: 'constant.character',
    }),
    recognize('start', {
      regex: currentLang._AT + currentLang._RANDOM,
      token: 'keyword'
    }),
    recognize('start', {
      regex: '[, ]+',
      token: 'punctuation.operator',
    }),
  );
}

function rule_listManipulation() {
  return comp(
    recognize('start', {
      regex: "^(" + currentLang._ADD_LIST + ")( )(.*)( )(" + currentLang._TO + ")( )(.*)$",
      token: ['keyword','text','text','text','keyword','text','text'],
      next: 'start',
    }),
    recognize('start', {
      regex: "^(" + currentLang._REMOVE + ")( )(.*)( )(" + currentLang._FROM + ")( )(.*)$",
      token: ['keyword','text','text','text','keyword','text','text'],
      next: 'start',
    }));
}


/**
 * Add highlighting for if/else, also add a condition
 */
function rule_ifElseOneLine() {
  return comp(
    recognize('start', {
      regex: keywordWithSpace(currentLang._IF),
      token: 'keyword',
      next: 'condition',
    }),
    recognize('start', {
      regex: keywordWithSpace(currentLang._ELSE),
      token: 'keyword',
    }),
    recognize('condition', {
      regex: keywordWithSpace(currentLang._IS),
      token: 'keyword',
      next: 'start',
    }),
    recognize('condition', {
      regex: keywordWithSpace(currentLang._IN),
      token: 'keyword',
      next: 'start',
    }),
  );
}

function rule_ifElse() {
  return comp(
    recognize('start', {
      regex: keywordWithSpace(currentLang._IF),
      token: 'keyword',
      next: 'condition',
    }),
    recognize('start', {
      regex: '\\b' + currentLang._ELSE + '\\b',
      token: 'keyword',
    }),
    recognize('condition', {
      regex: keywordWithSpace(currentLang._IS + '|' + currentLang._IN),
      token: 'keyword',
      next: 'start',
    }),
  );
}

/**
 * Add numbers and arithmetic
 */
function rule_arithmetic() {
  return recognize(['start', 'expression_eol'], [
    {
      regex: ' \\* ',
      token: 'keyword',
    },
    {
      regex: ' \\+ ',
      token: 'keyword',
    },
    {
      regex: ' \\- ',
      token: 'keyword',
    },
  ]);
}

/**
 * Add highlighting for repeat
 */
function rule_repeat() {
  return recognize('start', {
    regex: '(' + currentLang._REPEAT + ')( '+ word +' )(' + currentLang._TIMES + ')',
    token: ['keyword', 'text', 'keyword'],
  });
}

function rule_for(){
  return recognize('start', {
    regex: '(' + currentLang._FOR + ' )('+word+')( ' + currentLang._IN + ' )('+word+')',
    token: ['keyword', 'text', 'keyword', 'text'],
  });
}

function rule_forRange() {
  return recognize('start', {
    regex: '(' + currentLang._FOR + ' )('+word+')( ' + currentLang._IN + ' ' + currentLang._RANGE + ' )('+word+')( to )('+word+')',
    token: ['keyword', 'text', 'keyword', 'text', 'keyword', 'text'],
  });
}

function rule_forRangeParen() {
  return recognize('start', {
    regex: '(' + currentLang._FOR + ' )('+word+')( ' + currentLang._IN + ' ' + currentLang._RANGE + ')(\\(\\s*)('+word+')(\\s*,\\s*)('+word+')(\\s*\\))',
    token: ['keyword', 'text', 'keyword', 'paren.lparen', 'text', 'punctuation.operator', 'text', 'paren.rparen'],
  });
}

/**
 * Wrap a keyword in word-boundary markers for use in the tokenizer regexes
 *
 * Use this to only recognize a word if it's a complete word by itself (and
 * not accidentally a part of a larger word).
 *
 * The keyword must be followed by space.
 */
function keywordWithSpace(keyword: string) {
  // We used to use \b here to match a "word boundary". However,
  // "word boundary" seems to be defined rather narrowly, and for whatever
  // reason does not work properly with non-ASCII languages.
  //
  // Then, we tried negative lookbehind (?<!\p{L}), but lookbehinds are not
  // really properly supported outside of Chrome.
  //
  // Instead, we'll look for start-of-string OR a whitespace character. This
  // means users now MUST type spaces in order to get syntax highlighting,
  // whereas they might used to be able to get away with typing it directly
  // after a parenthesis or '+' symbol or something... but since the symbol
  // would be highlighted as well that's not desirable, and most of these commands
  // for the start of the line anyway.

  //FH Jan: loosened this to s+ allow for indented rules
  return '(?:^|\\s+)' + keyword + ' ';
}




/**
 * Modify the given ruleset, replacing literal spaces with "one or more spaces"
 */
function loosenRules(rules: Rules) {
  for (const ruleSets of Object.values(rules)) {
    for (const rule of ruleSets) {
      if (rule.regex && !(rule as any)._loosened) {
        (rule as any).regex = rule.regex.replace(/ /g, ' +');
        (rule as any)._loosened = true;
      }
    }
  }
  return rules;
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
        this.$rules = loosenRules(level.rules);
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