import { testTree } from "@lezer/generator/dist/test"
import { PARSER_FACTORIES } from '../../../../../static/js/lezer-parsers/language-packages';

const parsers = {
    1: PARSER_FACTORIES[1],
    2: PARSER_FACTORIES[2],
    3: PARSER_FACTORIES[3],
    4: PARSER_FACTORIES[4],
    5: PARSER_FACTORIES[5],
    6: PARSER_FACTORIES[6],
    7: PARSER_FACTORIES[7],
    8: PARSER_FACTORIES[8],
    9: PARSER_FACTORIES[9],
    10: PARSER_FACTORIES[10],
    11: PARSER_FACTORIES[11],
    12: PARSER_FACTORIES[12],
    13: PARSER_FACTORIES[13],
    14: PARSER_FACTORIES[14],
    15: PARSER_FACTORIES[15],
    16: PARSER_FACTORIES[16],
    17: PARSER_FACTORIES[17],
    18: PARSER_FACTORIES[18],
};

export function multiLevelTester(testName, code, expectedTree, from, to, language = 'en') {

    for (let i = from; i <= to; i++) {
        it(`${testName} for level ${i}`, () => {
            const parser = parsers[i](language);
            testTree(parser.parse(code), expectedTree);
        })
    }
}

export function singleLevelTester(testName, code, expectedTree, level, language = 'en') {
    it(testName, () => {
        const parser = parsers[level](language);
        testTree(parser.parse(code), expectedTree);
    })
}
