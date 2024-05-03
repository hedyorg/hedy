import {
    print as print1, echo as echo1, play as play1, ask as ask1, color as color1,
    forward as forward1, turn as turn1
} from "./level1-parser.terms";

import {
    print as print2, ask as ask2, play as play2, color as color2,
    forward as forward2, turn as turn2, sleep as sleep2, is as is2
} from "./level2-parser.terms";

import {
    print as print3, ask as ask3, play as play3, color as color3,
    forward as forward3, turn as turn3, sleep as sleep3, is as is3,
    add as add3, remove as remove3, from as from3, toList as toList3,
    at as at3, random as random3
} from "./level3-parser.terms"

import {
    print as print4, ask as ask4, play as play4, color as color4,
    forward as forward4, turn as turn4, sleep as sleep4, is as is4,
    add as add4, remove as remove4, from as from4, toList as toList4,
    at as at4, random as random4, clear as clear4
} from "./level4-parser.terms"

import {
    print as print5, ask as ask5, play as play5, color as color5,
    forward as forward5, turn as turn5, sleep as sleep5, is as is5,
    add as add5, remove as remove5, from as from5, toList as toList5,
    at as at5, random as random5, clear as clear5, ifs as if5,
    elses as else5, ins as in5, pressed as pressed5, not_in as not_in5
} from "./level5-parser.terms"

import {
    print as print6, ask as ask6, play as play6, color as color6,
    forward as forward6, turn as turn6, sleep as sleep6, is as is6,
    add as add6, remove as remove6, from as from6, toList as toList6,
    at as at6, random as random6, clear as clear6, ifs as if6,
    elses as else6, ins as in6, pressed as pressed6, not_in as not_in6
} from "./level6-parser.terms"

import {
    print as print7, ask as ask7, play as play7, color as color7,
    forward as forward7, turn as turn7, sleep as sleep7, is as is7,
    add as add7, remove as remove7, from as from7, toList as toList7,
    at as at7, random as random7, clear as clear7, ifs as if7,
    elses as else7, ins as in7, pressed as pressed7, not_in as not_in7,
    repeat as repeat7, times as times7, 
} from "./level7-parser.terms"

import {
    print as print8, ask as ask8, play as play8, color as color8,
    forward as forward8, turn as turn8, sleep as sleep8, is as is8,
    add as add8, remove as remove8, from as from8, toList as toList8,
    at as at8, random as random8, clear as clear8, ifs as if8,
    elses as else8, ins as in8, pressed as pressed8, not_in as not_in8,
    repeat as repeat8, times as times8, 
} from "./level8-parser.terms"

import {
    print as print10, ask as ask10, play as play10, color as color10,
    forward as forward10, turn as turn10, sleep as sleep10, is as is10,
    add as add10, remove as remove10, from as from10, toList as toList10,
    at as at10, random as random10, clear as clear10, ifs as if10,
    elses as else10, ins as in10, pressed as pressed10, not_in as not_in10,
    repeat as repeat10, times as times10, fors as for10
} from "./level10-parser.terms"

import {
    print as print11, ask as ask11, play as play11, color as color11,
    forward as forward11, turn as turn11, sleep as sleep11, is as is11,
    add as add11, remove as remove11, from as from11, toList as toList11,
    at as at11, random as random11, clear as clear11, ifs as if11,
    elses as else11, ins as in11, pressed as pressed11, not_in as not_in11,
    repeat as repeat11, times as times11, fors as for11, to as to11, range as range11
} from "./level11-parser.terms"

import {
    print as print12, ask as ask12, play as play12, color as color12,
    forward as forward12, turn as turn12, sleep as sleep12, is as is12,
    add as add12, remove as remove12, from as from12, toList as toList12,
    at as at12, random as random12, clear as clear12, ifs as if12,
    elses as else12, ins as in12, pressed as pressed12, not_in as not_in12,
    repeat as repeat12, times as times12, fors as for12, to as to12, range as range12,
    define as define12, returns as returns12, _with as with12, call as call12
} from "./level12-parser.terms"

import {
    print as print13, ask as ask13, play as play13, color as color13,
    forward as forward13, turn as turn13, sleep as sleep13, is as is13,
    add as add13, remove as remove13, from as from13, toList as toList13,
    at as at13, random as random13, clear as clear13, ifs as if13,
    elses as else13, ins as in13, pressed as pressed13, not_in as not_in13,
    repeat as repeat13, times as times13, fors as for13, to as to13, range as range13,
    define as define13, returns as returns13, _with as with13, call as call13,
    and as and13, or as or13
} from "./level13-parser.terms"

import {
    print as print14, ask as ask14, play as play14, color as color14,
    forward as forward14, turn as turn14, sleep as sleep14, is as is14,
    add as add14, remove as remove14, from as from14, toList as toList14,
    at as at14, random as random14, clear as clear14, ifs as if14,
    elses as else14, ins as in14, pressed as pressed14, not_in as not_in14,
    repeat as repeat14, times as times14, fors as for14, to as to14, range as range14,
    define as define14, returns as returns14, _with as with14, call as call14,
    and as and14, or as or14
} from "./level14-parser.terms"

import {
    print as print15, ask as ask15, play as play15, color as color15,
    forward as forward15, turn as turn15, sleep as sleep15, is as is15,
    add as add15, remove as remove15, from as from15, toList as toList15,
    at as at15, random as random15, clear as clear15, ifs as if15,
    elses as else15, ins as in15, pressed as pressed15, not_in as not_in15,
    repeat as repeat15, times as times15, fors as for15, to as to15, range as range15,
    define as define15, returns as returns15, _with as with15, call as call15,
    and as and15, or as or15, _while as while15
} from "./level15-parser.terms"

import {
    print as print16, ask as ask16, play as play16, color as color16,
    forward as forward16, turn as turn16, sleep as sleep16, is as is16,
    add as add16, remove as remove16, from as from16, toList as toList16,
    random as random16, clear as clear16, ifs as if16,
    elses as else16, ins as in16, pressed as pressed16, not_in as not_in16,
    repeat as repeat16, times as times16, fors as for16, to as to16, range as range16,
    define as define16, returns as returns16, _with as with16, call as call16,
    and as and16, or as or16, _while as while16
} from "./level16-parser.terms"

import {
    print as print17, ask as ask17, play as play17, color as color17,
    forward as forward17, turn as turn17, sleep as sleep17, is as is17,
    add as add17, remove as remove17, from as from17, toList as toList17,
    random as random17, clear as clear17, ifs as if17,
    elses as else17, ins as in17, pressed as pressed17, not_in as not_in17,
    repeat as repeat17, times as times17, fors as for17, to as to17, range as range17,
    define as define17, returns as returns17, _with as with17, call as call17,
    and as and17, or as or17, _while as while17, elif as elif17
} from "./level17-parser.terms"

import {
    print as print18, is as is18, input as input18, sleep as sleep18, random as random18, 
    forward as forward18, turn as turn18, play as play18, color as color18, add as add18,
    remove as remove18, from as from18, clear as clear18, ifs as ifs18,
    elses as elses18, and as and18, or as or18, pressed as pressed18, notIn as notIn18, ins as ins18,
    repeat as repeat18, times as times18, range as range18, whiles as whiles18,
    def as def18, returns as returns18, fors as fors18, toList as toList18, elif as elif18
}  from "./level18-parser.terms";

import TRADUCTION_IMPORT from '../../../highlighting/highlighting-trad.json';
import { Stack } from "@lezer/lr";
import { convert } from "../utils";
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
            "play": play1,
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
            "play": play2,
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
            "play": play3,
            "sleep": sleep3,
            "is": is3,
            "add": add3,
            "remove": remove3,
            "from": from3,
            "to_list": toList3,
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
            "play": play4,
            "sleep": sleep4,
            "is": is4,
            "add": add4,
            "remove": remove4,
            "from": from4,
            "to_list": toList4,
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
            "play": play5,
            "sleep": sleep5,
            "is": is5,
            "add": add5,
            "remove": remove5,
            "from": from5,
            "to_list": toList5,
            "clear": clear5,
            "not_in": not_in5,
            "in": in5
        },
        specialize: {
            "if": if5,
            "pressed": pressed5,
            "ask": ask5,
            "at": at5,
            "random": random5,
            "else": else5
        },        
    },
    6: {
        extend: {
            "print": print6,
            "forward": forward6,
            "turn": turn6,
            "color": color6,
            "play": play6,
            "sleep": sleep6,
            "is": is6,
            "add": add6,
            "remove": remove6,
            "from": from6,
            "to_list": toList6,
            "clear": clear6,
            "not_in": not_in6,
            "in": in6
        },
        specialize: {
            "if": if6,
            "pressed": pressed6,
            "ask": ask6,
            "at": at6,
            "random": random6,
            "else": else6
        },        
    },
    7: {
        extend: {
            "print": print7,
            "forward": forward7,
            "turn": turn7,
            "color": color7,
            "play": play7,
            "sleep": sleep7,
            "is": is7,
            "add": add7,
            "remove": remove7,
            "from": from7,
            "to_list": toList7,
            "clear": clear7,
            "not_in": not_in7,
            "in": in7,
            "repeat": repeat7,
            "times": times7
        },
        specialize: {
            "if": if7,
            "pressed": pressed7,
            "ask": ask7,
            "at": at7,
            "random": random7,
            "else": else7
        },        
    },
    8: {
        extend: {
            "print": print8,
            "forward": forward8,
            "turn": turn8,
            "color": color8,
            "play": play8,
            "sleep": sleep8,
            "is": is8,
            "add": add8,
            "remove": remove8,
            "from": from8,
            "to_list": toList8,
            "clear": clear8,
            "not_in": not_in8,
            "in": in8,
            "repeat": repeat8,
            "times": times8
        },
        specialize: {
            "if": if8,
            "pressed": pressed8,
            "ask": ask8,
            "at": at8,
            "random": random8,
            "else": else8
        },
    },
    // same as level 8
    9: {
        extend: {
            "print": print8,
            "forward": forward8,
            "turn": turn8,
            "color": color8,
            "play": play8,
            "sleep": sleep8,
            "is": is8,
            "add": add8,
            "remove": remove8,
            "from": from8,
            "to_list": toList8,
            "clear": clear8,
            "not_in": not_in8,
            "in": in8,
            "repeat": repeat8,
            "times": times8
        },
        specialize: {
            "if": if8,
            "pressed": pressed8,
            "ask": ask8,
            "at": at8,
            "random": random8,
            "else": else8
        },
    },
    10: {
        extend: {
            "print": print10,
            "forward": forward10,
            "turn": turn10,
            "color": color10,
            "play": play10,
            "sleep": sleep10,
            "is": is10,
            "add": add10,
            "remove": remove10,
            "from": from10,
            "to_list": toList10,
            "clear": clear10,
            "not_in": not_in10,
            "in": in10,
            "repeat": repeat10,
            "times": times10,
            "for": for10
        },
        specialize: {
            "if": if10,
            "pressed": pressed10,
            "ask": ask10,
            "at": at10,
            "random": random10,
            "else": else10
        },
    },
    11: {
        extend: {
            "print": print11,
            "forward": forward11,
            "turn": turn11,
            "color": color11,
            "play": play11,
            "sleep": sleep11,
            "is": is11,
            "add": add11,
            "remove": remove11,
            "from": from11,
            "to_list": toList11,
            "clear": clear11,
            "not_in": not_in11,
            "in": in11,
            "repeat": repeat11,
            "times": times11,
            "for": for11,
            "to": to11,
            "range": range11
        },
        specialize: {
            "if": if11,
            "pressed": pressed11,
            "ask": ask11,
            "at": at11,
            "random": random11,
            "else": else11
        },
    },
    12: {
        extend: {
            "print": print12,
            "forward": forward12,
            "turn": turn12,
            "color": color12,
            "play": play12,
            "sleep": sleep12,
            "is": is12,
            "add": add12,
            "remove": remove12,
            "from": from12,
            "to_list": toList12,
            "clear": clear12,
            "not_in": not_in12,
            "in": in12,
            "repeat": repeat12,
            "times": times12,
            "for": for12,
            "to": to12,
            "range": range12,
            "return": returns12,
            "define": define12,
        },
        specialize: {
            "if": if12,
            "pressed": pressed12,
            "ask": ask12,
            "at": at12,
            "random": random12,
            "else": else12,
            "call": call12,
            "with": with12
        },
    },
    13: {
        extend: {
            "print": print13,
            "forward": forward13,
            "turn": turn13,
            "color": color13,
            "play": play13,
            "sleep": sleep13,
            "is": is13,
            "add": add13,
            "remove": remove13,
            "from": from13,
            "to_list": toList13,
            "clear": clear13,
            "not_in": not_in13,
            "in": in13,
            "repeat": repeat13,
            "times": times13,
            "for": for13,
            "to": to13,
            "range": range13,
            "return": returns13,
            "define": define13
        },
        specialize: {
            "if": if13,
            "pressed": pressed13,
            "ask": ask13,
            "at": at13,
            "random": random13,
            "else": else13,
            "and": and13,
            "or": or13,
            "call": call13,
            "with": with13
        },
    },
    14: {
        extend: {
            "print": print14,
            "forward": forward14,
            "turn": turn14,
            "color": color14,
            "play": play14,
            "sleep": sleep14,
            "add": add14,
            "remove": remove14,
            "from": from14,
            "to_list": toList14,
            "clear": clear14,
            "not_in": not_in14,
            "repeat": repeat14,
            "times": times14,
            "for": for14,
            "to": to14,
            "range": range14,
            "return": returns14,
            "define": define14,            
        },
        specialize: {
            "if": if14,
            "pressed": pressed14,
            "ask": ask14,
            "at": at14,
            "random": random14,
            "else": else14,
            "and": and14,
            "or": or14,
            "in": in14,
            "is": is14,
            "call": call14,
            "with": with14
        },
    },
    15: {
        extend: {
            "print": print15,
            "forward": forward15,
            "turn": turn15,
            "color": color15,
            "play": play15,
            "sleep": sleep15,
            "is": is15,
            "add": add15,
            "remove": remove15,
            "from": from15,
            "to_list": toList15,
            "clear": clear15,
            "not_in": not_in15,
            "repeat": repeat15,
            "times": times15,
            "for": for15,
            "to": to15,
            "range": range15,
            "return": returns15,
            "define": define15            
        },
        specialize: {
            "if": if15,
            "pressed": pressed15,
            "ask": ask15,
            "at": at15,
            "random": random15,
            "else": else15,
            "and": and15,
            "or": or15,
            "in": in15,
            "is": is15,
            "while": while15,
            "call": call15,
            "with": with15
        },
    },
    16: {
        extend: {
            "print": print16,
            "forward": forward16,
            "turn": turn16,
            "color": color16,
            "play": play16,
            "sleep": sleep16,
            "is": is16,
            "add": add16,
            "remove": remove16,
            "from": from16,
            "to_list": toList16,
            "clear": clear16,
            "not_in": not_in16,
            "repeat": repeat16,
            "times": times16,
            "for": for16,
            "to": to16,
            "range": range16,
            "return": returns16,
            "define": define16            
        },
        specialize: {
            "if": if16,
            "pressed": pressed16,
            "ask": ask16,
            "random": random16,
            "else": else16,
            "and": and16,
            "or": or16,
            "in": in16,
            "is": is16,
            "while": while16,
            "call": call16,
            "with": with16
        },
    },
    17: {
        extend: {
            "print": print17,
            "forward": forward17,
            "turn": turn17,
            "color": color17,
            "play": play17,
            "sleep": sleep17,
            "is": is17,
            "add": add17,
            "remove": remove17,
            "from": from17,
            "to_list": toList17,
            "clear": clear17,
            "not_in": not_in17,
            "repeat": repeat17,
            "times": times17,
            "for": for17,
            "to": to17,
            "range": range17,
            "return": returns17,
            "define": define17
        },
        specialize: {
            "if": if17,
            "pressed": pressed17,
            "ask": ask17,
            "random": random17,
            "else": else17,
            "and": and17,
            "or": or17,
            "in": in17,
            "is": is17,
            "while": while17,
            "elif": elif17,
            "call": call17,
            "with": with17
        },
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
            "play": play18,
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
            "return": returns18,
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

export function specializeKeyword(name: string, stack: Stack) {
    for (const [key, value] of specializeTranslations) {
        const regexString =  value.replace(/ /g, '|');
        if (new RegExp(`^(${regexString})$`, 'gu').test(name)) {
            if (stack.canShift(keywordToToken[level].specialize[key])) {
                return keywordToToken[level].specialize[key];
            }
        }
    }
    return -1;
}

export function extendKeyword(name: string, stack: Stack) {
    for (const [key, value] of extendTranslations) {
        const regexString =  value.replace(/ /g, '|');
        if (new RegExp(`^(${regexString})$`, 'gu').test(name)) {
            if (stack.canShift(keywordToToken[level].extend[key])) {
                return keywordToToken[level].extend[key];
            }            
        }
    }
    return -1;
}
