import * as LEVELS_en from './highlightingRules/highlighting-en.json';
import * as LEVELS_nl from './highlightingRules/highlighting-nl.json';
import * as LEVELS_es from './highlightingRules/highlighting-es.json';
import * as LEVELS_ar from './highlightingRules/highlighting-ar.json';
import * as LEVELS_fr from './highlightingRules/highlighting-fr.json';
import * as LEVELS_hi from './highlightingRules/highlighting-hi.json';
import * as LEVELS_tr from './highlightingRules/highlighting-tr.json';
import * as LEVELS_id from './highlightingRules/highlighting-id.json';
import * as LEVELS_nb_NO from './highlightingRules/highlighting-nb_NO.json';



// A bunch of code expects a global "State" object. Set it here if not
// set yet.
if (!window.State) {
window.State = {};
}


var CHOICE;
switch(window.State.keyword_language){
  case 'nl':
    CHOICE = LEVELS_nl;
    break;
  case 'ar':
    CHOICE = LEVELS_ar;
    break;
  case 'es':
    CHOICE = LEVELS_es;
    break;
  case 'fr':
    CHOICE = LEVELS_fr;
    break;
  case 'tr':
    CHOICE = LEVELS_tr;
    break;
  case 'hi':
    CHOICE = LEVELS_hi;
    break;
  case 'id':
    CHOICE = LEVELS_id;
    break;
  case 'nb_NO':
    CHOICE = LEVELS_nb_NO;
    break;
  default:
    CHOICE = LEVELS_en;
    break;
}



// Convert to the right format
var LEVELS = [];
for (let key in CHOICE) {
  if (key != "default") {
    LEVELS.push(CHOICE[key]);
  }
}


// Only do this work if the 'define' function is actually available at runtime.
// If not, this script got included on a page that didn't include the Ace
// editor. No point in continuing if that is the case.
if ((window as any).define) {

  // Define the modes based on the level definitions above
  for (const level of LEVELS) {
    // This is a local definition of the file 'ace/mode/level1.js', etc.
    define('ace/mode/' + level.name, [], function(require, exports, _module) {
      var oop = require('ace/lib/oop');
      var TextMode = require('ace/mode/text').Mode;
      var TextHighlightRules = require('ace/mode/text_highlight_rules').TextHighlightRules;

      function ThisLevelHighlightRules(this: any) {
        this.$rules = level.rules;
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
