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
    add as add3, remove as remove3, from as from3, to_list as to_list3,
    at as at3, random as random3
} from "./level3-parser.terms"

import {
    print as print4, ask as ask4, play as play4, color as color4,
    forward as forward4, turn as turn4, sleep as sleep4, is as is4,
    add as add4, remove as remove4, from as from4, to_list as to_list4,
    at as at4, random as random4, clear as clear4
} from "./level4-parser.terms"

import {
    print as print5, ask as ask5, play as play5, color as color5,
    forward as forward5, turn as turn5, sleep as sleep5, is as is5,
    add as add5, remove as remove5, from as from5, to_list as to_list5,
    at as at5, random as random5, clear as clear5, ifs as if5,
    elses as else5, pressed as pressed5
} from "./level5-parser.terms"

import {
    print as print6, ask as ask6, play as play6, color as color6,
    forward as forward6, turn as turn6, sleep as sleep6, is as is6,
    add as add6, remove as remove6, from as from6, to_list as to_list6,
    at as at6, random as random6, clear as clear6, ifs as if6,
    elses as else6, ins as in6, pressed as pressed6, not_in as not_in6,
    elif as elif6
} from "./level6-parser.terms"

import {
    print as print7, ask as ask7, play as play7, color as color7,
    forward as forward7, turn as turn7, sleep as sleep7, is as is7,
    add as add7, remove as remove7, from as from7, to_list as to_list7,
    at as at7, random as random7, clear as clear7, ifs as if7,
    elses as else7, ins as in7, pressed as pressed7, not_in as not_in7, elif as elif7
} from "./level7-parser.terms"

import {
    print as print8, ask as ask8, play as play8, color as color8,
    forward as forward8, turn as turn8, sleep as sleep8, is as is8,
    add as add8, remove as remove8, from as from8, to_list as to_list8,
    at as at8, random as random8, clear as clear8, ifs as if8,
    elses as else8, ins as in8, pressed as pressed8, not_in as not_in8,
    repeat as repeat8, times as times8,
} from "./level8-parser.terms"

import {
    print as print10, ask as ask10, play as play10, color as color10,
    forward as forward10, turn as turn10, sleep as sleep10, is as is10,
    add as add10, remove as remove10, from as from10, to_list as to_list10,
    at as at10, random as random10, clear as clear10, ifs as if10,
    elses as else10, ins as in10, pressed as pressed10, not_in as not_in10,
    repeat as repeat10, times as times10, and as and10, or as or10,
} from "./level10-parser.terms"

import {
    print as print11, ask as ask11, play as play11, color as color11,
    forward as forward11, turn as turn11, sleep as sleep11, is as is11,
    add as add11, remove as remove11, from as from11, to_list as to_list11,
    at as at11, random as random11, clear as clear11, ifs as if11,
    elses as else11, ins as in11, pressed as pressed11, not_in as not_in11,
    repeat as repeat11, times as times11, fors as for11
} from "./level11-parser.terms"

import {
    print as print12, ask as ask12, play as play12, color as color12,
    forward as forward12, turn as turn12, sleep as sleep12, is as is12,
    add as add12, remove as remove12, from as from12, to_list as to_list12,
    at as at12, random as random12, clear as clear12, ifs as if12,
    elses as else12, ins as in12, pressed as pressed12, not_in as not_in12,
    repeat as repeat12, times as times12, fors as for12, define as define12,
    returns as returns12, _with as with12, call as call12
} from "./level12-parser.terms"

import {
    print as print13, is as is13, input as input13, sleep as sleep13, random as random13,
    forward as forward13, turn as turn13, play as play13, color as color13, add as add13,
    remove as remove13, from as from13, clear as clear13, ifs as ifs13,
    elses as elses13, and as and13, or as or13, pressed as pressed13, notIn as notIn13, ins as ins13,
    repeat as repeat13, times as times13, range as range13, whiles as whiles13,
    def as def13, returns as returns13, fors as fors13, to_list as to_list13, elif as elif13,
    low_true as true13, low_false as false13, cap_true as True13, cap_false as False13
}  from "./level13-parser.terms";

import {
    print as print14, is as is14, input as input14, sleep as sleep14, random as random14,
    forward as forward14, turn as turn14, play as play14, color as color14, add as add14,
    remove as remove14, from as from14, clear as clear14, ifs as ifs14,
    elses as elses14, and as and14, or as or14, pressed as pressed14, notIn as notIn14, ins as ins14,
    repeat as repeat14, times as times14, range as range14, whiles as whiles14,
    def as def14, returns as returns14, fors as fors14, to_list as to_list14, elif as elif14,
    low_true as true14, low_false as false14, cap_true as True14, cap_false as False14
}  from "./level14-parser.terms";

import {
    print as print15, is as is15, input as input15, sleep as sleep15, random as random15,
    forward as forward15, turn as turn15, play as play15, color as color15, add as add15,
    remove as remove15, from as from15, clear as clear15, ifs as ifs15,
    elses as elses15, and as and15, or as or15, pressed as pressed15, notIn as notIn15, ins as ins15,
    repeat as repeat15, times as times15, range as range15, whiles as whiles15,
    def as def15, returns as returns15, fors as fors15, to_list as to_list15, elif as elif15,
    low_true as true15, low_false as false15, cap_true as True15, cap_false as False15
}  from "./level15-parser.terms";

import {
    print as print16, is as is16, input as input16, sleep as sleep16, random as random16,
    forward as forward16, turn as turn16, play as play16, color as color16, add as add16,
    remove as remove16, from as from16, clear as clear16, ifs as ifs16,
    elses as elses16, and as and16, or as or16, pressed as pressed16, notIn as notIn16, ins as ins16,
    repeat as repeat16, times as times16, range as range16, whiles as whiles16,
    def as def16, returns as returns16, fors as fors16, to_list as to_list16, elif as elif16,
    low_true as true16, low_false as false16, cap_true as True16, cap_false as False16
}  from "./level16-parser.terms";


import TRADUCTION_IMPORT from '../../../highlighting/highlighting-trad.json';
import { Stack } from "@lezer/lr";
export interface InitializeCodeMirrorSyntaxHighlighterOptions {
    readonly keywordLanguage: string;
    readonly level: number;
}

/**
 * Whether we are specializing or extending grammar rules
 */
type SpecializeExtend = keyof TokenSpecializer;

interface TokenSpecializer {
    extend: Record<string, number>,
    specialize: Record<string, number>,
}

const keywordToToken: Record<number, TokenSpecializer> = {
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
            "play": play4,
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
            "play": play5,
            "sleep": sleep5,
            "is": is5,
            "add": add5,
            "remove": remove5,
            "from": from5,
            "to_list": to_list5,
            "clear": clear5,
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
            "to_list": to_list6,
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
            "else": else6,
            "elif": elif6
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
            "to_list": to_list7,
            "clear": clear7,
            "not_in": not_in7,
            "in": in7
        },
        specialize: {
            "if": if7,
            "pressed": pressed7,
            "ask": ask7,
            "at": at7,
            "random": random7,
            "else": else7,
            "elif": elif7
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
            "to_list": to_list8,
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
            "to_list": to_list8,
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
            "to_list": to_list10,
            "clear": clear10,
            "not_in": not_in10,
            "in": in10,
            "repeat": repeat10,
            "times": times10,
        },
        specialize: {
            "if": if10,
            "pressed": pressed10,
            "ask": ask10,
            "at": at10,
            "random": random10,
            "else": else10,
            "and": and10,
            "or": or10
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
            "to_list": to_list11,
            "clear": clear11,
            "not_in": not_in11,
            "in": in11,
            "repeat": repeat11,
            "times": times11,
            "for": for11,
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
            "to_list": to_list12,
            "clear": clear12,
            "not_in": not_in12,
            "in": in12,
            "repeat": repeat12,
            "times": times12,
            "for": for12,
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
        specialize: {
            "add": add13,
            "and": and13,
            "clear": clear13,
            "color": color13,
            "def": def13,
            "print": print13,
            "is": is13,
            "input": input13,
            "play": play13,
            "sleep": sleep13,
            "random": random13,
            "forward": forward13,
            "turn": turn13,
            "to_list": to_list13,
            "remove": remove13,
            "from": from13,
            "if": ifs13,
            "else": elses13,
            "or": or13,
            "pressed": pressed13,
            "not_in": notIn13,
            "in": ins13,
            "repeat": repeat13,
            "times": times13,
            "range": range13,
            "while": whiles13,
            "return": returns13,
            "for": fors13,
            "elif": elif13,
            "true": true13,
            "false": false13,
            "True": True13,
            "False": False13,
        },
        extend: {}
    },
    14: {
        specialize: {
            "add": add14,
            "and": and14,
            "clear": clear14,
            "color": color14,
            "def": def14,
            "print": print14,
            "is": is14,
            "input": input14,
            "play": play14,
            "sleep": sleep14,
            "random": random14,
            "forward": forward14,
            "turn": turn14,
            "to_list": to_list14,
            "remove": remove14,
            "from": from14,
            "if": ifs14,
            "else": elses14,
            "or": or14,
            "pressed": pressed14,
            "not_in": notIn14,
            "in": ins14,
            "repeat": repeat14,
            "times": times14,
            "range": range14,
            "while": whiles14,
            "return": returns14,
            "for": fors14,
            "elif": elif14,
            "true": true14,
            "false": false14,
            "True": True14,
            "False": False14,
        },
        extend: {}
    },
    15: {
        specialize: {
            "add": add15,
            "and": and15,
            "clear": clear15,
            "color": color15,
            "def": def15,
            "print": print15,
            "is": is15,
            "input": input15,
            "play": play15,
            "sleep": sleep15,
            "random": random15,
            "forward": forward15,
            "turn": turn15,
            "to_list": to_list15,
            "remove": remove15,
            "from": from15,
            "if": ifs15,
            "else": elses15,
            "or": or15,
            "pressed": pressed15,
            "not_in": notIn15,
            "in": ins15,
            "repeat": repeat15,
            "times": times15,
            "range": range15,
            "while": whiles15,
            "return": returns15,
            "for": fors15,
            "elif": elif15,
            "true": true15,
            "false": false15,
            "True": True15,
            "False": False15,
        },
        extend: {}
    },
    16: {
        specialize: {
            "add": add16,
            "and": and16,
            "clear": clear16,
            "color": color16,
            "def": def16,
            "print": print16,
            "is": is16,
            "input": input16,
            "play": play16,
            "sleep": sleep16,
            "random": random16,
            "forward": forward16,
            "turn": turn16,
            "to_list": to_list16,
            "remove": remove16,
            "from": from16,
            "if": ifs16,
            "else": elses16,
            "or": or16,
            "pressed": pressed16,
            "not_in": notIn16,
            "in": ins16,
            "repeat": repeat16,
            "times": times16,
            "range": range16,
            "while": whiles16,
            "return": returns16,
            "for": fors16,
            "elif": elif16,
            "true": true16,
            "false": false16,
            "True": True16,
            "False": False16,
        },
        extend: {}
    }
}

/**
 * Return the keyword translations (historically called "traductions" because they were created by a French person) for a given language
 *
 * The return value is `{ keyword -> regex }` for keywords, or the special keyword 'DIGIT'.
 */
export function traductionMap(language: string): Map<string, string> {
    // Recast this so TypeScript isn't too picky about indexing this map with a string.
    const keywordMap: Record<string, Record<string, string>> = TRADUCTION_IMPORT;

    if (!keywordMap[language]) {
        language = 'en';
    }

    return new Map(Object.entries(keywordMap[language]));
}


const PARSER_LOOKUP_CACHE = new Map<string, ParserKeyword[]>();

/**
 * For a given combination of level, keywordLang, and specialize/extend flavor, return a list of keyword regexes we could match and their respective token numbers.
 *
 * The regexes come from the "traductions" map, the classification into specialize/extend comes from the 'keywordToToken' map.
 *
 * The output is cached since the output is always the same.
 */
function parserLookups(level: number, keywordLang: string, specext: SpecializeExtend): ParserKeyword[] {
    const cacheKey = `${level}-${keywordLang}-${specext}`;
    if (PARSER_LOOKUP_CACHE.has(cacheKey)) {
        return PARSER_LOOKUP_CACHE.get(cacheKey)!;
    }

    const list = new Array<ParserKeyword>();

    for (const [keyword, restr] of traductionMap(keywordLang)) {
        // Turn spaces into alternatives. Not sure this is still necessary but it was there.
        const replacedStr =  restr.replace(/ /g, '|');
        const regex = new RegExp(`^(${replacedStr})$`, 'u');
        const token = keywordToToken[level]?.[specext]?.[keyword];
        if (token !== undefined) {
            list.push({ regex, token });
        }
    }

    PARSER_LOOKUP_CACHE.set(cacheKey, list);
    return list;
}

/**
 * How to match a keyword in a (level, language) combination against a parser token
 */
interface ParserKeyword {
    regex: RegExp;
    token: number;
}

export function specializeKeywordGen(level: number, keywordLang: string) {
    return (name: string, stack: Stack) => {
        for (const lookup of parserLookups(level, keywordLang, 'specialize')) {
            if (lookup.regex.test(name) && stack.canShift(lookup.token)) {
                return lookup.token;
            }
        }
        return -1;
    };
}

export function extendKeywordGen(level: number, keywordLang: string) {
    return (name: string, stack: Stack) => {
        for (const lookup of parserLookups(level, keywordLang, 'extend')) {
            if (lookup.regex.test(name) && stack.canShift(lookup.token)) {
                return lookup.token;
            }
        }
        return -1;
    };
}
