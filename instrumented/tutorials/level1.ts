function cov_29mwl0n763() {
  var path = "/home/capybara/repos/hedyc/static/js/tutorials/level1.ts";
  var hash = "20217fbee77ca0746c2abd518f4f3beca58cdcad";
  var global = new Function("return this")();
  var gcv = "__coverage__";
  var coverageData = {
    path: "/home/capybara/repos/hedyc/static/js/tutorials/level1.ts",
    statementMap: {
      "0": {
        start: {
          line: 13,
          column: 19
        },
        end: {
          line: 13,
          column: 20
        }
      },
      "1": {
        start: {
          line: 16,
          column: 2
        },
        end: {
          line: 16,
          column: 19
        }
      },
      "2": {
        start: {
          line: 18,
          column: 2
        },
        end: {
          line: 18,
          column: 35
        }
      },
      "3": {
        start: {
          line: 22,
          column: 2
        },
        end: {
          line: 22,
          column: 20
        }
      },
      "4": {
        start: {
          line: 24,
          column: 2
        },
        end: {
          line: 31,
          column: 3
        }
      },
      "5": {
        start: {
          line: 25,
          column: 4
        },
        end: {
          line: 25,
          column: 52
        }
      },
      "6": {
        start: {
          line: 26,
          column: 4
        },
        end: {
          line: 26,
          column: 26
        }
      },
      "7": {
        start: {
          line: 27,
          column: 4
        },
        end: {
          line: 27,
          column: 26
        }
      },
      "8": {
        start: {
          line: 29,
          column: 9
        },
        end: {
          line: 31,
          column: 3
        }
      },
      "9": {
        start: {
          line: 30,
          column: 4
        },
        end: {
          line: 30,
          column: 30
        }
      }
    },
    fnMap: {
      "0": {
        name: "startLevel1",
        decl: {
          start: {
            line: 15,
            column: 16
          },
          end: {
            line: 15,
            column: 27
          }
        },
        loc: {
          start: {
            line: 15,
            column: 30
          },
          end: {
            line: 19,
            column: 1
          }
        },
        line: 15
      },
      "1": {
        name: "callNextStepLevel1",
        decl: {
          start: {
            line: 21,
            column: 16
          },
          end: {
            line: 21,
            column: 34
          }
        },
        loc: {
          start: {
            line: 21,
            column: 37
          },
          end: {
            line: 33,
            column: 1
          }
        },
        line: 21
      }
    },
    branchMap: {
      "0": {
        loc: {
          start: {
            line: 24,
            column: 2
          },
          end: {
            line: 31,
            column: 3
          }
        },
        type: "if",
        locations: [{
          start: {
            line: 24,
            column: 2
          },
          end: {
            line: 31,
            column: 3
          }
        }, {
          start: {
            line: 24,
            column: 2
          },
          end: {
            line: 31,
            column: 3
          }
        }],
        line: 24
      },
      "1": {
        loc: {
          start: {
            line: 29,
            column: 9
          },
          end: {
            line: 31,
            column: 3
          }
        },
        type: "if",
        locations: [{
          start: {
            line: 29,
            column: 9
          },
          end: {
            line: 31,
            column: 3
          }
        }, {
          start: {
            line: 29,
            column: 9
          },
          end: {
            line: 31,
            column: 3
          }
        }],
        line: 29
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
      "7": 0,
      "8": 0,
      "9": 0
    },
    f: {
      "0": 0,
      "1": 0
    },
    b: {
      "0": [0, 0],
      "1": [0, 0]
    },
    _coverageSchema: "1a1c01bbd47fc00a2c39e90264f33305004495a9",
    hash: "20217fbee77ca0746c2abd518f4f3beca58cdcad"
  };
  var coverage = global[gcv] || (global[gcv] = {});
  if (!coverage[path] || coverage[path].hash !== hash) {
    coverage[path] = coverageData;
  }
  var actualCoverage = coverage[path];
  {
    // @ts-ignore
    cov_29mwl0n763 = function () {
      return actualCoverage;
    };
  }
  return actualCoverage;
}
cov_29mwl0n763();
/*** ADDING A TUTORIAL LEVEL SHORT GUIDE ***/

// Use this file as a template to create the tutorial for any level
// Create a dedicated file such as "level2.ts" and make sure you have startLevelX() and callNextStepLevelX() functions
// Add these to the startLevel() and callNextLevelStep() functions in tutorial.ts and make sure to import them correctly
// Also make sure that for every step/level combination there is an entry in the corresponding YAML file
// To start the tutorial for a specific level, for example level 1
// Call "startLevelTutorial(<level>)" on from a template, the rest should be handled automatically

import { theGlobalEditor } from "../app";
import { tutorialPopup, relocatePopup } from "./utils";
let current_step = (cov_29mwl0n763().s[0]++, 0);
export function startLevel1() {
  cov_29mwl0n763().f[0]++;
  cov_29mwl0n763().s[1]++;
  current_step = 1;
  cov_29mwl0n763().s[2]++;
  tutorialPopup("1", current_step);
}
export function callNextStepLevel1() {
  cov_29mwl0n763().f[1]++;
  cov_29mwl0n763().s[3]++;
  current_step += 1;
  cov_29mwl0n763().s[4]++;
  if (current_step == 2) {
    cov_29mwl0n763().b[0][0]++;
    cov_29mwl0n763().s[5]++;
    theGlobalEditor?.setValue("print Hello world!");
    cov_29mwl0n763().s[6]++;
    relocatePopup(50, 70);
    cov_29mwl0n763().s[7]++;
    tutorialPopup("1", 2);
  } else {
    cov_29mwl0n763().b[0][1]++;
    cov_29mwl0n763().s[8]++;
    if (current_step == 3) {
      cov_29mwl0n763().b[1][0]++;
      cov_29mwl0n763().s[9]++;
      location.replace("/hedy");
    } else {
      cov_29mwl0n763().b[1][1]++;
    }
  }
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjb3ZfMjltd2wwbjc2MyIsImFjdHVhbENvdmVyYWdlIiwidGhlR2xvYmFsRWRpdG9yIiwidHV0b3JpYWxQb3B1cCIsInJlbG9jYXRlUG9wdXAiLCJjdXJyZW50X3N0ZXAiLCJzIiwic3RhcnRMZXZlbDEiLCJmIiwiY2FsbE5leHRTdGVwTGV2ZWwxIiwiYiIsInNldFZhbHVlIiwibG9jYXRpb24iLCJyZXBsYWNlIl0sInNvdXJjZXMiOlsibGV2ZWwxLnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKiogQURESU5HIEEgVFVUT1JJQUwgTEVWRUwgU0hPUlQgR1VJREUgKioqL1xuXG4vLyBVc2UgdGhpcyBmaWxlIGFzIGEgdGVtcGxhdGUgdG8gY3JlYXRlIHRoZSB0dXRvcmlhbCBmb3IgYW55IGxldmVsXG4vLyBDcmVhdGUgYSBkZWRpY2F0ZWQgZmlsZSBzdWNoIGFzIFwibGV2ZWwyLnRzXCIgYW5kIG1ha2Ugc3VyZSB5b3UgaGF2ZSBzdGFydExldmVsWCgpIGFuZCBjYWxsTmV4dFN0ZXBMZXZlbFgoKSBmdW5jdGlvbnNcbi8vIEFkZCB0aGVzZSB0byB0aGUgc3RhcnRMZXZlbCgpIGFuZCBjYWxsTmV4dExldmVsU3RlcCgpIGZ1bmN0aW9ucyBpbiB0dXRvcmlhbC50cyBhbmQgbWFrZSBzdXJlIHRvIGltcG9ydCB0aGVtIGNvcnJlY3RseVxuLy8gQWxzbyBtYWtlIHN1cmUgdGhhdCBmb3IgZXZlcnkgc3RlcC9sZXZlbCBjb21iaW5hdGlvbiB0aGVyZSBpcyBhbiBlbnRyeSBpbiB0aGUgY29ycmVzcG9uZGluZyBZQU1MIGZpbGVcbi8vIFRvIHN0YXJ0IHRoZSB0dXRvcmlhbCBmb3IgYSBzcGVjaWZpYyBsZXZlbCwgZm9yIGV4YW1wbGUgbGV2ZWwgMVxuLy8gQ2FsbCBcInN0YXJ0TGV2ZWxUdXRvcmlhbCg8bGV2ZWw+KVwiIG9uIGZyb20gYSB0ZW1wbGF0ZSwgdGhlIHJlc3Qgc2hvdWxkIGJlIGhhbmRsZWQgYXV0b21hdGljYWxseVxuXG5pbXBvcnQge3RoZUdsb2JhbEVkaXRvcn0gZnJvbSBcIi4uL2FwcFwiO1xuaW1wb3J0IHt0dXRvcmlhbFBvcHVwLCByZWxvY2F0ZVBvcHVwfSBmcm9tIFwiLi91dGlsc1wiO1xuXG5sZXQgY3VycmVudF9zdGVwID0gMDtcblxuZXhwb3J0IGZ1bmN0aW9uIHN0YXJ0TGV2ZWwxKCkge1xuICBjdXJyZW50X3N0ZXAgPSAxO1xuXG4gIHR1dG9yaWFsUG9wdXAoXCIxXCIsIGN1cnJlbnRfc3RlcCk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBjYWxsTmV4dFN0ZXBMZXZlbDEoKSB7XG4gIGN1cnJlbnRfc3RlcCArPSAxO1xuXG4gIGlmIChjdXJyZW50X3N0ZXAgPT0gMikge1xuICAgIHRoZUdsb2JhbEVkaXRvcj8uc2V0VmFsdWUoXCJwcmludCBIZWxsbyB3b3JsZCFcIik7XG4gICAgcmVsb2NhdGVQb3B1cCg1MCwgNzApO1xuICAgIHR1dG9yaWFsUG9wdXAoXCIxXCIsIDIpO1xuXG4gIH0gZWxzZSBpZiAoY3VycmVudF9zdGVwID09IDMpIHtcbiAgICBsb2NhdGlvbi5yZXBsYWNlKFwiL2hlZHlcIik7XG4gIH1cblxufSJdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztJQWVZO0lBQUFBLGNBQUEsWUFBQUEsQ0FBQTtNQUFBLE9BQUFDLGNBQUE7SUFBQTtFQUFBO0VBQUEsT0FBQUEsY0FBQTtBQUFBO0FBQUFELGNBQUE7QUFmWjs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEsU0FBUUUsZUFBZSxRQUFPLFFBQVE7QUFDdEMsU0FBUUMsYUFBYSxFQUFFQyxhQUFhLFFBQU8sU0FBUztBQUVwRCxJQUFJQyxZQUFZLElBQUFMLGNBQUEsR0FBQU0sQ0FBQSxPQUFHLENBQUM7QUFFcEIsT0FBTyxTQUFTQyxXQUFXQSxDQUFBLEVBQUc7RUFBQVAsY0FBQSxHQUFBUSxDQUFBO0VBQUFSLGNBQUEsR0FBQU0sQ0FBQTtFQUM1QkQsWUFBWSxHQUFHLENBQUM7RUFBQ0wsY0FBQSxHQUFBTSxDQUFBO0VBRWpCSCxhQUFhLENBQUMsR0FBRyxFQUFFRSxZQUFZLENBQUM7QUFDbEM7QUFFQSxPQUFPLFNBQVNJLGtCQUFrQkEsQ0FBQSxFQUFHO0VBQUFULGNBQUEsR0FBQVEsQ0FBQTtFQUFBUixjQUFBLEdBQUFNLENBQUE7RUFDbkNELFlBQVksSUFBSSxDQUFDO0VBQUNMLGNBQUEsR0FBQU0sQ0FBQTtFQUVsQixJQUFJRCxZQUFZLElBQUksQ0FBQyxFQUFFO0lBQUFMLGNBQUEsR0FBQVUsQ0FBQTtJQUFBVixjQUFBLEdBQUFNLENBQUE7SUFDckJKLGVBQWUsRUFBRVMsUUFBUSxDQUFDLG9CQUFvQixDQUFDO0lBQUNYLGNBQUEsR0FBQU0sQ0FBQTtJQUNoREYsYUFBYSxDQUFDLEVBQUUsRUFBRSxFQUFFLENBQUM7SUFBQ0osY0FBQSxHQUFBTSxDQUFBO0lBQ3RCSCxhQUFhLENBQUMsR0FBRyxFQUFFLENBQUMsQ0FBQztFQUV2QixDQUFDLE1BQU07SUFBQUgsY0FBQSxHQUFBVSxDQUFBO0lBQUFWLGNBQUEsR0FBQU0sQ0FBQTtJQUFBLElBQUlELFlBQVksSUFBSSxDQUFDLEVBQUU7TUFBQUwsY0FBQSxHQUFBVSxDQUFBO01BQUFWLGNBQUEsR0FBQU0sQ0FBQTtNQUM1Qk0sUUFBUSxDQUFDQyxPQUFPLENBQUMsT0FBTyxDQUFDO0lBQzNCLENBQUM7TUFBQWIsY0FBQSxHQUFBVSxDQUFBO0lBQUE7RUFBRDtBQUVGIn0=