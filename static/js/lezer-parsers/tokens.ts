import {
  print as print18, is as is18, input as input18, sleep as sleep18, random as random18, 
  forward as forward18, turn as turn18, color as color18, add as add18,
  remove as remove18, from as from18, clear as clear18, ifs as ifs18,
  elses as elses18, and as and18, or as or18, pressed as pressed18, notIn as notIn18, ins as ins18,
  repeat as repeat18, times as times18, range as range18, whiles as whiles18,
  def as def18, returns as returns18, fors as fors18, toList as toList18, elif as elif18}
from "./level18-parser.terms";

import {
    print as print1, echo as echo1, ask as ask1, color as color1,
    forward as forward1, turn as turn1
} from "./level1-parser.terms";

import {
    print as print2, ask as ask2, color as color2,
    forward as forward2, turn as turn2, sleep as sleep2, is as is2
} from "./level2-parser.terms";

import {
    print as print3, ask as ask3, color as color3,
    forward as forward3, turn as turn3, sleep as sleep3, is as is3,
    add as add3, remove as remove3, from as from3, to_list as to_list3,
    at as at3, random as random3
} from "./level3-parser.terms"

import {
    print as print4, ask as ask4, color as color4,
    forward as forward4, turn as turn4, sleep as sleep4, is as is4,
    add as add4, remove as remove4, from as from4, to_list as to_list4,
    at as at4, random as random4, clear as clear4
} from "./level4-parser.terms"

import {
    print as print5, ask as ask5, color as color5,
    forward as forward5, turn as turn5, sleep as sleep5, is as is5,
    add as add5, remove as remove5, from as from5, to_list as to_list5,
    at as at5, random as random5, clear as clear5, ifs as if5,
    elses as else5, ins as in5, pressed as pressed5, not_in as not_in5
} from "./level5-parser.terms"

import TRADUCTION_IMPORT from '../../../highlighting/highlighting-trad.json';
export interface InitializeCodeMirrorSyntaxHighlighterOptions {
    readonly keywordLanguage: string;
    readonly level: number;
}

let TRADUCTION: Map<string,string>;
let level: number;
interface tokenSpecilizer {
    extend: Record<string, number>,
    specialize: Record<string, number>,
}
const keywordToToken: Record<number, tokenSpecilizer> = {
    1: {
        extend: {
            "ask": ask1,
            "print": print1,
            "echo": echo1,
            "forward": forward1,
            "turn": turn1,
            "color": color1
        },
        specialize: {}
    },
    2: {
        extend: {
            "print": print2,
            "forward": forward2,
            "turn": turn2,
            "color": color2,
            "sleep": sleep2,
            "is": is2
        },
        specialize: {
            "ask": ask2,
        }
    },
    3: {
        extend: {
            "print": print3,
            "forward": forward3,
            "turn": turn3,
            "color": color3,
            "sleep": sleep3,
            "is": is3,
            "add": add3,
            "remove": remove3,
            "from": from3,
            "to_list": to_list3,
        },
        specialize: {
            "ask": ask3,
            "at": at3,
            "random": random3
        }
    },
    4: {
        extend: {
            "print": print4,
            "forward": forward4,
            "turn": turn4,
            "color": color4,
            "sleep": sleep4,
            "is": is4,
            "add": add4,
            "remove": remove4,
            "from": from4,
            "to_list": to_list4,
            "clear": clear4
        },
        specialize: {
            "ask": ask4,
            "at": at4,
            "random": random4
        }
    },
    5: {
        extend: {
            "print": print5,
            "forward": forward5,
            "turn": turn5,
            "color": color5,
            "sleep": sleep5,
            "is": is5,
            "add": add5,
            "remove": remove5,
            "from": from5,
            "to_list": to_list5,
            "clear": clear5,
            "pressed": pressed5,
            "not_in": not_in5,
            "in": in5
        },
        specialize: {
            "if": if5,
            "ask": ask5,
            "at": at5,
            "random": random5,
            "else": else5
        }
    },
    18 : {
        specialize: {
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
        },
        extend: {}
    }
}

let specializeTranslations: Map<string, string>;
let extendTranslations: Map<string, string>;

export function initializeTranslation(options: InitializeCodeMirrorSyntaxHighlighterOptions) {
    const TRADUCTIONS = convert(TRADUCTION_IMPORT) as Map<string, Map<string,string>>;
    level = options.level;
    let lang = options.keywordLanguage;
    if (!TRADUCTIONS.has(lang)) { lang = 'en'; }
    // get the traduction    
    TRADUCTION = TRADUCTIONS.get(lang) as Map<string,string>;
    specializeTranslations = new Map();
    extendTranslations = new Map();
    
    for (const [key, value] of TRADUCTION) {
        if (key in keywordToToken[level].specialize) {
            specializeTranslations.set(key, value);
        } else if (key in keywordToToken[level].extend) {
            extendTranslations.set(key, value);
        }
    }
}

export function specializeKeyword(name: string) {
    for (const [key, value] of specializeTranslations) {
        const regexString =  value.replace(' ', '|');
        if (new RegExp(`^(${regexString})$`, 'gu').test(name)) {
          return keywordToToken[level].specialize[key];
        }
    }
    return -1;
}

export function extendKeyword(name: string) {
    for (const [key, value] of extendTranslations) {
        const regexString =  value.replace(' ', '|');
        if (new RegExp(`^(${regexString})$`, 'gu').test(name)) {
          return keywordToToken[level].extend[key];
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