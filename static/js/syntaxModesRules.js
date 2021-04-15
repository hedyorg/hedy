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
