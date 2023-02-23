function cov_2pctnmly3b() {
  var path = "/home/capybara/repos/hedyc/static/js/initialize.ts";
  var hash = "2f21166c66894fd84cb007704caf32aa5f37d8c0";
  var global = new Function("return this")();
  var gcv = "__coverage__";
  var coverageData = {
    path: "/home/capybara/repos/hedyc/static/js/initialize.ts",
    statementMap: {
      "0": {
        start: {
          line: 18,
          column: 2
        },
        end: {
          line: 18,
          column: 43
        }
      },
      "1": {
        start: {
          line: 20,
          column: 2
        },
        end: {
          line: 20,
          column: 18
        }
      },
      "2": {
        start: {
          line: 21,
          column: 2
        },
        end: {
          line: 21,
          column: 26
        }
      },
      "3": {
        start: {
          line: 22,
          column: 2
        },
        end: {
          line: 22,
          column: 19
        }
      },
      "4": {
        start: {
          line: 23,
          column: 2
        },
        end: {
          line: 23,
          column: 19
        }
      },
      "5": {
        start: {
          line: 24,
          column: 2
        },
        end: {
          line: 24,
          column: 23
        }
      },
      "6": {
        start: {
          line: 30,
          column: 2
        },
        end: {
          line: 32,
          column: 3
        }
      },
      "7": {
        start: {
          line: 31,
          column: 4
        },
        end: {
          line: 31,
          column: 22
        }
      }
    },
    fnMap: {
      "0": {
        name: "initialize",
        decl: {
          start: {
            line: 17,
            column: 16
          },
          end: {
            line: 17,
            column: 26
          }
        },
        loc: {
          start: {
            line: 17,
            column: 58
          },
          end: {
            line: 33,
            column: 1
          }
        },
        line: 17
      }
    },
    branchMap: {
      "0": {
        loc: {
          start: {
            line: 17,
            column: 27
          },
          end: {
            line: 17,
            column: 56
          }
        },
        type: "default-arg",
        locations: [{
          start: {
            line: 17,
            column: 54
          },
          end: {
            line: 17,
            column: 56
          }
        }],
        line: 17
      },
      "1": {
        loc: {
          start: {
            line: 30,
            column: 2
          },
          end: {
            line: 32,
            column: 3
          }
        },
        type: "if",
        locations: [{
          start: {
            line: 30,
            column: 2
          },
          end: {
            line: 32,
            column: 3
          }
        }, {
          start: {
            line: 30,
            column: 2
          },
          end: {
            line: 32,
            column: 3
          }
        }],
        line: 30
      }
    },
    s: {
      "0": 0,
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 0,
      "5": 0,
      "6": 0,
      "7": 0
    },
    f: {
      "0": 0
    },
    b: {
      "0": [0],
      "1": [0, 0]
    },
    _coverageSchema: "1a1c01bbd47fc00a2c39e90264f33305004495a9",
    hash: "2f21166c66894fd84cb007704caf32aa5f37d8c0"
  };
  var coverage = global[gcv] || (global[gcv] = {});
  if (!coverage[path] || coverage[path].hash !== hash) {
    coverage[path] = coverageData;
  }
  var actualCoverage = coverage[path];
  {
    // @ts-ignore
    cov_2pctnmly3b = function () {
      return actualCoverage;
    };
  }
  return actualCoverage;
}
cov_2pctnmly3b();
import { initializeApp } from './app';
import { initializeFormSubmits } from './auth';
import { setClientMessageLanguage } from './client-messages';
import { logs } from './logs';
import { initializeQuiz } from './quiz';
import { APP_STATE } from './state';
import { initializeTabs } from './tabs';
import { initializeTutorial } from './tutorials/tutorial';
export interface InitializeOptions {
  readonly logs?: boolean;
}

/**
 * This function gets called by the HTML when the page is being initialized.
 */
export function initialize(options: InitializeOptions = (cov_2pctnmly3b().b[0][0]++, {})) {
  cov_2pctnmly3b().f[0]++;
  cov_2pctnmly3b().s[0]++;
  setClientMessageLanguage(APP_STATE.lang);
  cov_2pctnmly3b().s[1]++;
  initializeApp();
  cov_2pctnmly3b().s[2]++;
  initializeFormSubmits();
  cov_2pctnmly3b().s[3]++;
  initializeQuiz();
  cov_2pctnmly3b().s[4]++;
  initializeTabs();
  cov_2pctnmly3b().s[5]++;
  initializeTutorial();

  // initializing the teacher/customize class pages is done in a different
  // file. That is not great, we should be using a parameter to this function
  // probably, but for now that is what it is.
  cov_2pctnmly3b().s[6]++;
  if (options.logs) {
    cov_2pctnmly3b().b[1][0]++;
    cov_2pctnmly3b().s[7]++;
    logs.initialize();
  } else {
    cov_2pctnmly3b().b[1][1]++;
  }
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjb3ZfMnBjdG5tbHkzYiIsImFjdHVhbENvdmVyYWdlIiwiaW5pdGlhbGl6ZUFwcCIsImluaXRpYWxpemVGb3JtU3VibWl0cyIsInNldENsaWVudE1lc3NhZ2VMYW5ndWFnZSIsImxvZ3MiLCJpbml0aWFsaXplUXVpeiIsIkFQUF9TVEFURSIsImluaXRpYWxpemVUYWJzIiwiaW5pdGlhbGl6ZVR1dG9yaWFsIiwiSW5pdGlhbGl6ZU9wdGlvbnMiLCJpbml0aWFsaXplIiwib3B0aW9ucyIsImIiLCJmIiwicyIsImxhbmciXSwic291cmNlcyI6WyJpbml0aWFsaXplLnRzIl0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IGluaXRpYWxpemVBcHAgfSBmcm9tICcuL2FwcCc7XG5pbXBvcnQgeyBpbml0aWFsaXplRm9ybVN1Ym1pdHMgfSBmcm9tICcuL2F1dGgnO1xuaW1wb3J0IHsgc2V0Q2xpZW50TWVzc2FnZUxhbmd1YWdlIH0gZnJvbSAnLi9jbGllbnQtbWVzc2FnZXMnO1xuaW1wb3J0IHsgbG9ncyB9IGZyb20gJy4vbG9ncyc7XG5pbXBvcnQgeyBpbml0aWFsaXplUXVpeiB9IGZyb20gJy4vcXVpeic7XG5pbXBvcnQgeyBBUFBfU1RBVEUgfSBmcm9tICcuL3N0YXRlJztcbmltcG9ydCB7IGluaXRpYWxpemVUYWJzIH0gZnJvbSAnLi90YWJzJztcbmltcG9ydCB7IGluaXRpYWxpemVUdXRvcmlhbCB9IGZyb20gJy4vdHV0b3JpYWxzL3R1dG9yaWFsJztcblxuZXhwb3J0IGludGVyZmFjZSBJbml0aWFsaXplT3B0aW9ucyB7XG4gIHJlYWRvbmx5IGxvZ3M/OiBib29sZWFuO1xufVxuXG4vKipcbiAqIFRoaXMgZnVuY3Rpb24gZ2V0cyBjYWxsZWQgYnkgdGhlIEhUTUwgd2hlbiB0aGUgcGFnZSBpcyBiZWluZyBpbml0aWFsaXplZC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGluaXRpYWxpemUob3B0aW9uczogSW5pdGlhbGl6ZU9wdGlvbnM9e30pIHtcbiAgc2V0Q2xpZW50TWVzc2FnZUxhbmd1YWdlKEFQUF9TVEFURS5sYW5nKTtcblxuICBpbml0aWFsaXplQXBwKCk7XG4gIGluaXRpYWxpemVGb3JtU3VibWl0cygpO1xuICBpbml0aWFsaXplUXVpeigpO1xuICBpbml0aWFsaXplVGFicygpO1xuICBpbml0aWFsaXplVHV0b3JpYWwoKTtcblxuICAvLyBpbml0aWFsaXppbmcgdGhlIHRlYWNoZXIvY3VzdG9taXplIGNsYXNzIHBhZ2VzIGlzIGRvbmUgaW4gYSBkaWZmZXJlbnRcbiAgLy8gZmlsZS4gVGhhdCBpcyBub3QgZ3JlYXQsIHdlIHNob3VsZCBiZSB1c2luZyBhIHBhcmFtZXRlciB0byB0aGlzIGZ1bmN0aW9uXG4gIC8vIHByb2JhYmx5LCBidXQgZm9yIG5vdyB0aGF0IGlzIHdoYXQgaXQgaXMuXG5cbiAgaWYgKG9wdGlvbnMubG9ncykge1xuICAgIGxvZ3MuaW5pdGlhbGl6ZSgpO1xuICB9XG59XG5cbiJdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7SUFlWTtJQUFBQSxjQUFBLFlBQUFBLENBQUE7TUFBQSxPQUFBQyxjQUFBO0lBQUE7RUFBQTtFQUFBLE9BQUFBLGNBQUE7QUFBQTtBQUFBRCxjQUFBO0FBZlosU0FBU0UsYUFBYSxRQUFRLE9BQU87QUFDckMsU0FBU0MscUJBQXFCLFFBQVEsUUFBUTtBQUM5QyxTQUFTQyx3QkFBd0IsUUFBUSxtQkFBbUI7QUFDNUQsU0FBU0MsSUFBSSxRQUFRLFFBQVE7QUFDN0IsU0FBU0MsY0FBYyxRQUFRLFFBQVE7QUFDdkMsU0FBU0MsU0FBUyxRQUFRLFNBQVM7QUFDbkMsU0FBU0MsY0FBYyxRQUFRLFFBQVE7QUFDdkMsU0FBU0Msa0JBQWtCLFFBQVEsc0JBQXNCO0FBRXpELE9BQU8sVUFBVUMsaUJBQWlCLENBQUM7RUFDakMsU0FBU0wsSUFBSSxDQUFDLEVBQUUsT0FBTztBQUN6Qjs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxPQUFPLFNBQVNNLFVBQVVBLENBQUNDLE9BQU8sRUFBRUYsaUJBQWlCLElBQUFWLGNBQUEsR0FBQWEsQ0FBQSxVQUFDLENBQUMsQ0FBQyxHQUFFO0VBQUFiLGNBQUEsR0FBQWMsQ0FBQTtFQUFBZCxjQUFBLEdBQUFlLENBQUE7RUFDeERYLHdCQUF3QixDQUFDRyxTQUFTLENBQUNTLElBQUksQ0FBQztFQUFDaEIsY0FBQSxHQUFBZSxDQUFBO0VBRXpDYixhQUFhLEVBQUU7RUFBQ0YsY0FBQSxHQUFBZSxDQUFBO0VBQ2hCWixxQkFBcUIsRUFBRTtFQUFDSCxjQUFBLEdBQUFlLENBQUE7RUFDeEJULGNBQWMsRUFBRTtFQUFDTixjQUFBLEdBQUFlLENBQUE7RUFDakJQLGNBQWMsRUFBRTtFQUFDUixjQUFBLEdBQUFlLENBQUE7RUFDakJOLGtCQUFrQixFQUFFOztFQUVwQjtFQUNBO0VBQ0E7RUFBQVQsY0FBQSxHQUFBZSxDQUFBO0VBRUEsSUFBSUgsT0FBTyxDQUFDUCxJQUFJLEVBQUU7SUFBQUwsY0FBQSxHQUFBYSxDQUFBO0lBQUFiLGNBQUEsR0FBQWUsQ0FBQTtJQUNoQlYsSUFBSSxDQUFDTSxVQUFVLEVBQUU7RUFDbkIsQ0FBQztJQUFBWCxjQUFBLEdBQUFhLENBQUE7RUFBQTtBQUNIIn0=