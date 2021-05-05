 //  MODE LEVEL 1 SETUP
define('ace/mode/level1', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level1_highlight_rules").ExampleHighlightRules;

  var Mode = function() {
    this.HighlightRules = ExampleHighlightRules;
  };
  oop.inherits(Mode, TextMode);

  (function() {
    this.lineCommentStart = "#";

    this.createWorker = function(session) {
        var worker = new WorkerClient(["ace"], "ace/mode/mynew_worker", "NewWorker");
        worker.attachToDocument(session.getDocument());
        worker.on("errors", function(e) {
            session.setAnnotations(e.data);
        });
        return worker;
    };

  }).call(Mode.prototype);

  exports.Mode = Mode;
});


 //  Syntax rules level 1
define('ace/mode/level1_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "keyword",
        regex: "^print "
      },{
          token: "keyword",
          regex: "^ask "
      },
      {
          token: "keyword",
          regex: "^echo "
      },{
          token: "comment",
          regex: "#"
      }],

    };
    this.normalizeRules();
  };

  oop.inherits(ExampleHighlightRules, TextHighlightRules);

  exports.ExampleHighlightRules = ExampleHighlightRules;

});

 //  MODE LEVEL 2 SETUP
define('ace/mode/level2', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level2_highlight_rules").ExampleHighlightRules;

  var Mode = function() {
    this.HighlightRules = ExampleHighlightRules;
  };
  oop.inherits(Mode, TextMode);

  (function() {
    this.lineCommentStart = "#";

    this.createWorker = function(session) {
        var worker = new WorkerClient(["ace"], "ace/mode/mynew_worker", "NewWorker");
        worker.attachToDocument(session.getDocument());
        worker.on("errors", function(e) {
            session.setAnnotations(e.data);
        });
        return worker;
    };

  }).call(Mode.prototype);

  exports.Mode = Mode;
});


 //  Syntax rules level 2
define('ace/mode/level2_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "keyword",
        regex: "^print ",
        next: "print rest"
      },{
        token: "keyword",
        regex: " is ask ",
        next: "rest"
      },{
        token: "keyword",
        regex: " is ",
        next: "rest"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "rest": [{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }]
    };
    this.normalizeRules();
  };

  oop.inherits(ExampleHighlightRules, TextHighlightRules);

  exports.ExampleHighlightRules = ExampleHighlightRules;

});

//  MODE LEVEL 3 SETUP
define('ace/mode/level3', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level3_highlight_rules").ExampleHighlightRules;

  var Mode = function() {
    this.HighlightRules = ExampleHighlightRules;
  };
  oop.inherits(Mode, TextMode);

  (function() {
    this.lineCommentStart = "#";

    this.createWorker = function(session) {
        var worker = new WorkerClient(["ace"], "ace/mode/mynew_worker", "NewWorker");
        worker.attachToDocument(session.getDocument());
        worker.on("errors", function(e) {
            session.setAnnotations(e.data);
        });
        return worker;
    };

  }).call(Mode.prototype);

  exports.Mode = Mode;
});


 //  Syntax rules level 3
define('ace/mode/level3_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "keyword",
        regex: "^print ",
        next: "print option"
      },{
        token: "keyword",
        regex: " is ask ",
        next: "rest"
      },{
        token: "keyword",
        regex: " is ",
        next: "rest"
      }],

      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'",
        next: "rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "rest": [{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }]
    };
    this.normalizeRules();
  };

  oop.inherits(ExampleHighlightRules, TextHighlightRules);

  exports.ExampleHighlightRules = ExampleHighlightRules;

});

//  MODE LEVEL 4 SETUP
define('ace/mode/level4', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level4_highlight_rules").ExampleHighlightRules;

  var Mode = function() {
    this.HighlightRules = ExampleHighlightRules;
  };
  oop.inherits(Mode, TextMode);

  (function() {
    this.lineCommentStart = "#";

    this.createWorker = function(session) {
        var worker = new WorkerClient(["ace"], "ace/mode/mynew_worker", "NewWorker");
        worker.attachToDocument(session.getDocument());
        worker.on("errors", function(e) {
            session.setAnnotations(e.data);
        });
        return worker;
    };

  }).call(Mode.prototype);

  exports.Mode = Mode;
});


 //  Syntax rules level 4
define('ace/mode/level4_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "keyword",
        regex: "^print | print ",
        next: "print option"
      },{
        token: "keyword",
        regex: " is ask ",
        next: "rest"
      },{
        token: "keyword",
        regex: " is ",
        //next: "rest"
      },{
        token: "keyword",
        regex: "^if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: " else ",
        next: "ifElseSpace"
      }],

      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      }],

      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "rest": [{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }]
    };
    this.normalizeRules();
  };

  oop.inherits(ExampleHighlightRules, TextHighlightRules);

  exports.ExampleHighlightRules = ExampleHighlightRules;

});