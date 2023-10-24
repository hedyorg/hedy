import {
  print as print18, is as is18, input as input18, sleep as sleep18, random as random18, 
  forward as forward18, turn as turn18, color as color18, add as add18,
  remove as remove18, from as from18, clear as clear18, ifs as ifs18,
  elses as elses18, and as and18, or as or18, pressed as pressed18, notIn as notIn18, ins as ins18,
  repeat as repeat18, times as times18, range as range18, whiles as whiles18,
  def as def18, returns as returns18, fors as fors18, toList as toList18, elif as elif18}
from "./level18-parser.terms";
import TRADUCTION_IMPORT from '../../../highlighting/highlighting-trad.json';

import {
    print as print1, echo as echo1, ask as ask1, color as color1,
    forward as forward1, turn as turn1
} from "./level1-parser.terms";
export interface InitializeCodeMirrorSyntaxHighlighterOptions {
    readonly keywordLanguage: string;
    readonly level: number;
}

let TRADUCTION: Map<string,string>;
let level: number;

const keywordToToken: Record<number, Record<string, number>> = {
    1: {
        "ask": ask1,
        "print": print1,
        "echo": echo1,
        "forward": forward1,
        "turn": turn1,
        "color": color1
    },
    18 : {
        "add": add18,
        "and": and18,    
        "clear": clear18,
        "color": color18,
        "def": def18,
        "print": print18,
        "is": is18,
        "input": input18,
        "sleep": sleep18,
        "random": random18,
        "forward": forward18,
        "turn": turn18,
        "to_list": toList18,
        "remove": remove18,
        "from": from18,
        "if": ifs18,
        "else": elses18,
        "or": or18,
        "pressed": pressed18,
        "not_in": notIn18,
        "in": ins18,
        "repeat": repeat18,
        "times": times18,
        "range": range18,
        "while": whiles18,
        "returns": returns18,
        "for": fors18,
        "elif": elif18
    }
}

export function initializeTranslation(options: InitializeCodeMirrorSyntaxHighlighterOptions) {
    const TRADUCTIONS = convert(TRADUCTION_IMPORT) as Map<string, Map<string,string>>;
    level = options.level;
    let lang = options.keywordLanguage;
    if (!TRADUCTIONS.has(lang)) { lang = 'en'; }
    // get the traduction    
    TRADUCTION = TRADUCTIONS.get(lang) as Map<string,string> ;    
}

export function specializeKeyword(name: string) {
    for (const [key, value] of TRADUCTION) {
        if (name === 'en') {
            console.log(key, value)
        }
        const regexString =  value.replace(' ', '|');
        if (new RegExp(`^(${regexString})$`, 'gu').test(name)) {
          return keywordToToken[level][key];
        }
    }
    return -1;
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