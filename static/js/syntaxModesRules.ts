import {LANG_en} from './syntaxLang-en';
import {LANG_es} from './syntaxLang-es';
import {LANG_nl} from './syntaxLang-nl';

// A bunch of code expects a global "State" object. Set it here if not
// set yet.
if (!window.State) {
window.State = {};
}

// Set this to true to use keywords from languages other than english
var localKeywordsEnable = true;

// Contains the current keywords based on the current language
var currentLang: { 
  _PRINT: string; 
  _IS: string; 
  _ASK: string; 
  _ECHO: string; 
  _FORWARD: string; 
  _TURN: string; 
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
if(localKeywordsEnable){
  switch(window.State.lang){
    case 'nl':
      currentLang = LANG_nl;
      break;
    case 'es':
      currentLang = LANG_es;
      break;
    default:
      currentLang = LANG_en;
      break;
  }
} else {
  currentLang = LANG_en;
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
      rule_turtle(),
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
    // Adds lists and 'at random'
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
    // Adds quoted text
    name: 'level3',
    rules: pipe(baseRules(),
      rule_turtle(),
      rule_printSpace('expression_eol'),
      rule_isAsk(),
      rule_is(),
    ),
  },
  {
    // Adds if/else
    name: 'level4',
    rules: pipe(baseRules(),
      rule_printSpace(),
      rule_isAsk(),
      rule_is(),
      rule_ifElseOneLine(),
      rule_expressions(),
    ),
  },
  {
    // Adds repeat
    name: 'level5',
    rules: pipe(baseRules(),
      rule_printSpace(),
      rule_isAsk(),
      rule_is(),
      rule_ifElseOneLine(),
      rule_expressions(),
      rule_repeat(),
    ),
  },
  {
    // Adds arithmetic
    name: 'level6',
    rules: pipe(baseRules(),
      rule_printSpace(),
      rule_isAsk(),
      rule_is(),
      rule_ifElseOneLine(),
      rule_expressions(),
      rule_repeat(),
      rule_arithmetic(),
    ),
  },
  {
    // Adds indented blocks -- no changes to highlighter necessary
    name: 'level7',
    rules: pipe(baseRules(),
      rule_printSpace(),
      rule_isAsk(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_repeat(),
      rule_arithmetic(),
    ),
  },
  {
    // Replaces 'repeat' with 'for'
    name: 'level8',
    rules: pipe(baseRules(),
      rule_printSpace(),
      rule_isAsk(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_for()
    ),
  },
  {
    // Replaces 'repeat' with 'for'
    name: 'level9and10',
    rules: pipe(baseRules(),
    rule_printSpace(),
    rule_isAsk(),
    rule_is(),
    rule_ifElse(),
    rule_expressions(),
    rule_arithmetic(),
    rule_forRange(),
    rule_for()
    ),
  },
  {
    // Nesting of 'for' loops (no changes necessary)
    name: 'level11',
    rules: pipe(baseRules(),
      rule_printSpace(),
      rule_isAsk(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRange(),
    ),
  },
  {
    // Adding fncall parens
    name: 'level12',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
    ),
  },
// ----------------------------------------------------------------
//  Everything below this line hasn't been done yet
// ----------------------------------------------------------------
  {
    name: 'level11',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
    ),
  },
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
      rule_forRangeParen(),
    ),
  },
  {
    name: 'level17',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
    ),
  },
  {
    name: 'level18and19',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
    ),
  },
  {
    name: 'level20',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
    ),
  },
  {
    name: 'level21',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
    ),
  },
  {
    name: 'level22',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
    ),
  },
  {
    name: 'level23',
    rules: pipe(baseRules(),
      rule_printParen(),
      rule_isInputParen(),
      rule_is(),
      rule_ifElse(),
      rule_expressions(),
      rule_arithmetic(),
      rule_forRangeParen(),
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
    regex: '(\\w+)( ' + currentLang._IS + ' ' + currentLang._ASK + ')',
    token: ['text', 'keyword'],
    next: next ?? 'expression_eol',
  });
}

/**
 * Add an 'is' rule, going to the indicated 'next' state (expression_eol if omitted)
 */
function rule_is(next?: string) {
  return recognize('start', {
    regex: '(\\w+)( ' + currentLang._IS + ' )',
    token: ['text', 'keyword'],
    next: next ?? 'expression_eol',
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

function rule_turtle() {
    return comp(
      recognize('start', {
        // Note: left and right are not yet keywords
        regex: currentLang._TURN + ' (left|right)?',
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
    regex: '(\\w+)( ' + currentLang._IS + ' ' + currentLang._INPUT + ')(\\()',
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
      regex: keywordWithSpace('((' + currentLang._IS + ')|(' + currentLang._IN + '))'),
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
      regex: keywordWithSpace('((' + currentLang._IS + ')|(' + currentLang._IN + '))'),
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
    regex: '(' + currentLang._REPEAT + ')( \\w+ )(' + currentLang._TIMES + ')',
    token: ['keyword', 'text', 'keyword'],
  });
}

function rule_for(){
  return recognize('start', {
    regex: '(' + currentLang._FOR + ' )(\\w+)( ' + currentLang._IN + ' )(\\w+)',
    token: ['keyword', 'text', 'keyword', 'text'],
  });
}

function rule_forRange() {
  return recognize('start', {
    regex: '(' + currentLang._FOR + ' )(\\w+)( ' + currentLang._IN + ' ' + currentLang._RANGE + ' )(\\w+)( to )(\\w+)',
    token: ['keyword', 'text', 'keyword', 'text', 'keyword', 'text'],
  });
}

function rule_forRangeParen() {
  return recognize('start', {
    regex: '(' + currentLang._FOR + ' )(\\w+)( ' + currentLang._IN + ' ' + currentLang._RANGE + ')(\\()([\\s\\w]+)(,)([\\s\\w]+)(\\))',
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
  return '\\b' + keyword + ' ';
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
