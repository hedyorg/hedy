import { testTree } from "@lezer/generator/dist/test"
import { PARSER_FACTORIES } from '../../../../../static/js/lezer-parsers/language-packages';

export function multiLevelTester(testName, code, expectedTree, from, to, language = 'en') {

    for (let i = from; i <= to; i++) {
        it(`${testName} for level ${i}`, () => {
            const parser = PARSER_FACTORIES[i](language);
            testTree(parser.parse(code), expectedTree);
        })
    }
}

export function singleLevelTester(testName, code, expectedTree, level, language = 'en') {
    it(testName, () => {
        const parser = PARSER_FACTORIES[level](language);
        testTree(parser.parse(code), expectedTree);
    })
}
