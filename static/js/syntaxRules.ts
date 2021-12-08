export interface Rule {
    readonly regex: string;
    readonly token: string | string[];
    readonly next?: string;
  }
  
  export type Rules = Record<string, Rule[]>;
  
  // Basic highlighter rules we can use in most levels
  // - Highlighters always begin in the 'start' state, and see line by line (no newlines!)
  // - We try to recognize as many commands and tokens as possible in 'start', only deviating
  //   to another state to avoid highlighting something.
  // - 'expression_eol' is the state to contain arbitrary values that will always eat the rest of the line
  // - 'gobble' is the state that will eat whatever is left in the line and go back to 'start'
  export function baseRules(_AT: string, _RANDOM: string): Rules {
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

  /**
   * From a list of rules, duplicate all rules
   *
   * - 1 is the rule that's given
   * - 2 is the same rule, adding an '$' which returns to the 'start' state
   *
   * 2nd one comes first to have the right precedence.
   */
  export function finishLine(rules: Rule[]) {
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
  export function recognize(stateOrStates: string | string[], ruleOrRules: Rule | Rule[]) {
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
  export function comp(...fns: Array<(x: any) => any>) {
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
  export function pipe(val: any, ...fns: Array<(x: any) => any>) {
    return comp(...fns)(val);
  }
  
  /**
   * Add a 'print' rule, going to the indicated 'next' state (start if omitted)
   */
  export function rule_printSpace(_PRINT: string, next?: string) {
    return recognize('start', {
      regex: keywordWithSpace(_PRINT),
      token: 'keyword',
      next: next ?? 'start',
    });
  }
  
  /**
   * Add an 'is ask' rule, going to the indicated 'next' state (expression_eol if omitted)
   */
  export function rule_isAsk(_IS: string, _ASK: string, next?: string) {
    return recognize('start', {
      regex: '(\\w+)( ' + _IS + ' ' + _ASK + ')',
      token: ['text', 'keyword'],
      next: next ?? 'expression_eol',
    });
  }
  
  /**
   * Add an 'is' rule, going to the indicated 'next' state (expression_eol if omitted)
   */
  export function rule_is(_IS: string, next?: string) {
    return recognize('start', {
      regex: '(\\w+)( ' + _IS + ' )',
      token: ['text', 'keyword'],
      next: next ?? 'expression_eol',
    });
  }
  
  /**
   * Add a 'print' rule with brackets
   */
  export function rule_printParen(_PRINT: string) {
    return recognize('start', {
      regex: '(' + _PRINT + ')(\\()',
      token: ['keyword', 'paren.lparen'],
      next: 'start'
    });
  }
  
  export function rule_turtle(_TURN: string, _FORWARD: string) {
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
  
  export function rule_sleep(_SLEEP: string) {
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
  export function rule_isInputParen(_IS: string, _INPUT: string) {
    return recognize('start', {
      regex: '(\\w+)( ' + _IS + ' ' + _INPUT + ')(\\()',
      token: ['text', 'keyword', 'paren.lparen'],
      next: 'start'
    });
  }
  
  /**
   * Recognize expressions as part of the 'start' state
   */
  export function rule_expressions(_AT: string, _RANDOM: string) {
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
  export function rule_ifElseOneLine(_IF: string, _ELSE: string, _IS: string, _IN: string) {
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
  
  export function rule_ifElse(_IF: string, _ELSE: string, _IS: string, _IN: string) {
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
  export function rule_arithmetic() {
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
  export function rule_repeat(_REPEAT: string, _TIMES: string) {
    return recognize('start', {
      regex: '(' + _REPEAT + ')( \\w+ )(' + _TIMES + ')',
      token: ['keyword', 'text', 'keyword'],
    });
  }
  
  export function rule_for(_FOR: string, _IN: string){
    return recognize('start', {
      regex: '(' + _FOR + ' )(\\w+)( ' + _IN + ' )(\\w+)',
      token: ['keyword', 'text', 'keyword', 'text'],
    });
  }
  
  export function rule_forRange(_FOR: string, _IN: string, _RANGE: string) {
    return recognize('start', {
      regex: '(' + _FOR + ' )(\\w+)( ' + _IN + ' ' + _RANGE + ' )(\\w+)( to )(\\w+)',
      token: ['keyword', 'text', 'keyword', 'text', 'keyword', 'text'],
    });
  }
  
  export function rule_forRangeParen(_FOR: string, _IN: string, _RANGE: string) {
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
  export function keywordWithSpace(keyword: string) {
    return '\\b' + keyword + ' ';
  }