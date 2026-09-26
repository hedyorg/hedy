import { testTree } from "@lezer/generator/dist/test"
import { PARSER_FACTORIES } from '../../../../../static/js/lezer-parsers/language-packages';

export function multiLevelTester(testName: string, code: string, expectedTree: string, from: number, to: number, language = 'en') {

    for (let i = from; i <= to; i++) {
        it(`${testName} for level ${i}`, () => {
            const parser = PARSER_FACTORIES[i](language);
            testTree(parser.parse(code), expectedTree);
        })
    }
}

export function singleLevelTester(testName: string, code: string, expectedTree: string, level: number, language = 'en') {
    it(testName, () => {
        const parser = PARSER_FACTORIES[level](language);
        testTree(parser.parse(code), expectedTree);
    })
}
