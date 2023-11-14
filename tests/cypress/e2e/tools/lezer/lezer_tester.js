import { parser as level1Parser } from "../../../../../static/js/lezer-parsers/level1-parser"
import { parser as level2Parser } from "../../../../../static/js/lezer-parsers/level2-parser"
import { parser as level3Parser } from "../../../../../static/js/lezer-parsers/level3-parser"
import { parser as level4Parser } from "../../../../../static/js/lezer-parsers/level4-parser"
import { parser as level5Parser } from "../../../../../static/js/lezer-parsers/level5-parser"
import { parser as level6Parser } from "../../../../../static/js/lezer-parsers/level6-parser"
import { parser as level7Parser } from "../../../../../static/js/lezer-parsers/level7-parser"
import { parser as level8Parser } from "../../../../../static/js/lezer-parsers/level8-parser"
import { parser as level9Parser } from "../../../../../static/js/lezer-parsers/level9-parser"
import { parser as level10Parser } from "../../../../../static/js/lezer-parsers/level10-parser"
import { parser as level11Parser } from "../../../../../static/js/lezer-parsers/level11-parser"
import { parser as level12Parser } from "../../../../../static/js/lezer-parsers/level12-parser"
import { parser as level13Parser } from "../../../../../static/js/lezer-parsers/level13-parser"
import { parser as level14Parser } from "../../../../../static/js/lezer-parsers/level14-parser"
import { parser as level15Parser } from "../../../../../static/js/lezer-parsers/level15-parser"
import { parser as level16Parser } from "../../../../../static/js/lezer-parsers/level16-parser"
import { parser as level17Parser } from "../../../../../static/js/lezer-parsers/level17-parser"
import { parser as level18Parser } from "../../../../../static/js/lezer-parsers/level18-parser"
import { testTree } from "@lezer/generator/dist/test"
import { initializeTranslation } from '../../../../../static/js/lezer-parsers/tokens';

const parsers = {
    1: level1Parser,
    2: level2Parser,
    3: level3Parser,
    4: level4Parser,
    5: level5Parser,
    6: level6Parser,
    7: level7Parser,
    8: level8Parser,
    9: level9Parser,
    10: level10Parser,
    11: level11Parser,
    12: level12Parser,
    13: level13Parser,
    14: level14Parser,
    15: level15Parser,
    16: level16Parser,
    17: level17Parser,
    18: level18Parser        
};

export function multiLevelTester(testName, code, expectedTree, from, to) {

    for (let i = from; i <= to; i++) {
        it(`${testName} for level ${i}`, () => {
            initializeTranslation({ keywordLanguage: 'en', level: i });
            testTree(parsers[i].parse(code), expectedTree);
        })
    }
}

export function singleLevelTester(testName, code, expectedTree, level) {
    it(testName, () => {
        initializeTranslation({ keywordLanguage: 'en', level: level });    
        testTree(parsers[level].parse(code), expectedTree);
    })
}