import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tests for level 16', () => {
    describe('Successful tests', () => {
        describe('Play tests', () => {
            describe('Play list access random', () => {
                const code = 'play list[random]'
                const expectedTree = 'Program(Command(Play(play,Expression(ListAccess(Text,Op,random,Op)))))'

                multiLevelTester('Play note', code, expectedTree, 16, 18)
            });

            describe('Play list access index', () => {
                const code = 'play list[1]'
                const expectedTree = 'Program(Command(Play(play,Expression(ListAccess(Text,Op,Number,Op)))))'

                multiLevelTester('Play note', code, expectedTree, 16, 18)
            });
        })
    });
})
