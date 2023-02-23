function cov_n3jptcs37() {
  var path = "/home/capybara/repos/hedyc/static/js/buttons.js";
  var hash = "358b89019b8c4478d19e2a00ffd6e318722cffd8";
  var global = new Function("return this")();
  var gcv = "__coverage__";
  var coverageData = {
    path: "/home/capybara/repos/hedyc/static/js/buttons.js",
    statementMap: {
      "0": {
        start: {
          line: 8,
          column: 21
        },
        end: {
          line: 14,
          column: 1
        }
      },
      "1": {
        start: {
          line: 9,
          column: 14
        },
        end: {
          line: 9,
          column: 16
        }
      },
      "2": {
        start: {
          line: 11,
          column: 4
        },
        end: {
          line: 11,
          column: 47
        }
      },
      "3": {
        start: {
          line: 13,
          column: 4
        },
        end: {
          line: 13,
          column: 15
        }
      },
      "4": {
        start: {
          line: 17,
          column: 17
        },
        end: {
          line: 17,
          column: 49
        }
      },
      "5": {
        start: {
          line: 18,
          column: 18
        },
        end: {
          line: 18,
          column: 40
        }
      },
      "6": {
        start: {
          line: 19,
          column: 4
        },
        end: {
          line: 19,
          column: 37
        }
      },
      "7": {
        start: {
          line: 20,
          column: 4
        },
        end: {
          line: 20,
          column: 28
        }
      },
      "8": {
        start: {
          line: 21,
          column: 4
        },
        end: {
          line: 23,
          column: 6
        }
      },
      "9": {
        start: {
          line: 22,
          column: 8
        },
        end: {
          line: 22,
          column: 27
        }
      },
      "10": {
        start: {
          line: 24,
          column: 4
        },
        end: {
          line: 24,
          column: 67
        }
      },
      "11": {
        start: {
          line: 26,
          column: 4
        },
        end: {
          line: 26,
          column: 66
        }
      },
      "12": {
        start: {
          line: 29,
          column: 19
        },
        end: {
          line: 37,
          column: 1
        }
      },
      "13": {
        start: {
          line: 30,
          column: 18
        },
        end: {
          line: 30,
          column: 40
        }
      },
      "14": {
        start: {
          line: 35,
          column: 12
        },
        end: {
          line: 35,
          column: 58
        }
      },
      "15": {
        start: {
          line: 36,
          column: 4
        },
        end: {
          line: 36,
          column: 36
        }
      }
    },
    fnMap: {
      "0": {
        name: "(anonymous_0)",
        decl: {
          start: {
            line: 8,
            column: 21
          },
          end: {
            line: 8,
            column: 22
          }
        },
        loc: {
          start: {
            line: 8,
            column: 37
          },
          end: {
            line: 14,
            column: 1
          }
        },
        line: 8
      },
      "1": {
        name: "buttons_add",
        decl: {
          start: {
            line: 16,
            column: 9
          },
          end: {
            line: 16,
            column: 20
          }
        },
        loc: {
          start: {
            line: 16,
            column: 27
          },
          end: {
            line: 27,
            column: 1
          }
        },
        line: 16
      },
      "2": {
        name: "(anonymous_2)",
        decl: {
          start: {
            line: 21,
            column: 21
          },
          end: {
            line: 21,
            column: 22
          }
        },
        loc: {
          start: {
            line: 21,
            column: 33
          },
          end: {
            line: 23,
            column: 5
          }
        },
        line: 21
      },
      "3": {
        name: "(anonymous_3)",
        decl: {
          start: {
            line: 29,
            column: 19
          },
          end: {
            line: 29,
            column: 20
          }
        },
        loc: {
          start: {
            line: 29,
            column: 35
          },
          end: {
            line: 37,
            column: 1
          }
        },
        line: 29
      }
    },
    branchMap: {},
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
      "9": 0,
      "10": 0,
      "11": 0,
      "12": 0,
      "13": 0,
      "14": 0,
      "15": 0
    },
    f: {
      "0": 0,
      "1": 0,
      "2": 0,
      "3": 0
    },
    b: {},
    _coverageSchema: "1a1c01bbd47fc00a2c39e90264f33305004495a9",
    hash: "358b89019b8c4478d19e2a00ffd6e318722cffd8"
  };
  var coverage = global[gcv] || (global[gcv] = {});
  if (!coverage[path] || coverage[path].hash !== hash) {
    coverage[path] = coverageData;
  }
  var actualCoverage = coverage[path];
  {
    // @ts-ignore
    cov_n3jptcs37 = function () {
      return actualCoverage;
    };
  }
  return actualCoverage;
}
cov_n3jptcs37();
cov_n3jptcs37().s[0]++;
// This file defines a module that can be imported as an external module
// in Python through Skulpt.
//
// The module is defined in a variable called $builtinmodule (that is a
// function for some reason) in which a variable mod is created containing all
// the member functions and classes of that module.

var $builtinmodule = function (name) {
  cov_n3jptcs37().f[0]++;
  var mod = (cov_n3jptcs37().s[1]++, {});
  cov_n3jptcs37().s[2]++;
  mod.add = new Sk.builtin.func(buttons_add);
  cov_n3jptcs37().s[3]++;
  return mod;
};
function buttons_add(name) {
  cov_n3jptcs37().f[1]++;
  let button = (cov_n3jptcs37().s[4]++, document.createElement("button"));
  var name_js = (cov_n3jptcs37().s[5]++, Sk.ffi.remapToJs(name));
  cov_n3jptcs37().s[6]++;
  button.classList.add("blue-btn");
  cov_n3jptcs37().s[7]++;
  button.innerText = name;
  cov_n3jptcs37().s[8]++;
  button.onclick = function () {
    cov_n3jptcs37().f[2]++;
    cov_n3jptcs37().s[9]++;
    button_click(name);
  };
  cov_n3jptcs37().s[10]++;
  document.getElementById("dynamic-buttons").appendChild(button);
  cov_n3jptcs37().s[11]++;
  document.getElementById("dynamic-buttons").style.display = "";
}
cov_n3jptcs37().s[12]++;
var button_click = function (name) {
  cov_n3jptcs37().f[3]++;
  var name_js = (cov_n3jptcs37().s[13]++, Sk.ffi.remapToJs(name));

  // For this to work the first element of e needs to be a constant indicating
  // this event is from a button, to make sure it is unique we use USEREVENT
  // the dictionary can then be filled with whatever data we need.
  var e = (cov_n3jptcs37().s[14]++, [PygameLib.constants.USEREVENT, {
    key: name
  }]);
  cov_n3jptcs37().s[15]++;
  PygameLib.eventQueue.unshift(e);
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjb3ZfbjNqcHRjczM3IiwiYWN0dWFsQ292ZXJhZ2UiLCJzIiwiJGJ1aWx0aW5tb2R1bGUiLCJuYW1lIiwiZiIsIm1vZCIsImFkZCIsIlNrIiwiYnVpbHRpbiIsImZ1bmMiLCJidXR0b25zX2FkZCIsImJ1dHRvbiIsImRvY3VtZW50IiwiY3JlYXRlRWxlbWVudCIsIm5hbWVfanMiLCJmZmkiLCJyZW1hcFRvSnMiLCJjbGFzc0xpc3QiLCJpbm5lclRleHQiLCJvbmNsaWNrIiwiYnV0dG9uX2NsaWNrIiwiZ2V0RWxlbWVudEJ5SWQiLCJhcHBlbmRDaGlsZCIsInN0eWxlIiwiZGlzcGxheSIsImUiLCJQeWdhbWVMaWIiLCJjb25zdGFudHMiLCJVU0VSRVZFTlQiLCJrZXkiLCJldmVudFF1ZXVlIiwidW5zaGlmdCJdLCJzb3VyY2VzIjpbImJ1dHRvbnMuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gVGhpcyBmaWxlIGRlZmluZXMgYSBtb2R1bGUgdGhhdCBjYW4gYmUgaW1wb3J0ZWQgYXMgYW4gZXh0ZXJuYWwgbW9kdWxlXG4vLyBpbiBQeXRob24gdGhyb3VnaCBTa3VscHQuXG4vL1xuLy8gVGhlIG1vZHVsZSBpcyBkZWZpbmVkIGluIGEgdmFyaWFibGUgY2FsbGVkICRidWlsdGlubW9kdWxlICh0aGF0IGlzIGFcbi8vIGZ1bmN0aW9uIGZvciBzb21lIHJlYXNvbikgaW4gd2hpY2ggYSB2YXJpYWJsZSBtb2QgaXMgY3JlYXRlZCBjb250YWluaW5nIGFsbFxuLy8gdGhlIG1lbWJlciBmdW5jdGlvbnMgYW5kIGNsYXNzZXMgb2YgdGhhdCBtb2R1bGUuXG5cbnZhciAkYnVpbHRpbm1vZHVsZSA9IGZ1bmN0aW9uIChuYW1lKSB7XG4gICAgdmFyIG1vZCA9IHt9O1xuXG4gICAgbW9kLmFkZCA9IG5ldyBTay5idWlsdGluLmZ1bmMoYnV0dG9uc19hZGQpO1xuXG4gICAgcmV0dXJuIG1vZDtcbn07XG5cbmZ1bmN0aW9uIGJ1dHRvbnNfYWRkKG5hbWUpIHtcbiAgICBsZXQgYnV0dG9uID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcImJ1dHRvblwiKTtcbiAgICB2YXIgbmFtZV9qcyA9IFNrLmZmaS5yZW1hcFRvSnMobmFtZSk7XG4gICAgYnV0dG9uLmNsYXNzTGlzdC5hZGQoXCJibHVlLWJ0blwiKTtcbiAgICBidXR0b24uaW5uZXJUZXh0ID0gbmFtZTtcbiAgICBidXR0b24ub25jbGljayA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgYnV0dG9uX2NsaWNrKG5hbWUpO1xuICAgIH07XG4gICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoXCJkeW5hbWljLWJ1dHRvbnNcIikuYXBwZW5kQ2hpbGQoYnV0dG9uKTtcblxuICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKFwiZHluYW1pYy1idXR0b25zXCIpLnN0eWxlLmRpc3BsYXkgPSBcIlwiO1xufVxuXG52YXIgYnV0dG9uX2NsaWNrID0gZnVuY3Rpb24gKG5hbWUpIHtcbiAgICB2YXIgbmFtZV9qcyA9IFNrLmZmaS5yZW1hcFRvSnMobmFtZSk7XG5cbiAgICAvLyBGb3IgdGhpcyB0byB3b3JrIHRoZSBmaXJzdCBlbGVtZW50IG9mIGUgbmVlZHMgdG8gYmUgYSBjb25zdGFudCBpbmRpY2F0aW5nXG4gICAgLy8gdGhpcyBldmVudCBpcyBmcm9tIGEgYnV0dG9uLCB0byBtYWtlIHN1cmUgaXQgaXMgdW5pcXVlIHdlIHVzZSBVU0VSRVZFTlRcbiAgICAvLyB0aGUgZGljdGlvbmFyeSBjYW4gdGhlbiBiZSBmaWxsZWQgd2l0aCB3aGF0ZXZlciBkYXRhIHdlIG5lZWQuXG4gICAgdmFyIGUgPSBbUHlnYW1lTGliLmNvbnN0YW50cy5VU0VSRVZFTlQsIHsga2V5OiBuYW1lIH1dO1xuICAgIFB5Z2FtZUxpYi5ldmVudFF1ZXVlLnVuc2hpZnQoZSk7XG59XG4iXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7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