import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tests for level 15', () => {
    describe('Successful tests', () => {
        describe('Boolean tests', () => {
            describe('Assign boolean True', () => {
                const code = 't = True'
                const expectedTree = 'Program(Command(Assign(Text,Op,Expression(True))))'

                multiLevelTester('Assign boolean True', code, expectedTree, 15, 18)
            });

            describe('Assign boolean true', () => {
                const code = 't = true'
                const expectedTree = 'Program(Command(Assign(Text,Op,Expression(true))))'

                multiLevelTester('Assign boolean true', code, expectedTree, 15, 18)
            });

            describe('Assign boolean False', () => {
                const code = 't = False'
                const expectedTree = 'Program(Command(Assign(Text,Op,Expression(False))))'

                multiLevelTester('Assign boolean False', code, expectedTree, 15, 18)
            });

            describe('Assign boolean false', () => {
                const code = 't = false'
                const expectedTree = 'Program(Command(Assign(Text,Op,Expression(false))))'

                multiLevelTester('Assign boolean false', code, expectedTree, 15, 18)
            });

            describe('Print boolean literal true', () => {
                const code = 'print true'
                const expectedTree = 'Program(Command(Print(print,Expression(true))))'

                multiLevelTester('Print boolean literal true', code, expectedTree, 15, 17)
            });

            describe('Print boolean literal false', () => {
                const code = 'print false'
                const expectedTree = 'Program(Command(Print(print,Expression(false))))'

                multiLevelTester('Print boolean literal false', code, expectedTree, 15, 17)
            });

            describe('AssignList boolean values', () => {
                const code = 'options = False, True'
                const expectedTree = 'Program(Command(AssignList(Text,Op,False,Comma,True)))'

                singleLevelTester('AssignList boolean values', code, expectedTree, 15)
            });

            describe('While with boolean equality', () => {
                const code = `
                t is True
                while t = false
                    sleep`

                const expectedTree =
                `Program(
                  Command(Assign(Text,is,Expression(True))),
                  Command(While(while,Condition(EqualityCheck(Expression(Text),Op,Expression(false))))),
                    Command(Sleep(sleep)))
                `

                multiLevelTester('AssignList boolean values', code, expectedTree, 15, 18)
            });
        })
    });
})
