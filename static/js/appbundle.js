var hedy = (() => {
  var __defProp = Object.defineProperty;
  var __markAsModule = (target) => __defProp(target, "__esModule", { value: true });
  var __export = (target, all) => {
    __markAsModule(target);
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };

  // static/js/index.ts
  var js_exports = {};
  __export(js_exports, {
    tryPaletteCode: () => tryPaletteCode
  });

  // static/js/modal.ts
  var Modal = class {
    constructor() {
      $("#modal-confirm-button").on("click", () => this.hide());
      $("#modal-no-button").on("click", () => this.hide());
      $("#modal-cancel-button").on("click", () => this.hide());
    }
    show() {
      $("#modal-mask").show();
      $("#modal-content").show();
      window.scrollTo(0, 0);
    }
    hide() {
      $("#modal-mask").hide();
      $("#modal-content").hide();
      $("#modal-alert").hide();
      $("#modal-prompt").hide();
      $("#modal-confirm").hide();
    }
    alert(message, timeoutMs) {
      $("#modal-alert-text").text(message);
      this.show();
      $("#modal-alert").show();
      if (timeoutMs)
        setTimeout(() => this.hide(), timeoutMs);
    }
    confirm(message, confirmCb) {
      $("#modal-confirm-text").text(message);
      this.show();
      $("#modal-confirm").show();
      $("#modal-yes-button").off("click").on("click", () => {
        this.hide();
        confirmCb();
      });
    }
    prompt(message, defaultValue, confirmCb) {
      $("#modal-prompt-text").text(message);
      this.show();
      $("#modal-prompt").show();
      if (defaultValue)
        $("#modal-prompt-input").val(defaultValue);
      $("#modal-ok-button").off("click").on("click", () => {
        this.hide();
        const value = $("#modal-prompt-input").val();
        if (typeof value === "string") {
          confirmCb(value);
        }
      });
    }
  };
  window.modal = new Modal();

  // static/js/syntaxModesRules.ts
  function baseRules() {
    return {
      gobble: [
        {
          regex: ".*",
          token: "text",
          next: "start"
        }
      ],
      expression_eol: finishLine([
        {
          regex: "'[^']*'",
          token: "constant.character"
        },
        {
          regex: "at random",
          token: "keyword"
        },
        {
          regex: "$",
          token: "text"
        }
      ])
    };
  }
  var LEVELS = [
    {
      name: "level1",
      rules: pipe(baseRules(), rule_print("gobble"), rule_turtle(), recognize("start", {
        regex: "echo ",
        token: "keyword",
        next: "gobble"
      }), recognize("start", {
        regex: "ask ",
        token: "keyword",
        next: "gobble"
      }))
    },
    {
      name: "level2",
      rules: pipe(baseRules(), rule_print("expression_eol"), rule_isAsk("gobble"), rule_is("gobble"), rule_turtle())
    },
    {
      name: "level3",
      rules: pipe(baseRules(), rule_turtle(), rule_print("expression_eol"), rule_isAsk(), rule_is())
    },
    {
      name: "level4",
      rules: pipe(baseRules(), rule_print(), rule_isAsk(), rule_is(), rule_ifElse(), rule_expressions())
    },
    {
      name: "level5",
      rules: pipe(baseRules(), rule_print(), rule_isAsk(), rule_is(), rule_ifElse(), rule_expressions(), rule_repeat())
    },
    {
      name: "level6",
      rules: pipe(baseRules(), rule_print(), rule_isAsk(), rule_is(), rule_ifElse(), rule_expressions(), rule_repeat(), rule_arithmetic())
    },
    {
      name: "level7",
      rules: pipe(baseRules(), rule_print(), rule_isAsk(), rule_is(), rule_ifElse(), rule_expressions(), rule_repeat(), rule_arithmetic())
    },
    {
      name: "level8and9",
      rules: pipe(baseRules(), rule_print(), rule_isAsk(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRange())
    },
    {
      name: "level10",
      rules: pipe(baseRules(), rule_print(), rule_isAsk(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRange())
    },
    {
      name: "level11",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level11",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level12",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level13",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level14",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level15",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level16",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level17and18",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level19",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level20",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level21",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    },
    {
      name: "level22",
      rules: pipe(baseRules(), rule_printParen(), rule_isInputParen(), rule_is(), rule_ifElse(), rule_expressions(), rule_arithmetic(), rule_forRangeParen())
    }
  ];
  function finishLine(rules) {
    const ret = [];
    for (const rule of rules) {
      if (rule.regex) {
        ret.push({
          regex: rule.regex + "$",
          token: rule.token,
          next: "start"
        });
      }
      ret.push(rule);
    }
    return ret;
  }
  function recognize(stateOrStates, ruleOrRules) {
    return (rules) => {
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
  function comp(...fns) {
    return (val) => {
      for (const fn of fns) {
        val = fn(val);
      }
      return val;
    };
  }
  function pipe(val, ...fns) {
    return comp(...fns)(val);
  }
  function rule_print(next) {
    return recognize("start", {
      regex: "print",
      token: "keyword",
      next: next != null ? next : "start"
    });
  }
  function rule_isAsk(next) {
    return recognize("start", {
      regex: "(\\w+)( is ask )",
      token: ["text", "keyword"],
      next: next != null ? next : "expression_eol"
    });
  }
  function rule_is(next) {
    return recognize("start", {
      regex: "(\\w+)( is )",
      token: ["text", "keyword"],
      next: next != null ? next : "expression_eol"
    });
  }
  function rule_printParen() {
    return recognize("start", {
      regex: "(print)(\\()",
      token: ["keyword", "paren.lparen"],
      next: "start"
    });
  }
  function rule_turtle() {
    return comp(recognize("start", {
      regex: "turn (left|right)?",
      token: "keyword",
      next: "start"
    }), recognize("start", {
      regex: "forward",
      token: "keyword",
      next: "start"
    }));
  }
  function rule_isInputParen() {
    return recognize("start", {
      regex: "(\\w+)( is input)(\\()",
      token: ["text", "keyword", "paren.lparen"],
      next: "start"
    });
  }
  function rule_expressions() {
    return comp(recognize("start", {
      regex: "'[^']*'",
      token: "constant.character"
    }), recognize("start", {
      regex: "at random",
      token: "keyword"
    }), recognize("start", {
      regex: "[, ]+",
      token: "punctuation.operator"
    }));
  }
  function rule_ifElse() {
    return comp(recognize("start", {
      regex: completeKeyword("if"),
      token: "keyword",
      next: "condition"
    }), recognize("start", {
      regex: completeKeyword("else"),
      token: "keyword"
    }), recognize("condition", {
      regex: completeKeyword("is"),
      token: "keyword",
      next: "start"
    }));
  }
  function rule_arithmetic() {
    return recognize(["start", "expression_eol"], [
      {
        regex: " \\* ",
        token: "keyword"
      },
      {
        regex: " \\+ ",
        token: "keyword"
      },
      {
        regex: " \\- ",
        token: "keyword"
      }
    ]);
  }
  function rule_repeat() {
    return recognize("start", {
      regex: "(repeat)( \\w+ )(times)",
      token: ["keyword", "text", "keyword"]
    });
  }
  function rule_forRange() {
    return recognize("start", {
      regex: "(for )(\\w+)( in range )(\\w+)( to )(\\w+)",
      token: ["keyword", "text", "keyword", "text", "keyword", "text"]
    });
  }
  function rule_forRangeParen() {
    return recognize("start", {
      regex: "(for )(\\w+)( in range)(\\()([\\s\\w]+)(,)([\\s\\w]+)(\\))",
      token: ["keyword", "text", "keyword", "paren.lparen", "text", "punctuation.operator", "text", "paren.rparen"]
    });
  }
  function loosenRules(rules) {
    for (const ruleSets of Object.values(rules)) {
      for (const rule of ruleSets) {
        if (rule.regex && !rule._loosened) {
          rule.regex = rule.regex.replace(/ /g, " +");
          rule._loosened = true;
        }
      }
    }
    return rules;
  }
  for (const level of LEVELS) {
    define("ace/mode/" + level.name, [], function(require2, exports, _module) {
      var oop = require2("ace/lib/oop");
      var TextMode = require2("ace/mode/text").Mode;
      var TextHighlightRules = require2("ace/mode/text_highlight_rules").TextHighlightRules;
      function ThisLevelHighlightRules() {
        this.$rules = loosenRules(level.rules);
        this.normalizeRules();
      }
      ;
      oop.inherits(ThisLevelHighlightRules, TextHighlightRules);
      function Mode() {
        this.HighlightRules = ThisLevelHighlightRules;
      }
      ;
      oop.inherits(Mode, TextMode);
      exports.Mode = Mode;
    });
  }
  function completeKeyword(keyword) {
    return "\\b" + keyword + "\\b";
  }

  // static/js/app.ts
  (function() {
    if (!window.State) {
      window.State = {};
    }
    initializeMainEditor($("#editor"));
    for (const preview of $(".turn-pre-into-ace pre").get()) {
      $(preview).addClass("text-lg rounded");
      const exampleEditor = turnIntoAceEditor(preview, true);
      exampleEditor.setOptions({ maxLines: Infinity });
      exampleEditor.setValue(exampleEditor.getValue().replace(/\n+$/, ""), -1);
      const buttonContainer = $("<div>").css({ position: "absolute", top: 5, right: 5, width: "auto" }).appendTo(preview);
      $("<button>").attr("title", UiMessages["try_button"]).css({ fontFamily: "sans-serif" }).addClass("green-btn").text("\u21E5").appendTo(buttonContainer).click(function() {
        var _a;
        (_a = window.editor) == null ? void 0 : _a.setValue(exampleEditor.getValue() + "\n");
      });
    }
    function initializeMainEditor($editor) {
      if (!$editor.length)
        return;
      var editor2 = window.editor = turnIntoAceEditor($editor.get(0), $editor.data("readonly"));
      const storage = window.sessionStorage;
      if (storage) {
        const levelKey = $editor.data("lskey");
        const loadedProgram = $editor.data("loaded-program");
        const programFromStorage = storage.getItem(levelKey);
        if (loadedProgram !== "True" && programFromStorage) {
          editor2.setValue(programFromStorage, 1);
        }
        editor2.on("blur", function(_e) {
          storage.setItem(levelKey, editor2.getValue());
        });
        editor2.on("change", function() {
          if ($("#inline-modal").is(":visible"))
            $("#inline-modal").hide();
          window.State.disable_run = false;
          $("#runit").css("background-color", "");
          window.State.unsaved_changes = true;
        });
      }
      window.onbeforeunload = function() {
        if (window.State.unsaved_changes) {
          if (!window.State.no_unload_prompt)
            return window.auth.texts.unsaved_changes;
        }
      };
      let altPressed;
      window.addEventListener("keydown", function(ev) {
        const keyCode = ev.keyCode;
        if (keyCode === 18) {
          altPressed = true;
          return;
        }
        if (keyCode === 13 && altPressed) {
          if (!window.State.level || !window.State.lang) {
            throw new Error("Oh no");
          }
          runit(window.State.level, window.State.lang, function() {
            $("#output").focus();
          });
        }
        if (keyCode === 37 && document.activeElement === document.getElementById("output")) {
          editor2.focus();
          editor2.navigateFileEnd();
        }
      });
      window.addEventListener("keyup", function(ev) {
        const keyCode = ev.keyCode;
        if (keyCode === 18) {
          altPressed = false;
          return;
        }
      });
    }
    function turnIntoAceEditor(element, isReadOnly) {
      const editor2 = ace.edit(element);
      editor2.setTheme("ace/theme/monokai");
      if (isReadOnly) {
        editor2.setOptions({
          readOnly: true,
          showGutter: false,
          showPrintMargin: false,
          highlightActiveLine: false
        });
      }
      var highlighter = 1;
      if (highlighter == 1) {
        const modeExceptions = {
          "8": "ace/mode/level8and9",
          "9": "ace/mode/level8and9",
          "17": "ace/mode/level17and18",
          "18": "ace/mode/level17and18",
          "21": "ace/mode/level21and22",
          "22": "ace/mode/level21and22"
        };
        if (window.State.level) {
          const mode = modeExceptions[window.State.level] || `ace/mode/level${window.State.level}`;
          editor2.session.setMode(mode);
        }
      }
      return editor2;
    }
  })();
  function reloadOnExpiredSession() {
    if (!window.auth.profile || window.auth.profile.session_expires_at > Date.now())
      return false;
    location.reload();
    return true;
  }
  function runit(level, lang, cb) {
    if (window.State.disable_run)
      return window.modal.alert(window.auth.texts.answer_question);
    if (reloadOnExpiredSession())
      return;
    error.hide();
    try {
      level = level.toString();
      var editor2 = ace.edit("editor");
      var code = editor2.getValue();
      console.log("Original program:\n", code);
      $.ajax({
        type: "POST",
        url: "/parse",
        data: JSON.stringify({
          level,
          code,
          lang,
          read_aloud: !!$("#speak_dropdown").val(),
          adventure_name: window.State.adventure_name
        }),
        contentType: "application/json",
        dataType: "json"
      }).done(function(response) {
        console.log("Response", response);
        if (response.Warning) {
          error.showWarning(ErrorMessages["Transpile_warning"], response.Warning);
        }
        if (response.Error) {
          error.show(ErrorMessages["Transpile_error"], response.Error);
          return;
        }
        runPythonProgram(response.Code, response.has_turtle, cb).catch(function(err) {
          console.log(err);
          error.show(ErrorMessages["Execute_error"], err.message);
          reportClientError(level, code, err.message);
        });
      }).fail(function(xhr) {
        console.error(xhr);
        if (xhr.readyState < 4) {
          error.show(ErrorMessages["Connection_error"], ErrorMessages["CheckInternet"]);
        } else {
          error.show(ErrorMessages["Other_error"], ErrorMessages["ServerError"]);
        }
      });
    } catch (e) {
      console.error(e);
      error.show(ErrorMessages["Other_error"], e.message);
    }
  }
  function tryPaletteCode(exampleCode) {
    var editor2 = ace.edit("editor");
    var MOVE_CURSOR_TO_END = 1;
    editor2.setValue(exampleCode + "\n", MOVE_CURSOR_TO_END);
    window.State.unsaved_changes = false;
  }
  window.saveit = function saveit2(level, lang, name, code, cb) {
    error.hide();
    if (reloadOnExpiredSession())
      return;
    try {
      if (!window.auth.profile) {
        return window.modal.confirm(window.auth.texts.save_prompt, function() {
          if (window.State && window.State.adventure_name)
            level = [level, window.State.adventure_name];
          localStorage.setItem("hedy-first-save", JSON.stringify([level, lang, name, code]));
          window.location.pathname = "/login";
        });
      }
      window.State.unsaved_changes = false;
      var adventure_name = window.State.adventure_name;
      if (level instanceof Array) {
        adventure_name = level[1];
        level = level[0];
      }
      $.ajax({
        type: "POST",
        url: "/programs",
        data: JSON.stringify({
          level,
          lang,
          name,
          code,
          adventure_name
        }),
        contentType: "application/json",
        dataType: "json"
      }).done(function(response) {
        if (cb)
          return response.Error ? cb(response) : cb(null, response);
        if (response.Warning) {
          error.showWarning(ErrorMessages["Transpile_warning"], response.Warning);
        }
        if (response.Error) {
          error.show(ErrorMessages["Transpile_error"], response.Error);
          return;
        }
        window.modal.alert(window.auth.texts.save_success_detail, 4e3);
        $("#program_name").val(response.name);
        window.State.adventures.map(function(adventure) {
          if (adventure.short_name === (adventure_name || "level")) {
            adventure.loaded_program = { name: response.name, code };
          }
        });
      }).fail(function(err) {
        console.error(err);
        error.show(ErrorMessages["Connection_error"], JSON.stringify(err));
        if (err.status === 403) {
          localStorage.setItem("hedy-first-save", JSON.stringify([adventure_name ? [level, adventure_name] : level, lang, name, code]));
          localStorage.setItem("hedy-save-redirect", "hedy");
          window.location.pathname = "/login";
        }
      });
    } catch (e) {
      console.error(e);
      error.show(ErrorMessages["Other_error"], e.message);
    }
  };
  function viewProgramLink(programId) {
    return window.location.origin + "/hedy/" + programId + "/view";
  }
  window.share_program = function share_program(level, lang, id, Public, reload) {
    if (!window.auth.profile)
      return window.modal.alert(window.auth.texts.must_be_logged);
    var share = function(id2) {
      $.ajax({
        type: "POST",
        url: "/programs/share",
        data: JSON.stringify({
          id: id2,
          public: Public
        }),
        contentType: "application/json",
        dataType: "json"
      }).done(function(response) {
        if (Public)
          window.copy_to_clipboard(viewProgramLink(id2), true);
        window.modal.alert(Public ? window.auth.texts.share_success_detail : window.auth.texts.unshare_success_detail, 4e3);
        if (reload)
          setTimeout(function() {
            location.reload();
          }, 1e3);
      }).fail(function(err) {
        console.error(err);
        error.show(ErrorMessages["Connection_error"], JSON.stringify(err));
      });
    };
    if (id !== true)
      return share(id);
    var name = $("#program_name").val();
    var code = ace.edit("editor").getValue();
    return saveit(level, lang, name, code, function(err, resp) {
      if (err && err.Warning)
        return error.showWarning(ErrorMessages["Transpile_warning"], err.Warning);
      if (err && err.Error)
        return error.show(ErrorMessages["Transpile_error"], err.Error);
      share(resp.id);
    });
  };
  window.copy_to_clipboard = function copy_to_clipboard(string, noAlert) {
    var el = document.createElement("textarea");
    el.value = string;
    el.setAttribute("readonly", "");
    el.style.position = "absolute";
    el.style.left = "-9999px";
    document.body.appendChild(el);
    var selected = document.getSelection().rangeCount > 0 ? document.getSelection().getRangeAt(0) : false;
    el.select();
    document.execCommand("copy");
    document.body.removeChild(el);
    if (selected) {
      document.getSelection().removeAllRanges();
      document.getSelection().addRange(selected);
    }
    if (!noAlert)
      window.modal.alert(window.auth.texts.copy_clipboard, 4e3);
  };
  function reportClientError(level, code, client_error) {
    $.ajax({
      type: "POST",
      url: "/report_error",
      data: JSON.stringify({
        level,
        code,
        page: window.location.href,
        client_error
      }),
      contentType: "application/json",
      dataType: "json"
    });
  }
  window.onerror = function reportClientException(message, source, line_number, column_number, error2) {
    $.ajax({
      type: "POST",
      url: "/client_exception",
      data: JSON.stringify({
        message,
        source,
        line_number,
        column_number,
        error: error2,
        url: window.location.href,
        user_agent: navigator.userAgent
      }),
      contentType: "application/json",
      dataType: "json"
    });
  };
  function runPythonProgram(code, hasTurtle, cb) {
    const outputDiv = $("#output");
    outputDiv.empty();
    Sk.pre = "output";
    const turtleConfig = Sk.TurtleGraphics || (Sk.TurtleGraphics = {});
    turtleConfig.target = "turtlecanvas";
    turtleConfig.width = 400;
    turtleConfig.height = 300;
    turtleConfig.worldWidth = 400;
    turtleConfig.worldHeight = 300;
    if (!hasTurtle) {
      $("#turtlecanvas").empty();
    }
    Sk.configure({
      output: outf,
      read: builtinRead,
      inputfun: inputFromInlineModal,
      inputfunTakesPrompt: true,
      __future__: Sk.python3
    });
    return Sk.misceval.asyncToPromise(function() {
      return Sk.importMainWithBody("<stdin>", false, code, true);
    }).then(function(_mod) {
      console.log("Program executed");
      if (cb)
        cb();
    }).catch(function(err) {
      console.log(err);
      const errorMessage = errorMessageFromSkulptError(err) || JSON.stringify(err);
      throw new Error(errorMessage);
    });
    function errorMessageFromSkulptError(err) {
      const message = err.args && err.args.v && err.args.v[0] && err.args.v[0].v;
      return message;
    }
    function addToOutput(text, color) {
      $("<span>").text(text).css({ color }).appendTo(outputDiv);
    }
    function outf(text) {
      addToOutput(text, "white");
      speak(text);
    }
    function builtinRead(x) {
      if (Sk.builtinFiles === void 0 || Sk.builtinFiles["files"][x] === void 0)
        throw "File not found: '" + x + "'";
      return Sk.builtinFiles["files"][x];
    }
    function inputFromTerminal(prompt) {
      return new Promise(function(ok) {
        addToOutput(prompt + "\n", "white");
        const input = $("<input>").attr("placeholder", "Typ hier je antwoord").appendTo(outputDiv).focus();
        input.on("keypress", function(e) {
          if (e.which == 13) {
            const text = input.val();
            input.remove();
            addToOutput(text + "\n", "yellow");
            ok(text);
          }
        });
      });
    }
    function inputFromInlineModal(prompt) {
      return new Promise(function(ok) {
        window.State.disable_run = true;
        $("#runit").css("background-color", "gray");
        const input = $('#inline-modal input[type="text"]');
        $("#inline-modal .caption").text(prompt);
        input.val("");
        input[0].placeholder = prompt;
        speak(prompt);
        setTimeout(function() {
          input.focus();
        }, 0);
        $("#inline-modal form").one("submit", function(event) {
          window.State.disable_run = false;
          $("#runit").css("background-color", "");
          event.preventDefault();
          $("#inline-modal").hide();
          ok(input.val());
          $("#output").focus();
          return false;
        });
        $("#inline-modal").show();
      });
    }
  }
  var error = {
    hide() {
      $("#errorbox").hide();
      $("#warningbox").hide();
      if ($("#editor").length)
        editor.resize();
    },
    showWarning(caption, message) {
      $("#warningbox .caption").text(caption);
      $("#warningbox .details").text(message);
      $("#warningbox").show();
      if ($("#editor").length)
        editor.resize();
    },
    show(caption, message) {
      $("#errorbox .caption").text(caption);
      $("#errorbox .details").text(message);
      $("#errorbox").show();
      if ($("#editor").length)
        editor.resize();
    }
  };
  (function() {
    window.speak = function speak2(text) {
      var selectedURI = $("#speak_dropdown").val();
      if (!selectedURI) {
        return;
      }
      var voice = window.speechSynthesis.getVoices().filter((v) => v.voiceURI === selectedURI)[0];
      if (voice) {
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = voice;
        utterance.rate = 0.9;
        speechSynthesis.speak(utterance);
      }
    };
    if (!window.speechSynthesis) {
      return;
    }
    if (!window.State.lang) {
      return;
    }
    let attempts = 0;
    const timer = setInterval(function() {
      attempts += 1;
      const voices = findVoices(window.State.lang);
      if (voices.length > 0) {
        for (const voice of voices) {
          $("#speak_dropdown").append($("<option>").attr("value", voice.voiceURI).text("\u{1F4E3} " + voice.name));
        }
        $("#speak_container").show();
        clearInterval(timer);
      }
      if (attempts >= 20) {
        clearInterval(timer);
      }
    }, 100);
    function findVoices(lang) {
      const simpleLang = lang.match(/^([a-z]+)/i)[1];
      if (!window.speechSynthesis) {
        return [];
      }
      return window.speechSynthesis.getVoices().filter((voice) => voice.lang.startsWith(simpleLang));
    }
  })();
  window.create_class = function create_class() {
    window.modal.prompt(window.auth.texts.class_name_prompt, "", function(class_name) {
      $.ajax({
        type: "POST",
        url: "/class",
        data: JSON.stringify({
          name: class_name
        }),
        contentType: "application/json",
        dataType: "json"
      }).done(function(response) {
        location.reload();
      }).fail(function(err) {
        console.error(err);
        error.show(ErrorMessages["Connection_error"], JSON.stringify(err));
      });
    });
  };
  window.rename_class = function rename_class(id) {
    window.modal.prompt(window.auth.texts.class_name_prompt, "", function(class_name) {
      $.ajax({
        type: "PUT",
        url: "/class/" + id,
        data: JSON.stringify({
          name: class_name
        }),
        contentType: "application/json",
        dataType: "json"
      }).done(function(response) {
        location.reload();
      }).fail(function(err) {
        console.error(err);
        error.show(ErrorMessages["Connection_error"], JSON.stringify(err));
      });
    });
  };
  window.delete_class = function delete_class(id) {
    window.modal.confirm(window.auth.texts.delete_class_prompt, function() {
      $.ajax({
        type: "DELETE",
        url: "/class/" + id,
        contentType: "application/json",
        dataType: "json"
      }).done(function(response) {
        window.location.pathname = "/for-teachers";
      }).fail(function(err) {
        console.error(err);
        error.show(ErrorMessages["Connection_error"], JSON.stringify(err));
      });
    });
  };
  window.join_class = function join_class(link, name, noRedirect) {
    if (!window.auth.profile) {
      return window.modal.confirm(window.auth.texts.join_prompt, function() {
        localStorage.setItem("hedy-join", JSON.stringify({ link, name }));
        window.location.pathname = "/login";
        return;
      });
    }
    $.ajax({
      type: "GET",
      url: link
    }).done(function(response) {
      window.modal.alert(window.auth.texts.class_join_confirmation + " " + name);
      if (!noRedirect)
        window.location.pathname = "/programs";
    }).fail(function(err) {
      console.error(err);
      error.show(ErrorMessages["Connection_error"], JSON.stringify(err));
    });
  };
  window.remove_student = function delete_class2(class_id, student_id) {
    window.modal.confirm(window.auth.texts.remove_student_prompt, function() {
      $.ajax({
        type: "DELETE",
        url: "/class/" + class_id + "/student/" + student_id,
        contentType: "application/json",
        dataType: "json"
      }).done(function(response) {
        location.reload();
      }).fail(function(err) {
        console.error(err);
        error.show(ErrorMessages["Connection_error"], JSON.stringify(err));
      });
    });
  };
  window.prompt_unsaved = function prompt_unsaved(cb) {
    if (!window.State.unsaved_changes)
      return cb();
    window.State.no_unload_prompt = true;
    window.modal.confirm(window.auth.texts.unsaved_changes, cb);
  };

  // static/js/auth.ts
  var countries = { "AF": "Afghanistan", "AX": "\xC5land Islands", "AL": "Albania", "DZ": "Algeria", "AS": "American Samoa", "AD": "Andorra", "AO": "Angola", "AI": "Anguilla", "AQ": "Antarctica", "AG": "Antigua and Barbuda", "AR": "Argentina", "AM": "Armenia", "AW": "Aruba", "AU": "Australia", "AT": "Austria", "AZ": "Azerbaijan", "BS": "Bahamas", "BH": "Bahrain", "BD": "Bangladesh", "BB": "Barbados", "BY": "Belarus", "BE": "Belgium", "BZ": "Belize", "BJ": "Benin", "BM": "Bermuda", "BT": "Bhutan", "BO": "Bolivia, Plurinational State of", "BQ": "Bonaire, Sint Eustatius and Saba", "BA": "Bosnia and Herzegovina", "BW": "Botswana", "BV": "Bouvet Island", "BR": "Brazil", "IO": "British Indian Ocean Territory", "BN": "Brunei Darussalam", "BG": "Bulgaria", "BF": "Burkina Faso", "BI": "Burundi", "KH": "Cambodia", "CM": "Cameroon", "CA": "Canada", "CV": "Cape Verde", "KY": "Cayman Islands", "CF": "Central African Republic", "TD": "Chad", "CL": "Chile", "CN": "China", "CX": "Christmas Island", "CC": "Cocos (Keeling) Islands", "CO": "Colombia", "KM": "Comoros", "CG": "Congo", "CD": "Congo, the Democratic Republic of the", "CK": "Cook Islands", "CR": "Costa Rica", "CI": "C\xF4te d'Ivoire", "HR": "Croatia", "CU": "Cuba", "CW": "Cura\xE7ao", "CY": "Cyprus", "CZ": "Czech Republic", "DK": "Denmark", "DJ": "Djibouti", "DM": "Dominica", "DO": "Dominican Republic", "EC": "Ecuador", "EG": "Egypt", "SV": "El Salvador", "GQ": "Equatorial Guinea", "ER": "Eritrea", "EE": "Estonia", "ET": "Ethiopia", "FK": "Falkland Islands (Malvinas)", "FO": "Faroe Islands", "FJ": "Fiji", "FI": "Finland", "FR": "France", "GF": "French Guiana", "PF": "French Polynesia", "TF": "French Southern Territories", "GA": "Gabon", "GM": "Gambia", "GE": "Georgia", "DE": "Germany", "GH": "Ghana", "GI": "Gibraltar", "GR": "Greece", "GL": "Greenland", "GD": "Grenada", "GP": "Guadeloupe", "GU": "Guam", "GT": "Guatemala", "GG": "Guernsey", "GN": "Guinea", "GW": "Guinea-Bissau", "GY": "Guyana", "HT": "Haiti", "HM": "Heard Island and McDonald Islands", "VA": "Holy See (Vatican City State)", "HN": "Honduras", "HK": "Hong Kong", "HU": "Hungary", "IS": "Iceland", "IN": "India", "ID": "Indonesia", "IR": "Iran, Islamic Republic of", "IQ": "Iraq", "IE": "Ireland", "IM": "Isle of Man", "IL": "Israel", "IT": "Italy", "JM": "Jamaica", "JP": "Japan", "JE": "Jersey", "JO": "Jordan", "KZ": "Kazakhstan", "KE": "Kenya", "KI": "Kiribati", "KP": "Korea, Democratic People's Republic of", "KR": "Korea, Republic of", "KW": "Kuwait", "KG": "Kyrgyzstan", "LA": "Lao People's Democratic Republic", "LV": "Latvia", "LB": "Lebanon", "LS": "Lesotho", "LR": "Liberia", "LY": "Libya", "LI": "Liechtenstein", "LT": "Lithuania", "LU": "Luxembourg", "MO": "Macao", "MK": "Macedonia, the Former Yugoslav Republic of", "MG": "Madagascar", "MW": "Malawi", "MY": "Malaysia", "MV": "Maldives", "ML": "Mali", "MT": "Malta", "MH": "Marshall Islands", "MQ": "Martinique", "MR": "Mauritania", "MU": "Mauritius", "YT": "Mayotte", "MX": "Mexico", "FM": "Micronesia, Federated States of", "MD": "Moldova, Republic of", "MC": "Monaco", "MN": "Mongolia", "ME": "Montenegro", "MS": "Montserrat", "MA": "Morocco", "MZ": "Mozambique", "MM": "Myanmar", "NA": "Namibia", "NR": "Nauru", "NP": "Nepal", "NL": "Netherlands", "NC": "New Caledonia", "NZ": "New Zealand", "NI": "Nicaragua", "NE": "Niger", "NG": "Nigeria", "NU": "Niue", "NF": "Norfolk Island", "MP": "Northern Mariana Islands", "NO": "Norway", "OM": "Oman", "PK": "Pakistan", "PW": "Palau", "PS": "Palestine, State of", "PA": "Panama", "PG": "Papua New Guinea", "PY": "Paraguay", "PE": "Peru", "PH": "Philippines", "PN": "Pitcairn", "PL": "Poland", "PT": "Portugal", "PR": "Puerto Rico", "QA": "Qatar", "RE": "R\xE9union", "RO": "Romania", "RU": "Russian Federation", "RW": "Rwanda", "BL": "Saint Barth\xE9lemy", "SH": "Saint Helena, Ascension and Tristan da Cunha", "KN": "Saint Kitts and Nevis", "LC": "Saint Lucia", "MF": "Saint Martin (French part)", "PM": "Saint Pierre and Miquelon", "VC": "Saint Vincent and the Grenadines", "WS": "Samoa", "SM": "San Marino", "ST": "Sao Tome and Principe", "SA": "Saudi Arabia", "SN": "Senegal", "RS": "Serbia", "SC": "Seychelles", "SL": "Sierra Leone", "SG": "Singapore", "SX": "Sint Maarten (Dutch part)", "SK": "Slovakia", "SI": "Slovenia", "SB": "Solomon Islands", "SO": "Somalia", "ZA": "South Africa", "GS": "South Georgia and the South Sandwich Islands", "SS": "South Sudan", "ES": "Spain", "LK": "Sri Lanka", "SD": "Sudan", "SR": "Suriname", "SJ": "Svalbard and Jan Mayen", "SZ": "Swaziland", "SE": "Sweden", "CH": "Switzerland", "SY": "Syrian Arab Republic", "TW": "Taiwan, Province of China", "TJ": "Tajikistan", "TZ": "Tanzania, United Republic of", "TH": "Thailand", "TL": "Timor-Leste", "TG": "Togo", "TK": "Tokelau", "TO": "Tonga", "TT": "Trinidad and Tobago", "TN": "Tunisia", "TR": "Turkey", "TM": "Turkmenistan", "TC": "Turks and Caicos Islands", "TV": "Tuvalu", "UG": "Uganda", "UA": "Ukraine", "AE": "United Arab Emirates", "GB": "United Kingdom", "US": "United States", "UM": "United States Minor Outlying Islands", "UY": "Uruguay", "UZ": "Uzbekistan", "VU": "Vanuatu", "VE": "Venezuela, Bolivarian Republic of", "VN": "Viet Nam", "VG": "Virgin Islands, British", "VI": "Virgin Islands, U.S.", "WF": "Wallis and Futuna", "EH": "Western Sahara", "YE": "Yemen", "ZM": "Zambia", "ZW": "Zimbabwe" };
  window.auth = {
    texts: AuthMessages,
    entityify: function(string) {
      return string.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;").replace(/`/g, "&#96;");
    },
    emailRegex: /^(([a-zA-Z0-9_+\.\-]+)@([\da-zA-Z\.\-]+)\.([a-zA-Z\.]{2,6})\s*)$/,
    redirect: function(where) {
      where = "/" + where;
      window.location.pathname = where;
    },
    logout: function() {
      $.ajax({ type: "POST", url: "/auth/logout" }).done(function() {
        auth.redirect("login");
      });
    },
    destroy: function() {
      window.modal.confirm(auth.texts.are_you_sure, function() {
        $.ajax({ type: "POST", url: "/auth/destroy" }).done(function() {
          auth.redirect("");
        });
      });
    },
    error: function(message, element, id) {
      $(id || "#error").html(message);
      $(id || "#error").css("display", "block");
      if (element)
        $("#" + element).css("border", "solid 1px red");
    },
    clear_error: function(id) {
      $(id || "#error").html("");
      $(id || "#error").css("display", "none");
      $("form *").css("border", "");
    },
    success: function(message, id) {
      $("#error").css("display", "none");
      $(id || "#success").html(message);
      $(id || "#success").css("display", "block");
    },
    submit: function(op) {
      var values = {};
      $("form.auth *").map(function(k, el) {
        if (el.id)
          values[el.id] = el.value;
      });
      if (op === "signup") {
        if (!values.username)
          return auth.error(auth.texts.please_username, "username");
        values.username = values.username.trim();
        if (values.username.length < 3)
          return auth.error(auth.texts.username_three, "username");
        if (values.username.match(/:|@/))
          return auth.error(auth.texts.username_special, "username");
        if (!values.password)
          return auth.error(auth.texts.please_password, "password");
        if (values.password.length < 6)
          return auth.error(auth.texts.password_six, "password");
        if (!values.email.match(window.auth.emailRegex))
          return auth.error(auth.texts.valid_email, "email");
        if (values.email !== values.mail_repeat)
          return auth.error(auth.texts.repeat_match_email, "mail_repeat");
        if (values.password !== values.password_repeat)
          return auth.error(auth.texts.repeat_match_password, "password_repeat");
        if (values.birth_year) {
          values.birth_year = parseInt(values.birth_year);
          if (!values.birth_year || values.birth_year < 1900 || values.birth_year > new Date().getFullYear())
            return auth.error(auth.texts.valid_year + new Date().getFullYear(), "birth_year");
        }
        var payload = {};
        ["username", "email", "password", "birth_year", "country", "gender", "subscribe"].map(function(k) {
          if (!values[k])
            return;
          if (k === "birth_year")
            payload[k] = parseInt(values[k]);
          else if (k === "subscribe")
            payload[k] = $("#subscribe").prop("checked");
          else
            payload[k] = values[k];
        });
        payload.prog_experience = $("input[name=has_experience]:checked").val();
        var languages = [];
        if ($("#languages").is(":visible"))
          $("input[name=languages]").filter(":checked").map(function(v) {
            languages.push($(this).val());
          });
        if (languages.length)
          payload.experience_languages = languages;
        $.ajax({ type: "POST", url: "/auth/signup", data: JSON.stringify(payload), contentType: "application/json; charset=utf-8" }).done(function() {
          auth.success(auth.texts.signup_success);
          window.auth.profile = { session_expires_at: Date.now() + 1e3 * 60 * 60 * 24 };
          var savedProgram = localStorage.getItem("hedy-first-save");
          var joinClass = localStorage.getItem("hedy-join");
          if (!savedProgram) {
            if (!joinClass)
              return auth.redirect("programs");
            joinClass = JSON.parse(joinClass);
            localStorage.removeItem("hedy-join");
            return window.join_class(joinClass.link, joinClass.name);
          }
          savedProgram = JSON.parse(savedProgram);
          window.saveit(savedProgram[0], savedProgram[1], savedProgram[2], savedProgram[3], function() {
            localStorage.removeItem("hedy-first-save");
            if (joinClass) {
              joinClass = JSON.parse(joinClass);
              localStorage.removeItem("hedy-join");
              window.join_class(joinClass.link, joinClass.name, true);
            }
            var redirect = localStorage.getItem("hedy-save-redirect");
            if (redirect)
              localStorage.removeItem("hedy-save-redirect");
            auth.redirect(redirect || "programs");
          });
        }).fail(function(response) {
          var error2 = response.responseText || "";
          if (error2.match("email"))
            auth.error(auth.texts.exists_email);
          else if (error2.match("username"))
            auth.error(auth.texts.exists_username);
          else
            auth.error(auth.texts.ajax_error);
        });
      }
      if (op === "login") {
        if (!values.username)
          return auth.error(auth.texts.please_username_email, "username");
        if (!values.password)
          return auth.error(auth.texts.please_password, "password");
        auth.clear_error();
        $.ajax({ type: "POST", url: "/auth/login", data: JSON.stringify({ username: values.username, password: values.password }), contentType: "application/json; charset=utf-8" }).done(function() {
          window.auth.profile = { session_expires_at: Date.now() + 1e3 * 60 * 60 * 24 };
          var savedProgram = localStorage.getItem("hedy-first-save");
          var joinClass = localStorage.getItem("hedy-join");
          if (!savedProgram) {
            if (!joinClass)
              return auth.redirect("programs");
            joinClass = JSON.parse(joinClass);
            localStorage.removeItem("hedy-join");
            return window.join_class(joinClass.link, joinClass.name);
          }
          savedProgram = JSON.parse(savedProgram);
          window.saveit(savedProgram[0], savedProgram[1], savedProgram[2], savedProgram[3], function() {
            localStorage.removeItem("hedy-first-save");
            if (joinClass) {
              joinClass = JSON.parse(joinClass);
              localStorage.removeItem("hedy-join");
              window.join_class(joinClass.link, joinClass.name, true);
            }
            var redirect = localStorage.getItem("hedy-save-redirect");
            if (redirect)
              localStorage.removeItem("hedy-save-redirect");
            auth.redirect(redirect || "programs");
          });
        }).fail(function(response) {
          if (response.status === 403) {
            auth.error(auth.texts.invalid_username_password + " " + auth.texts.no_account + ` &nbsp;<button class="green-btn" onclick="auth.redirect ('signup')">` + auth.texts.create_account + "</button>");
            $("#create-account").hide();
            localStorage.setItem("hedy-login-username", values.username);
          } else
            auth.error(auth.texts.ajax_error);
        });
      }
      if (op === "profile") {
        if (!values.email.match(window.auth.emailRegex))
          return auth.error(auth.texts.valid_email, "email");
        if (values.birth_year) {
          values.birth_year = parseInt(values.birth_year);
          if (!values.birth_year || values.birth_year < 1900 || values.birth_year > new Date().getFullYear())
            return auth.error(auth.texts.valid_year + new Date().getFullYear(), "birth_year");
        }
        var payload = {};
        ["email", "birth_year", "country", "gender"].map(function(k) {
          if (!values[k])
            return;
          if (k === "birth_year")
            payload[k] = parseInt(values[k]);
          payload[k] = values[k];
        });
        payload.prog_experience = $("input[name=has_experience]:checked").val();
        var languages = [];
        if ($("#languages").is(":visible"))
          $("input[name=languages]").filter(":checked").map(function(v) {
            languages.push($(this).val());
          });
        payload.experience_languages = languages;
        auth.clear_error();
        $.ajax({ type: "POST", url: "/profile", data: JSON.stringify(payload), contentType: "application/json; charset=utf-8" }).done(function() {
          auth.success(auth.texts.profile_updated);
        }).fail(function(response) {
          auth.error(auth.texts.ajax_error);
        });
      }
      if (op === "change_password") {
        if (!values.password)
          return auth.error(auth.texts.please_password, "password", "#error-password");
        if (values.password.length < 6)
          return auth.error(auth.texts.password_six, "password", "#error-password");
        if (values.password !== values.password_repeat)
          return auth.error(auth.texts.repeat_match, "password_repeat", "#error-password");
        var payload = { old_password: values.old_password, new_password: values.password };
        auth.clear_error("#error-password");
        $.ajax({ type: "POST", url: "/auth/change_password", data: JSON.stringify(payload), contentType: "application/json; charset=utf-8" }).done(function() {
          auth.success(auth.texts.password_updated, "#success-password");
          $("#old_password").val("");
          $("#password").val("");
          $("#password_repeat").val("");
        }).fail(function(response) {
          if (response.status === 403)
            auth.error(auth.texts.invalid_password, null, "#error-password");
          else
            auth.error(auth.texts.ajax_error, null, "#error-password");
        });
      }
      if (op === "recover") {
        if (!values.username)
          return auth.error(auth.texts.please_username, "username");
        var payload = { username: values.username };
        auth.clear_error();
        $.ajax({ type: "POST", url: "/auth/recover", data: JSON.stringify(payload), contentType: "application/json; charset=utf-8" }).done(function() {
          auth.success(auth.texts.sent_password_recovery);
          $("#username").val("");
        }).fail(function(response) {
          if (response.status === 403)
            auth.error(auth.texts.invalid_username);
          else
            auth.error(auth.texts.ajax_error);
        });
      }
      if (op === "reset") {
        if (!values.password)
          return auth.error(auth.texts.please_password, "password");
        if (values.password.length < 6)
          return auth.eror(auth.texts.password_six, "password");
        if (values.password !== values.password_repeat)
          return auth.error(auth.texts.repeat_match, "password_repeat");
        var payload = { username: auth.reset.username, token: auth.reset.token, password: values.password };
        auth.clear_error();
        $.ajax({ type: "POST", url: "/auth/reset", data: JSON.stringify(payload), contentType: "application/json; charset=utf-8" }).done(function() {
          auth.success(auth.texts.password_resetted);
          $("#password").val("");
          $("#password_repeat").val("");
          delete auth.reset;
          auth.redirect("login");
        }).fail(function(response) {
          if (response.status === 403)
            auth.error(auth.texts.invalid_reset_link);
          else
            auth.error(auth.texts.ajax_error);
        });
      }
    },
    markAsTeacher: function(username, is_teacher) {
      $.ajax({ type: "POST", url: "/admin/markAsTeacher", data: JSON.stringify({ username, is_teacher }), contentType: "application/json; charset=utf-8" }).done(function() {
        window.modal.alert(["User", username, "successfully", is_teacher ? "marked" : "unmarked", "as teacher"].join(" "), 4e3);
        location.reload();
      }).fail(function(error2) {
        console.log(error2);
        window.modal.alert(["Error when", is_teacher ? "marking" : "unmarking", "user", username, "as teacher"].join(" "));
      });
    },
    changeUserEmail: function(username, email) {
      window.modal.prompt("Please enter the corrected email", email, function(correctedEmail) {
        if (correctedEmail === email)
          return;
        if (!correctedEmail.match(window.auth.emailRegex))
          return window.modal.alert("Please enter a valid email.");
        $.ajax({ type: "POST", url: "/admin/changeUserEmail", data: JSON.stringify({ username, email: correctedEmail }), contentType: "application/json; charset=utf-8" }).done(function() {
          window.modal.alert(["Successfully changed the email for User", username, "to", correctedEmail].join(" "));
          location.reload();
        }).fail(function(error2) {
          console.log(error2);
          window.modal.alert(["Error when changing the email for User", username].join(" "));
        });
      });
    }
  };
  if ($("#country")) {
    html = '<option value="">Select</option>';
    Object.keys(countries).map(function(code) {
      html += '<option value="' + code + '">' + countries[code] + "</option>";
    });
    $("#country").html(html);
  }
  var html;
  $(".auth input").get().map(function(el) {
    el.addEventListener("input", auth.clear_error);
  });
  $.ajax({ type: "GET", url: "/profile" }).done(function(response) {
    if (["/signup", "/login"].indexOf(window.location.pathname) !== -1)
      auth.redirect("my-profile");
    auth.profile = response;
    if ($("#profile").html()) {
      $("#username").html(response.username);
      $("#email").val(response.email);
      $("#birth_year").val(response.birth_year);
      $("#gender").val(response.gender);
      $("#country").val(response.country);
      if (response.prog_experience) {
        $('input[name=has_experience][value="' + response.prog_experience + '"]').prop("checked", true);
        if (response.prog_experience === "yes")
          $("#languages").show();
      }
      (response.experience_languages || []).map(function(lang) {
        $('input[name=languages][value="' + lang + '"]').prop("checked", true);
      });
      $("#student_classes ul").html((response.student_classes || []).map(function(Class) {
        return "<li>" + auth.entityify(Class.name) + "</li>";
      }).join(""));
    }
  }).fail(function(response) {
    if (window.location.pathname.indexOf(["/my-profile"]) !== -1)
      auth.redirect("login");
  });
  if (window.location.pathname === "/reset") {
    query = window.location.search.slice(1).split("&");
    params = {};
    query.map(function(item) {
      item = item.split("=");
      params[item[0]] = decodeURIComponent(item[1]);
    });
    if (!params.username || !params.token)
      auth.redirect("recover");
    else
      auth.reset = params;
  }
  var query;
  var params;
  if (window.location.pathname === "/signup") {
    login_username = localStorage.getItem("hedy-login-username");
    if (login_username) {
      localStorage.removeItem("hedy-login-username");
      if (login_username.match("@"))
        $("#email").val(login_username);
      else
        $("#username").val(login_username);
    }
  }
  var login_username;
  $("#email, #mail_repeat").on("cut copy paste", function(e) {
    e.preventDefault();
    return false;
  });

  // static/js/tabs.ts
  $(function() {
    function switchToTab(tabName) {
      var _a, _b, _c, _d, _e;
      const tab = $('*[data-tab="' + tabName + '"]');
      const allTabs = tab.siblings("*[data-tab]");
      const target = $('*[data-tabtarget="' + tabName + '"]');
      const allTargets = target.siblings("*[data-tabtarget]");
      allTabs.removeClass("tab-selected");
      tab.addClass("tab-selected");
      allTargets.addClass("hidden");
      target.removeClass("hidden");
      const adventures = {};
      window.State.adventures.map(function(adventure) {
        adventures[adventure.short_name] = adventure;
      });
      if (tabName === "end") {
        $("#level-header input").hide();
        $("#editor-area").hide();
        return;
      }
      $("#level-header input").show();
      $("#editor-area").show();
      if (window.State.loaded_program && (window.State.adventure_name_onload || "level") === tabName) {
        $("#program_name").val(window.State.loaded_program.name);
        (_a = window.editor) == null ? void 0 : _a.setValue(window.State.loaded_program.code);
      } else if (adventures[tabName] && adventures[tabName].loaded_program) {
        $("#program_name").val(adventures[tabName].loaded_program.name);
        (_b = window.editor) == null ? void 0 : _b.setValue(adventures[tabName].loaded_program.code);
      } else if (tabName === "level") {
        $("#program_name").val(window.State.default_program_name);
        (_c = window.editor) == null ? void 0 : _c.setValue(window.State.default_program);
      } else {
        $("#program_name").val(adventures[tabName].default_save_name + " - " + window.State.level_title + " " + window.State.level);
        (_d = window.editor) == null ? void 0 : _d.setValue(adventures[tabName].start_code);
      }
      window.State.adventure_name = tabName === "level" ? void 0 : tabName;
      (_e = window.editor) == null ? void 0 : _e.clearSelection();
      window.State.unsaved_changes = false;
    }
    $("*[data-tab]").click(function(e) {
      const tab = $(e.target);
      const tabName = tab.data("tab");
      e.preventDefault();
      if (window.State.unsaved_changes)
        window.modal.confirm(window.auth.texts.unsaved_changes, () => switchToTab(tabName));
      else
        switchToTab(tabName);
      const hashFragment = tabName !== "level" ? tabName : "";
      if (window.history) {
        window.history.replaceState(null, "", "#" + hashFragment);
      }
    });
    if (window.State && window.State.adventure_name) {
      switchToTab(window.State.adventure_name);
    } else if (window.location.hash) {
      const hashFragment = window.location.hash.replace(/^#/, "");
      if (hashFragment) {
        switchToTab(hashFragment);
      }
    }
  });
  window.load_quiz = function(level) {
    $('*[data-tabtarget="end"]').html('<iframe id="quiz-iframe" class="w-full" title="Quiz" src="/quiz/start/' + level + '"></iframe>');
  };

  // static/js/translating.ts
  $(function() {
    function estimateLineCount(s) {
      var ESTIMATED_LINE_LENGTH = 80;
      var lines = s.split("\n");
      var wrappedLines = lines.map((x) => Math.floor(x.length / ESTIMATED_LINE_LENGTH));
      return sum(wrappedLines) + lines.length;
    }
    function sum(xs) {
      let ret = 0;
      for (const x of xs) {
        ret += x;
      }
      return ret;
    }
    function resizeArea(el) {
      var lines = Math.max(1, estimateLineCount($(el).val()));
      var targetHeight = lines * 25 + 4;
      if ($(el).height() < targetHeight) {
        $(el).css({ height: `${targetHeight}px` });
      }
    }
    $("textarea").each((i, el) => resizeArea(el)).on("input", (e) => {
      const target = $(e.target);
      if (!target.hasClass("touched")) {
        target.addClass("touched");
        target.attr("name", target.data("name"));
        recordChangeToForm(target.closest("form"));
      }
      resizeArea(target);
    });
    var FORM_MAP = new Map();
    function recordChangeToForm(form) {
      var fileName = form.data("file");
      var formData = FORM_MAP.get(fileName);
      if (!formData) {
        var button = $('button[data-file="' + fileName + '"]');
        formData = {
          button,
          changes: 0
        };
        FORM_MAP.set(fileName, formData);
      }
      formData.changes += 1;
      formData.button.text(`${fileName} (${formData.changes})`);
    }
    $("button[data-file]").click((e) => {
      var fileName = $(e.target).data("file");
      var form = $('form[data-file="' + fileName + '"]');
      form.submit();
    });
  });
  return js_exports;
})();
//# sourceMappingURL=appbundle.js.map
