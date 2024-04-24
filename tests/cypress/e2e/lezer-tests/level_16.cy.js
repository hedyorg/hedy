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
        }),
        describe('AssignList tests', () => {
            describe('Assign empty list', () => {
                const code = 'empty = []'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Op)))'

                multiLevelTester('Assign empty list', code, expectedTree, 16, 18)
            });

            describe('Assign list with number', () => {
                const code = 'number = [1]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Number,Op)))'

                multiLevelTester('Assign list with number', code, expectedTree, 16, 18)
            });

            describe('Assign list with float', () => {
                const code = 'number = [42.1]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Number,Op)))'

                multiLevelTester('Assign list with float', code, expectedTree, 16, 18)
            });

            describe('Assign list with string', () => {
                const code = 'string = ["cat"]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,String,Op)))'

                multiLevelTester('Assign list with string', code, expectedTree, 16, 18)
            });

            describe('Assign list with var', () => {
                const code = 'incorrect = [variable]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Text,Op)))'

                multiLevelTester('Assign list with var', code, expectedTree, 16, 18)
            });

            describe('Assign list with multiple items', () => {
                const code = 'list = [1, 0.1, "cat", variable]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Number,Comma,Number,Comma,String,Comma,Text,Op)))'

                multiLevelTester('Assign list with multiple items', code, expectedTree, 16, 18)
            });
        })
    });
})
