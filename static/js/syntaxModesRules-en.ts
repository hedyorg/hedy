import * as syntaxRules from './syntaxRules';
var _PRINT='print';
var _ASK='ask'; 
var _ECHO='echo';
var _FORWARD='forward';
var _TURN='turn'; 
var _IS='is';
var _SLEEP='sleep';
var _ADD_LIST='add';
var _TO_LIST='to';
var _REMOVE='remove';
var _FROM='from';
var _AT='at'; 
var _RANDOM='random'; 
var _IN='in'; 
var _IF='if';
var _ELSE='else'; 
var _AND='and'; 
var _REPEAT='repeat';
var _TIMES='times'; 
var _FOR='for'; 
var _RANGE='range';
var _TO='to';
var _STEP='step';
var _ELIF='elif';
var _INPUT='input';
var _OR='or';
var _WHILE='while';

const LEVELS = [
  {
    name: 'level1',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printSpace(_PRINT,'gobble'),
      syntaxRules.rule_turtle(_TURN,_FORWARD),
      syntaxRules.recognize('start', {
        regex: syntaxRules.keywordWithSpace(_ECHO),
        token: 'keyword',
        next: 'gobble',
      }),
      syntaxRules.recognize('start', {
        regex: syntaxRules.keywordWithSpace(_ASK),
        token: 'keyword',
        next: 'gobble',
      }),
    ),
  },
  {
    // Adds lists and 'at random'
    name: 'level2',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),

      syntaxRules.rule_printSpace(_PRINT,'expression_eol'),
      syntaxRules.rule_isAsk(_IS,_ASK,'gobble'),
      syntaxRules.rule_is(_IS,'gobble'),
      syntaxRules.rule_turtle(_TURN,_FORWARD),
      syntaxRules.rule_sleep(_SLEEP),

    ),
  },
  {
    // Adds quoted text
    name: 'level3',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_turtle(_TURN,_FORWARD),
      syntaxRules.rule_printSpace('expression_eol'),
      syntaxRules.rule_isAsk(_IS,_ASK),
      syntaxRules.rule_is(_IS),
    ),
  },
  {
    // Adds if/else
    name: 'level4',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printSpace(_PRINT),
      syntaxRules.rule_isAsk(_IS,_ASK),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElseOneLine(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
    ),
  },
  {
    // Adds repeat
    name: 'level5',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printSpace(_PRINT),
      syntaxRules.rule_isAsk(_IS,_ASK),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElseOneLine(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_repeat(_REPEAT,_TIMES),
    ),
  },
  {
    // Adds arithmetic
    name: 'level6',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printSpace(_PRINT),
      syntaxRules.rule_isAsk(_IS,_ASK),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElseOneLine(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_repeat(_REPEAT,_TIMES),
      syntaxRules.rule_arithmetic(),
    ),
  },
  {
    // Adds indented blocks -- no changes to highlighter necessary
    name: 'level7',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printSpace(_PRINT),
      syntaxRules.rule_isAsk(_IS,_ASK),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_repeat(_REPEAT,_TIMES),
      syntaxRules.rule_arithmetic(),
    ),
  },
  {
    // Replaces 'repeat' with 'for'
    name: 'level8',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printSpace(_PRINT),
      syntaxRules.rule_isAsk(_IS,_ASK),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_for(_FOR,_IN)
    ),
  },
  {
    // Replaces 'repeat' with 'for'
    name: 'level9and10',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
    syntaxRules.rule_printSpace(_PRINT),
    syntaxRules.rule_isAsk(_IS,_ASK),
    syntaxRules.rule_is(_IS),
    syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
    syntaxRules.rule_expressions(_AT,_RANDOM),
    syntaxRules.rule_arithmetic(),
    syntaxRules.rule_forRange(_FOR,_IN,_RANGE),
    syntaxRules.rule_for(_FOR,_IN)
    ),
  },
  {
    // Nesting of 'for' loops (no changes necessary)
    name: 'level11',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printSpace(_PRINT),
      syntaxRules.rule_isAsk(_IS,_ASK),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRange(_FOR,_IN,_RANGE),
    ),
  },
  {
    // Adding fncall parens
    name: 'level12',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
// ----------------------------------------------------------------
//  Everything below this line hasn't been done yet
// ----------------------------------------------------------------
  {
    name: 'level11',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level13',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level14',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level15',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level16',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level17',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level18and19',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level20',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level21',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level22',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
  {
    name: 'level23',
    rules: syntaxRules.pipe(syntaxRules.baseRules(_AT,_RANDOM),
      syntaxRules.rule_printParen(_PRINT),
      syntaxRules.rule_isInputParen(_IS,_INPUT),
      syntaxRules.rule_is(_IS),
      syntaxRules.rule_ifElse(_IF,_ELSE,_IS,_IN),
      syntaxRules.rule_expressions(_AT,_RANDOM),
      syntaxRules.rule_arithmetic(),
      syntaxRules.rule_forRangeParen(_FOR, _IN,_RANGE),
    ),
  },
];
  
/**
 * Modify the given ruleset, replacing literal spaces with "one or more spaces"
 */
function loosenRules(rules: syntaxRules.Rules) {
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
    define('ace/mode/' + level.name + 'en', [], function(require, exports, _module) {
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
