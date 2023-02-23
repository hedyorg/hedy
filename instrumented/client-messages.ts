function cov_2nzdw0g6v4() {
  var path = "/home/capybara/repos/hedyc/static/js/client-messages.ts";
  var hash = "f14f493436910f39d78b169945bdc567184ce1dc";
  var global = new Function("return this")();
  var gcv = "__coverage__";
  var coverageData = {
    path: "/home/capybara/repos/hedyc/static/js/client-messages.ts",
    statementMap: {
      "0": {
        start: {
          line: 4,
          column: 56
        },
        end: {
          line: 4,
          column: 93
        }
      },
      "1": {
        start: {
          line: 11,
          column: 2
        },
        end: {
          line: 11,
          column: 73
        }
      }
    },
    fnMap: {
      "0": {
        name: "setClientMessageLanguage",
        decl: {
          start: {
            line: 9,
            column: 16
          },
          end: {
            line: 9,
            column: 40
          }
        },
        loc: {
          start: {
            line: 9,
            column: 54
          },
          end: {
            line: 12,
            column: 1
          }
        },
        line: 9
      }
    },
    branchMap: {
      "0": {
        loc: {
          start: {
            line: 11,
            column: 32
          },
          end: {
            line: 11,
            column: 71
          }
        },
        type: "binary-expr",
        locations: [{
          start: {
            line: 11,
            column: 32
          },
          end: {
            line: 11,
            column: 49
          }
        }, {
          start: {
            line: 11,
            column: 53
          },
          end: {
            line: 11,
            column: 71
          }
        }],
        line: 11
      }
    },
    s: {
      "0": 0,
      "1": 0
    },
    f: {
      "0": 0
    },
    b: {
      "0": [0, 0]
    },
    _coverageSchema: "1a1c01bbd47fc00a2c39e90264f33305004495a9",
    hash: "f14f493436910f39d78b169945bdc567184ce1dc"
  };
  var coverage = global[gcv] || (global[gcv] = {});
  if (!coverage[path] || coverage[path].hash !== hash) {
    coverage[path] = coverageData;
  }
  var actualCoverage = coverage[path];
  {
    // @ts-ignore
    cov_2nzdw0g6v4 = function () {
      return actualCoverage;
    };
  }
  return actualCoverage;
}
cov_2nzdw0g6v4();
import { MessageKey, TRANSLATIONS } from './message-translations';
export let ClientMessages: Record<MessageKey, string> = (cov_2nzdw0g6v4().s[0]++, Object.assign({}, TRANSLATIONS['en']));

/**
 * Switch the values in the 'ErrorMessages' global
 */
export function setClientMessageLanguage(key: string) {
  cov_2nzdw0g6v4().f[0]++;
  cov_2nzdw0g6v4().s[1]++;
  // Mutate the object in-place, so that all imported references are still valid
  Object.assign(ClientMessages, (cov_2nzdw0g6v4().b[0][0]++, TRANSLATIONS[key]) ?? (cov_2nzdw0g6v4().b[0][1]++, TRANSLATIONS['en']));
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjb3ZfMm56ZHcwZzZ2NCIsImFjdHVhbENvdmVyYWdlIiwiTWVzc2FnZUtleSIsIlRSQU5TTEFUSU9OUyIsIkNsaWVudE1lc3NhZ2VzIiwiUmVjb3JkIiwicyIsIk9iamVjdCIsImFzc2lnbiIsInNldENsaWVudE1lc3NhZ2VMYW5ndWFnZSIsImtleSIsImYiLCJiIl0sInNvdXJjZXMiOlsiY2xpZW50LW1lc3NhZ2VzLnRzIl0sInNvdXJjZXNDb250ZW50IjpbIlxuaW1wb3J0IHsgTWVzc2FnZUtleSwgVFJBTlNMQVRJT05TIH0gZnJvbSAnLi9tZXNzYWdlLXRyYW5zbGF0aW9ucyc7XG5cbmV4cG9ydCBsZXQgQ2xpZW50TWVzc2FnZXM6IFJlY29yZDxNZXNzYWdlS2V5LCBzdHJpbmc+ID0gT2JqZWN0LmFzc2lnbih7fSwgVFJBTlNMQVRJT05TWydlbiddKTtcblxuLyoqXG4gKiBTd2l0Y2ggdGhlIHZhbHVlcyBpbiB0aGUgJ0Vycm9yTWVzc2FnZXMnIGdsb2JhbFxuICovXG5leHBvcnQgZnVuY3Rpb24gc2V0Q2xpZW50TWVzc2FnZUxhbmd1YWdlKGtleTogc3RyaW5nKSB7XG4gIC8vIE11dGF0ZSB0aGUgb2JqZWN0IGluLXBsYWNlLCBzbyB0aGF0IGFsbCBpbXBvcnRlZCByZWZlcmVuY2VzIGFyZSBzdGlsbCB2YWxpZFxuICBPYmplY3QuYXNzaWduKENsaWVudE1lc3NhZ2VzLCBUUkFOU0xBVElPTlNba2V5XSA/PyBUUkFOU0xBVElPTlNbJ2VuJ10pO1xufVxuIl0sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0lBZVk7SUFBQUEsY0FBQSxZQUFBQSxDQUFBO01BQUEsT0FBQUMsY0FBQTtJQUFBO0VBQUE7RUFBQSxPQUFBQSxjQUFBO0FBQUE7QUFBQUQsY0FBQTtBQWRaLFNBQVNFLFVBQVUsRUFBRUMsWUFBWSxRQUFRLHdCQUF3QjtBQUVqRSxPQUFPLElBQUlDLGNBQWMsRUFBRUMsTUFBTSxDQUFDSCxVQUFVLEVBQUUsTUFBTSxDQUFDLElBQUFGLGNBQUEsR0FBQU0sQ0FBQSxPQUFHQyxNQUFNLENBQUNDLE1BQU0sQ0FBQyxDQUFDLENBQUMsRUFBRUwsWUFBWSxDQUFDLElBQUksQ0FBQyxDQUFDOztBQUU3RjtBQUNBO0FBQ0E7QUFDQSxPQUFPLFNBQVNNLHdCQUF3QkEsQ0FBQ0MsR0FBRyxFQUFFLE1BQU0sRUFBRTtFQUFBVixjQUFBLEdBQUFXLENBQUE7RUFBQVgsY0FBQSxHQUFBTSxDQUFBO0VBQ3BEO0VBQ0FDLE1BQU0sQ0FBQ0MsTUFBTSxDQUFDSixjQUFjLEVBQUUsQ0FBQUosY0FBQSxHQUFBWSxDQUFBLFVBQUFULFlBQVksQ0FBQ08sR0FBRyxDQUFDLE1BQUFWLGNBQUEsR0FBQVksQ0FBQSxVQUFJVCxZQUFZLENBQUMsSUFBSSxDQUFDLEVBQUM7QUFDeEUifQ==