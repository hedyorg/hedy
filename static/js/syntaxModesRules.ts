import * as REGEX from '../../highlighting/highlighting.json'; 

// A bunch of code expects a global "State" object. Set it here if not
// set yet.
if (!window.State) {
  window.State = {};
}

// convert an objet in a map
function convert(o:(object|undefined)) {
  if (typeof o === 'object') {
    let tmp:Map<string, object> = new Map(Object.entries(o));
    
    let ret:Map<string, (undefined|object)> = new Map();

    tmp.forEach((value, key) => {
      ret.set(key, convert(value));
    });

    return ret;
  } else {
    return o;
  }
}

// here we need to transfome (__<KEYWORD>__) in a current kayword with translation
function convertReg(oldReg:string, TRAD:Map<string,string> ) {
  var newReg = oldReg;

  TRAD.forEach((value,key) => {
    key = key;
    var reg = new RegExp('\\(__' + key + '__\\)','g');
    newReg = newReg.replace(reg, value); 
  });

  return newReg;
}



// import traduction
import TRADUCTION_IMPORT from '../../highlighting/highlighting-trad.json'; 
let TRADUCTIONS = convert(TRADUCTION_IMPORT) as Map<string, Map<string,string>>;

var lang = window.State.keyword_language as string;

if (!TRADUCTIONS.has(lang)) { lang = 'en'; }

// get the traduction
var TRADUCTION = TRADUCTIONS.get(lang) as Map<string,string> ;


// translate regex
var data = JSON.stringify(REGEX);
var data_tr = convertReg(data,TRADUCTION);
var REGEX_tr = JSON.parse(data_tr);



// Convert to the right format
var LEVELS = [];
for (let key in REGEX_tr) {
  if (key != "default") {
    LEVELS.push(REGEX_tr[key]);
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
        console.log(level.rules);
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
