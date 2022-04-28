
import * as LEVELS_ar from '../../highlighting/highlightingRules/highlighting-ar.json'; 
import * as LEVELS_bg from '../../highlighting/highlightingRules/highlighting-bg.json'; 
import * as LEVELS_bn from '../../highlighting/highlightingRules/highlighting-bn.json'; 
import * as LEVELS_cs from '../../highlighting/highlightingRules/highlighting-cs.json'; 
import * as LEVELS_de from '../../highlighting/highlightingRules/highlighting-de.json'; 
import * as LEVELS_el from '../../highlighting/highlightingRules/highlighting-el.json'; 
import * as LEVELS_en from '../../highlighting/highlightingRules/highlighting-en.json'; 
import * as LEVELS_es from '../../highlighting/highlightingRules/highlighting-es.json'; 
import * as LEVELS_fa from '../../highlighting/highlightingRules/highlighting-fa.json'; 
import * as LEVELS_fr from '../../highlighting/highlightingRules/highlighting-fr.json'; 
import * as LEVELS_fy from '../../highlighting/highlightingRules/highlighting-fy.json'; 
import * as LEVELS_hi from '../../highlighting/highlightingRules/highlighting-hi.json'; 
import * as LEVELS_hu from '../../highlighting/highlightingRules/highlighting-hu.json'; 
import * as LEVELS_id from '../../highlighting/highlightingRules/highlighting-id.json'; 
import * as LEVELS_it from '../../highlighting/highlightingRules/highlighting-it.json'; 
import * as LEVELS_nb_NO from '../../highlighting/highlightingRules/highlighting-nb_NO.json'; 
import * as LEVELS_nl from '../../highlighting/highlightingRules/highlighting-nl.json'; 
import * as LEVELS_pl from '../../highlighting/highlightingRules/highlighting-pl.json'; 
import * as LEVELS_pt_BR from '../../highlighting/highlightingRules/highlighting-pt_BR.json'; 
import * as LEVELS_pt_PT from '../../highlighting/highlightingRules/highlighting-pt_PT.json'; 
import * as LEVELS_ru from '../../highlighting/highlightingRules/highlighting-ru.json'; 
import * as LEVELS_sw from '../../highlighting/highlightingRules/highlighting-sw.json'; 
import * as LEVELS_tr from '../../highlighting/highlightingRules/highlighting-tr.json'; 
import * as LEVELS_zh_Hans from '../../highlighting/highlightingRules/highlighting-zh_Hans.json'; 




// A bunch of code expects a global "State" object. Set it here if not
// set yet.
if (!window.State) {
window.State = {};
}




var CHOICE;
switch(window.State.keyword_language){
  case 'ar':
    CHOICE = LEVELS_ar;
    break;
  case 'bg':
    CHOICE = LEVELS_bg;
    break;
  case 'bn':
    CHOICE = LEVELS_bn;
    break;
  case 'cs':
    CHOICE = LEVELS_cs;
    break;
  case 'de':
    CHOICE = LEVELS_de;
    break;
  case 'el':
    CHOICE = LEVELS_el;
    break;
  case 'en':
    CHOICE = LEVELS_en;
    break;
  case 'es':
    CHOICE = LEVELS_es;
    break;
  case 'fa':
    CHOICE = LEVELS_fa;
    break;
  case 'fr':
    CHOICE = LEVELS_fr;
    break;
  case 'fy':
    CHOICE = LEVELS_fy;
    break;
  case 'hi':
    CHOICE = LEVELS_hi;
    break;
  case 'hu':
    CHOICE = LEVELS_hu;
    break;
  case 'id':
    CHOICE = LEVELS_id;
    break;
  case 'it':
    CHOICE = LEVELS_it;
    break;
  case 'nb_NO':
    CHOICE = LEVELS_nb_NO;
    break;
  case 'nl':
    CHOICE = LEVELS_nl;
    break;
  case 'pl':
    CHOICE = LEVELS_pl;
    break;
  case 'pt_BR':
    CHOICE = LEVELS_pt_BR;
    break;
  case 'pt_PT':
    CHOICE = LEVELS_pt_PT;
    break;
  case 'ru':
    CHOICE = LEVELS_ru;
    break;
  case 'sw':
    CHOICE = LEVELS_sw;
    break;
  case 'tr':
    CHOICE = LEVELS_tr;
    break;
  case 'zh_Hans':
    CHOICE = LEVELS_zh_Hans;
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
