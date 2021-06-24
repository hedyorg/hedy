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

//  MODE LEVEL 5 SETUP
define('ace/mode/level5', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level5_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 5
define('ace/mode/level5_highlight_rules', [], function(require, exports, module) {
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
      },{
        token: "keyword",
        regex: "^if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: " else ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^repeat "
      }],

      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "repeat "
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
        regex: "'$|' ",
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


//  MODE LEVEL 6 SETUP
define('ace/mode/level6', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level6_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 6
define('ace/mode/level6_highlight_rules', [], function(require, exports, module) {
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
      },{
        token: "keyword",
        regex: "^if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: " else ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^repeat "
      },{
        token: "keyword",
        regex: " \\* "
      },{
        token: "keyword",
        regex: " \\+ "
      },{
        token: "keyword",
        regex: " \\- "
      }],

      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "repeat "
      },{
        token: "keyword",
        regex: "is "
      },{
        token: "keyword",
        regex: " \\* "
      }
      ,{
        token: "keyword",
        regex: " \\+ "
      }
      ,{
        token: "keyword",
        regex: " \\- "
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

//  MODE LEVEL 7 SETUP
define('ace/mode/level7', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level7_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 7
define('ace/mode/level7_highlight_rules', [], function(require, exports, module) {
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
      },{
        token: "keyword",
        regex: "^if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^else$",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^repeat "
      },{
        token: "keyword",
        regex: " \\* "
      },{
        token: "keyword",
        regex: " \\+ "
      },{
        token: "keyword",
        regex: " \\- "
      }],

      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "repeat "
      },{
        token: "keyword",
        regex: "is "
      },{
        token: "keyword",
        regex: " \\* "
      }
      ,{
        token: "keyword",
        regex: " \\+ "
      }
      ,{
        token: "keyword",
        regex: " \\- "
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

//  MODE LEVEL 8 and 9 SETUP
define('ace/mode/level8and9', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level8and9_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 8 and 9
define('ace/mode/level8and9_highlight_rules', [], function(require, exports, module) {
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
      },{
        token: "keyword",
        regex: "^if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^else$",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: " \\* "
      },{
        token: "keyword",
        regex: " \\+ "
      },{
        token: "keyword",
        regex: " \\- "
      },{
        token: "keyword",
        regex: "^for ",
        next: "forloop1"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range ",
        next: "forloop2"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: " to ",
        next: "forloop3"
      },{
        defaultToken : "text"
      }],

      "forloop3": [{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "is "
      },{
        token: "keyword",
        regex: " \\* "
      }
      ,{
        token: "keyword",
        regex: " \\+ "
      }
      ,{
        token: "keyword",
        regex: " \\- "
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
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

//  MODE LEVEL 10 SETUP
define('ace/mode/level10', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level10_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 10
define('ace/mode/level10_highlight_rules', [], function(require, exports, module) {
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
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^else$",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: " \\* "
      },{
        token: "keyword",
        regex: " \\+ "
      },{
        token: "keyword",
        regex: " \\- "
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range ",
        next: "forloop2"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: " to ",
        next: "forloop3"
      },{
        defaultToken : "text"
      }],

      "forloop3": [{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "is "
      },{
        token: "keyword",
        regex: " \\* "
      }
      ,{
        token: "keyword",
        regex: " \\+ "
      }
      ,{
        token: "keyword",
        regex: " \\- "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 11 SETUP
define('ace/mode/level11', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level11_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 11
define('ace/mode/level11_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " is input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " is ",
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^else$",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: " \\* "
      },{
        token: "keyword",
        regex: " \\+ "
      },{
        token: "keyword",
        regex: " \\- "
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "is "
      },{
        token: "keyword",
        regex: " \\* "
      }
      ,{
        token: "keyword",
        regex: " \\+ "
      }
      ,{
        token: "keyword",
        regex: " \\- "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 12 SETUP
define('ace/mode/level12', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level12_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 12
define('ace/mode/level12_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " is input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^else$",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "is "
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 13 SETUP
define('ace/mode/level13', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level13_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 13
define('ace/mode/level13_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " is input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^else| else",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "support.function",
        regex: "True|False",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 14 SETUP
define('ace/mode/level14', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level14_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 14
define('ace/mode/level14_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " is input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^else| else",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "support.function",
        regex: "True|False"
      },{
        token: "keyword",
        regex: " is "
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },
      {
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 15 SETUP
define('ace/mode/level15', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level15_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 15
define('ace/mode/level15_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "comment",
        regex: "#.*$"
      },{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " is input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^else| else",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "support.function",
        regex: "True|False"
      },{
        token: "keyword",
        regex: " is "
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "print ",
        next: "print option"
      },{
        token: "keyword",
        regex: "is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },
      {
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 16 SETUP
define('ace/mode/level16', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level16_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 16
define('ace/mode/level16_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "comment",
        regex: "#.*$"
      },{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " is input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^elif|^else| else| elif",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "support.function",
        regex: "True|False"
      },{
        token: "keyword",
        regex: " is "
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: "is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "<"
      },{
        token: "keyword",
        regex: ">"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 17 & 18 SETUP
define('ace/mode/level17and18', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level17and18_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 17 & 18
define('ace/mode/level17and18_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "comment",
        regex: "#.*$"
      },{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " is input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^elif|^else| else| elif",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      },{
        token: "keyword",
        regex: "^while | while ",
        next: "ifElseSpace"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "support.function",
        regex: "True|False"
      },{
        token: "keyword",
        regex: " is "
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: "is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "<"
      },{
        token: "keyword",
        regex: ">"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        defaultToken : "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 19 SETUP
define('ace/mode/level19', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level19_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 19
define('ace/mode/level19_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "comment",
        regex: "#.*$"
      },{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " is input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^elif|^else| else| elif",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      },{
        token: "keyword",
        regex: "^while | while ",
        next: "ifElseSpace"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "support.function",
        regex: "True|False"
      },{
        token: "keyword",
        regex: " is "
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "length[(]",
        next: "length is"
      },{
        defaultToken : "text"
      }],

      "length is": [{
        token: "keyword",
        regex: "[)]",
        next: "LijstOfGeenLijst"
      },{
        defaultToken: "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "length[(]",
        next: "length forloop"
      },{
        defaultToken : "text"
      }],

      "length forloop": [{
        token: "keyword",
        regex: "[)]",
        next: "forloop2"
      },{
        defaultToken: "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: "is ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "<"
      },{
        token: "keyword",
        regex: ">"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: " length[(]",
        next: "length rest"
      },{
        defaultToken : "text"
      }],

      "length rest": [{
        token: "keyword",
        regex: "[)]",
        next: "print option"
      },{
        defaultToken: "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 20 SETUP
define('ace/mode/level20', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level20_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 20
define('ace/mode/level20_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "comment",
        regex: "#.*$"
      },{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " = input[(]|= input[(]| =input[(]|=input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " = | =|=|= ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^elif|^else| else| elif",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      },{
        token: "keyword",
        regex: "^while | while ",
        next: "ifElseSpace"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "support.function",
        regex: "True|False"
      },{
        token: "keyword",
        regex: " = | =|=|= "
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "length[(]",
        next: "length is"
      },{
        defaultToken : "text"
      }],

      "length is": [{
        token: "keyword",
        regex: "[)]",
        next: "LijstOfGeenLijst"
      },{
        defaultToken: "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "length[(]",
        next: "length forloop"
      },{
        defaultToken : "text"
      }],

      "length forloop": [{
        token: "keyword",
        regex: "[)]",
        next: "forloop2"
      },{
        defaultToken: "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " = | =|=|= ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "<"
      },{
        token: "keyword",
        regex: ">"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: " length[(]",
        next: "length rest"
      },{
        defaultToken : "text"
      }],

      "length rest": [{
        token: "keyword",
        regex: "[)]",
        next: "print option"
      },{
        defaultToken: "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 21 SETUP
define('ace/mode/level21', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level21_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 21
define('ace/mode/level21_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "comment",
        regex: "#.*$"
      },{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " = input[(]|= input[(]| =input[(]|=input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " = | =|=|= ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^elif|^else| else| elif",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      },{
        token: "keyword",
        regex: "^while | while ",
        next: "ifElseSpace"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "support.function",
        regex: "True|False"
      },{
        token: "keyword",
        regex: " = | =|=|= "
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "length[(]",
        next: "length is"
      },{
        defaultToken : "text"
      }],

      "length is": [{
        token: "keyword",
        regex: "[)]",
        next: "LijstOfGeenLijst"
      },{
        defaultToken: "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "length[(]",
        next: "length forloop"
      },{
        defaultToken : "text"
      }],

      "length forloop": [{
        token: "keyword",
        regex: "[)]",
        next: "forloop2"
      },{
        defaultToken: "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " != |!= |!=| !=| = | =|=|= ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "<"
      },{
        token: "keyword",
        regex: ">"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: " length[(]",
        next: "length rest"
      },{
        defaultToken : "text"
      }],

      "length rest": [{
        token: "keyword",
        regex: "[)]",
        next: "print option"
      },{
        defaultToken: "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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

//  MODE LEVEL 21 and 22 SETUP
define('ace/mode/level21and22', [], function(require, exports, module) {

  var oop = require("ace/lib/oop");
  var TextMode = require("ace/mode/text").Mode;
  var Tokenizer = require("ace/tokenizer").Tokenizer;
  var ExampleHighlightRules = require("ace/mode/level21and22_highlight_rules").ExampleHighlightRules;

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


 //  Syntax rules level 22
define('ace/mode/level21and22_highlight_rules', [], function(require, exports, module) {
  var oop = require("ace/lib/oop");
  var TextHighlightRules = require("ace/mode/text_highlight_rules").TextHighlightRules;

  var ExampleHighlightRules = function() {

    this.$rules = {

      "start": [{
        token: "comment",
        regex: "#.*$"
      },{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " = input[(]|= input[(]| =input[(]|=input[(]",
        next: "input"
      },{
        token: "keyword",
        regex: " = | =|=|= ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "^if |    if ",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "^elif|^else| else| elif",
        next: "ifElseSpace"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "^for | for ",
        next: "forloop1"
      },{
        token: "keyword",
        regex: "^while | while ",
        next: "ifElseSpace"
      }],

      "LijstOfGeenLijst": [{
        token: "text",
        regex: "\\[",
        next: "lijst"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "support.function",
        regex: "True|False"
      },{
        token: "keyword",
        regex: " = | =|=|= "
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "length[(]",
        next: "length is"
      },{
        defaultToken : "text"
      }],

      "length is": [{
        token: "keyword",
        regex: "[)]",
        next: "LijstOfGeenLijst"
      },{
        defaultToken: "text"
      }],

      "lijst": [{
        token: "constant.character",
        regex: "'",
        next: "singleQuote"
      },{
        token: "text",
        regex: "\\]",
        next: "start"
      }],

      "singleQuote": [{
        token: "constant.character",
        regex: "'",
        next: "lijst"
      },{
        token: "constant.character",
        regex: "'\\]",
        next: "start"
      },{
        defaultToken: "constant.character"
      }],

      "input": [{
        token: "constant.character",
        regex: "'",
        next: "input rest"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "input rest": [{
        token: "constant.character",
        regex: "'",
        next: "input eind"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "constant.character"
      }],

      "input eind": [{
        token: "keyword",
        regex: "[)]$",
        next: "start"
      },
      {
        token: "text",
        regex: "$",
        next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop1": [{
        token: "keyword",
        regex: " in range[(]",
        next: "forloop2"
      },{
      token: "text",
      regex: "$",
      next: "start"
      },{
        defaultToken : "text"
      }],

      "forloop2": [{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "length[(]",
        next: "length forloop"
      },{
        defaultToken : "text"
      }],

      "length forloop": [{
        token: "keyword",
        regex: "[)]",
        next: "forloop2"
      },{
        defaultToken: "text"
      }],


      "ifElseSpace": [{
        token: "keyword",
        regex: "^print[(]| print[(]",
        next: "print option"
      },{
        token: "keyword",
        regex: " != |!= |!=| !=| = | =|=|= ",
        next: "LijstOfGeenLijst"
      },{
        token: "keyword",
        regex: "\\*"
      }
      ,{
        token: "keyword",
        regex: "\\+"
      }
      ,{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: "<"
      },{
        token: "keyword",
        regex: ">"
      },{
        token: "keyword",
        regex: " and "
      },{
        token: "keyword",
        regex: " or "
      },{
        token: "text",
        regex: "$",
        next: "start"
      }],


      "print option": [{
        token: "constant.character",
        regex: "'",
        next: "print rest"
      },{
        token: "text",
        regex: "$",
        next: "start"
      },{
        token: "keyword",
        regex: "[)]",
        next: "start"
      },{
        token: "keyword",
        regex: "\\*"
      },{
        token: "keyword",
        regex: "\\+"
      },{
        token: "keyword",
        regex: "\\-"
      },{
        token: "keyword",
        regex: " length[(]",
        next: "length rest"
      },{
        defaultToken : "text"
      }],

      "length rest": [{
        token: "keyword",
        regex: "[)]",
        next: "print option"
      },{
        defaultToken: "text"
      }],

      "print rest": [{
        token: "keyword",
        regex: " at random | at random$",
      },{
        token: "constant.character", // constant.character
        regex: "'$",
        next: "start"
      },{
        token: "constant.character",
        regex: "'",
        next: "print option"
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