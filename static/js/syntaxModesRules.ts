

// A bunch of code expects a global "State" object. Set it here if not
// set yet.
if (!window.State) {
  window.State = {};
}


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
    newReg = newReg.replace("(__" + key + "__)", value); 
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

// import regexs
import REGEX_IMPORT from '../../highlighting/highlighting.json'; 
let REGEX = convert(REGEX_IMPORT) as Map<string,Map<string,Map<string,Map<string,string>>>>;






REGEX.forEach((levelValue,levelKey) => {
  levelKey = levelKey;

  levelValue.forEach((stateValue,stateKey) => {
    stateKey = stateKey;

    stateValue.forEach((ruleValue,ruleKey) => {
      ruleKey = ruleKey;

      //console.log(ruleValue.get('regex'));
      var oldReg = ruleValue.get('regex') as string;
      ruleValue.set('regex', convertReg(oldReg,TRADUCTION));
      //console.log(ruleValue.get('regex'));
      //console.log();
    });
  });
});






// Only do this work if the 'define' function is actually available at runtime.
// If not, this script got included on a page that didn't include the Ace
// editor. No point in continuing if that is the case.
if ((window as any).define) {

  // Define the modes based on the level definitions above
  REGEX.forEach((levelRule,levelName) => {
    // This is a local definition of the file 'ace/mode/level1.js', etc.
    define('ace/mode/' + levelName, [], function(require, exports, _module) {
      var oop = require('ace/lib/oop');
      var TextMode = require('ace/mode/text').Mode;
      var TextHighlightRules = require('ace/mode/text_highlight_rules').TextHighlightRules;

      function ThisLevelHighlightRules(this: any) {
        this.$rules = levelRule;
        this.normalizeRules();
      };
      oop.inherits(ThisLevelHighlightRules, TextHighlightRules);

      function Mode(this: any) {
        this.HighlightRules = ThisLevelHighlightRules;
      };
      oop.inherits(Mode, TextMode);

      exports.Mode = Mode;
    });
  });
}
