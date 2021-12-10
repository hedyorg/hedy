import {LANG_en} from './syntaxLang-en';
import {LANG_nl} from './syntaxLang-nl';

// Set this to true to use keywords from languages other than english
var localKeywordsEnable = false;

// Sets the current keywords based on the current language
var currentLang;
if(localKeywordsEnable){
  switch(window.State.lang){
    case 'nl':
      currentLang = LANG_nl;
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
function baseRules(_AT: string, _RANDOM: string): Rules {
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
        regex: _AT + ' ' + _RANDOM,
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
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printSpace(currentLang._PRINT,'gobble'),
      rule_turtle(currentLang._TURN,currentLang._FORWARD),
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
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),

      rule_printSpace(currentLang._PRINT,'expression_eol'),
      rule_isAsk(currentLang._IS,currentLang._ASK,'gobble'),
      rule_is(currentLang._IS,'gobble'),
      rule_turtle(currentLang._TURN,currentLang._FORWARD),
      rule_sleep(currentLang._SLEEP),

    ),
  },
  {
    // Adds quoted text
    name: 'level3',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_turtle(currentLang._TURN,currentLang._FORWARD),
      rule_printSpace(currentLang._PRINT,'expression_eol'),
      rule_isAsk(currentLang._IS,currentLang._ASK),
      rule_is(currentLang._IS),
    ),
  },
  {
    // Adds if/else
    name: 'level4',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printSpace(currentLang._PRINT),
      rule_isAsk(currentLang._IS,currentLang._ASK),
      rule_is(currentLang._IS),
      rule_ifElseOneLine(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
    ),
  },
  {
    // Adds repeat
    name: 'level5',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printSpace(currentLang._PRINT),
      rule_isAsk(currentLang._IS,currentLang._ASK),
      rule_is(currentLang._IS),
      rule_ifElseOneLine(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_repeat(currentLang._REPEAT,currentLang._TIMES),
    ),
  },
  {
    // Adds arithmetic
    name: 'level6',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printSpace(currentLang._PRINT),
      rule_isAsk(currentLang._IS,currentLang._ASK),
      rule_is(currentLang._IS),
      rule_ifElseOneLine(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_repeat(currentLang._REPEAT,currentLang._TIMES),
      rule_arithmetic(),
    ),
  },
  {
    // Adds indented blocks -- no changes to highlighter necessary
    name: 'level7',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printSpace(currentLang._PRINT),
      rule_isAsk(currentLang._IS,currentLang._ASK),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_repeat(currentLang._REPEAT,currentLang._TIMES),
      rule_arithmetic(),
    ),
  },
  {
    // Replaces 'repeat' with 'for'
    name: 'level8',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printSpace(currentLang._PRINT),
      rule_isAsk(currentLang._IS,currentLang._ASK),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_for(currentLang._FOR,currentLang._IN)
    ),
  },
  {
    // Replaces 'repeat' with 'for'
    name: 'level9and10',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
    rule_printSpace(currentLang._PRINT),
    rule_isAsk(currentLang._IS,currentLang._ASK),
    rule_is(currentLang._IS),
    rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
    rule_expressions(currentLang._AT,currentLang._RANDOM),
    rule_arithmetic(),
    rule_forRange(currentLang._FOR,currentLang._IN,currentLang._RANGE),
    rule_for(currentLang._FOR,currentLang._IN)
    ),
  },
  {
    // Nesting of 'for' loops (no changes necessary)
    name: 'level11',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printSpace(currentLang._PRINT),
      rule_isAsk(currentLang._IS,currentLang._ASK),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRange(currentLang._FOR,currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    // Adding fncall parens
    name: 'level12',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR,currentLang._IN,currentLang._RANGE),
    ),
  },
// ----------------------------------------------------------------
//  Everything below this line hasn't been done yet
// ----------------------------------------------------------------
  {
    name: 'level11',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR,currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    name: 'level13',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR,currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    name: 'level14',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF, currentLang._ELSE, currentLang._IS, currentLang._IN),
      rule_expressions(currentLang._AT, currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR, currentLang._IN, currentLang._RANGE),
    ),
  },
  {
    name: 'level15',
    rules: pipe(baseRules(currentLang._AT, currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR, currentLang._IN, currentLang._RANGE),
    ),
  },
  {
    name: 'level16',
    rules: pipe(baseRules(currentLang._AT, currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR,currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    name: 'level17',
    rules: pipe(baseRules(currentLang._AT, currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS, currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR, currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    name: 'level18and19',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR, currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    name: 'level20',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR, currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    name: 'level21',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR, currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    name: 'level22',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR, currentLang._IN,currentLang._RANGE),
    ),
  },
  {
    name: 'level23',
    rules: pipe(baseRules(currentLang._AT,currentLang._RANDOM),
      rule_printParen(currentLang._PRINT),
      rule_isInputParen(currentLang._IS,currentLang._INPUT),
      rule_is(currentLang._IS),
      rule_ifElse(currentLang._IF,currentLang._ELSE,currentLang._IS,currentLang._IN),
      rule_expressions(currentLang._AT,currentLang._RANDOM),
      rule_arithmetic(),
      rule_forRangeParen(currentLang._FOR, currentLang._IN,currentLang._RANGE),
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
function rule_printSpace(_PRINT: string, next?: string) {
  return recognize('start', {
    regex: keywordWithSpace(_PRINT),
    token: 'keyword',
    next: next ?? 'start',
  });
}

/**
 * Add an 'is ask' rule, going to the indicated 'next' state (expression_eol if omitted)
 */
function rule_isAsk(_IS: string, _ASK: string, next?: string) {
  return recognize('start', {
    regex: '(\\w+)( ' + _IS + ' ' + _ASK + ')',
    token: ['text', 'keyword'],
    next: next ?? 'expression_eol',
  });
}

/**
 * Add an 'is' rule, going to the indicated 'next' state (expression_eol if omitted)
 */
function rule_is(_IS: string, next?: string) {
  return recognize('start', {
    regex: '(\\w+)( ' + _IS + ' )',
    token: ['text', 'keyword'],
    next: next ?? 'expression_eol',
  });
}

/**
 * Add a 'print' rule with brackets
 */
function rule_printParen(_PRINT: string) {
  return recognize('start', {
    regex: '(' + _PRINT + ')(\\()',
    token: ['keyword', 'paren.lparen'],
    next: 'start'
  });
}

function rule_turtle(_TURN: string, _FORWARD: string) {
    return comp(
      recognize('start', {
        // Note: left and right are not yet keywords
        regex: _TURN + ' (left|right)?',
        token: 'keyword',
        next: 'start',
      }),
      recognize('start', {
        regex: _FORWARD,
        token: 'keyword',
        next: 'start',
      })
    )
}

function rule_sleep(_SLEEP: string) {
  return recognize('start', {
      regex: _SLEEP,
      token: 'keyword',
      next: 'start',
    }
  )
}

/**
 * Add an 'is input' rule with brackets
 */
function rule_isInputParen(_IS: string, _INPUT: string) {
  return recognize('start', {
    regex: '(\\w+)( ' + _IS + ' ' + _INPUT + ')(\\()',
    token: ['text', 'keyword', 'paren.lparen'],
    next: 'start'
  });
}

/**
 * Recognize expressions as part of the 'start' state
 */
function rule_expressions(_AT: string, _RANDOM: string) {
  return comp(
    recognize('start', {
      regex: "'[^']*'",
      token: 'constant.character',
    }),
    recognize('start', {
      regex: _AT + _RANDOM,
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
function rule_ifElseOneLine(_IF: string, _ELSE: string, _IS: string, _IN: string) {
  return comp(
    recognize('start', {
      regex: keywordWithSpace(_IF),
      token: 'keyword',
      next: 'condition',
    }),
    recognize('start', {
      regex: keywordWithSpace(_ELSE),
      token: 'keyword',
    }),
    recognize('condition', {
      regex: keywordWithSpace('((' + _IS + ')|(' + _IN + '))'),
      token: 'keyword',
      next: 'start',
    }),
  );
}

function rule_ifElse(_IF: string, _ELSE: string, _IS: string, _IN: string) {
  return comp(
    recognize('start', {
      regex: keywordWithSpace(_IF),
      token: 'keyword',
      next: 'condition',
    }),
    recognize('start', {
      regex: '\\b' + _ELSE + '\\b',
      token: 'keyword',
    }),
    recognize('condition', {
      regex: keywordWithSpace('((' + _IS + ')|(' + _IN + '))'),
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
function rule_repeat(_REPEAT: string, _TIMES: string) {
  return recognize('start', {
    regex: '(' + _REPEAT + ')( \\w+ )(' + _TIMES + ')',
    token: ['keyword', 'text', 'keyword'],
  });
}

function rule_for(_FOR: string, _IN: string){
  return recognize('start', {
    regex: '(' + _FOR + ' )(\\w+)( ' + _IN + ' )(\\w+)',
    token: ['keyword', 'text', 'keyword', 'text'],
  });
}

function rule_forRange(_FOR: string, _IN: string, _RANGE: string) {
  return recognize('start', {
    regex: '(' + _FOR + ' )(\\w+)( ' + _IN + ' ' + _RANGE + ' )(\\w+)( to )(\\w+)',
    token: ['keyword', 'text', 'keyword', 'text', 'keyword', 'text'],
  });
}

function rule_forRangeParen(_FOR: string, _IN: string, _RANGE: string) {
  return recognize('start', {
    regex: '(' + _FOR + ' )(\\w+)( ' + _IN + ' ' + _RANGE + ')(\\()([\\s\\w]+)(,)([\\s\\w]+)(\\))',
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
