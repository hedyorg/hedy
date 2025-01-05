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
import { PARSER_FACTORIES } from '../../../../../static/js/lezer-parsers/language-packages';

const parsers = {
    1: PARSER_FACTORIES[1]('en'),
    2: PARSER_FACTORIES[2]('en'),
    3: PARSER_FACTORIES[3]('en'),
    4: PARSER_FACTORIES[4]('en'),
    5: PARSER_FACTORIES[5]('en'),
    6: PARSER_FACTORIES[6]('en'),
    7: PARSER_FACTORIES[7]('en'),
    8: PARSER_FACTORIES[8]('en'),
    9: PARSER_FACTORIES[9]('en'),
    10: PARSER_FACTORIES[10]('en'),
    11: PARSER_FACTORIES[11]('en'),
    12: PARSER_FACTORIES[12]('en'),
    13: PARSER_FACTORIES[13]('en'),
    14: PARSER_FACTORIES[14]('en'),
    15: PARSER_FACTORIES[15]('en'),
    16: PARSER_FACTORIES[16]('en'),
    17: PARSER_FACTORIES[17]('en'),
    18: PARSER_FACTORIES[18]('en')
};

export function multiLevelTester(testName, code, expectedTree, from, to, language = 'en') {

    for (let i = from; i <= to; i++) {
        it(`${testName} for level ${i}`, () => {
            initializeTranslation({ keywordLanguage: language, level: i });
            testTree(parsers[i].parse(code), expectedTree);
        })
    }
}

export function singleLevelTester(testName, code, expectedTree, level, language = 'en') {
    it(testName, () => {
        initializeTranslation({ keywordLanguage: language, level: level });
        testTree(parsers[level].parse(code), expectedTree);
    })
}
