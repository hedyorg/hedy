import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tests for level 13', () => {
    describe('Successful tests', () => {        
        describe('Boolean tests', () => {
            describe('Assign boolean True', () => {
                const code = 't = True'
                const expectedTree = 'Program(Command(Assign(Text,Op,Expression(True))))'

                multiLevelTester('Assign boolean True', code, expectedTree, 13, 16)
            });

            describe('Assign boolean true', () => {
                const code = 't = true'
                const expectedTree = 'Program(Command(Assign(Text,Op,Expression(true))))'

                multiLevelTester('Assign boolean true', code, expectedTree, 13, 16)
            });

            describe('Assign boolean False', () => {
                const code = 't = False'
                const expectedTree = 'Program(Command(Assign(Text,Op,Expression(False))))'

                multiLevelTester('Assign boolean False', code, expectedTree, 13, 16)
            });

            describe('Assign boolean false', () => {
                const code = 't = false'
                const expectedTree = 'Program(Command(Assign(Text,Op,Expression(false))))'

                multiLevelTester('Assign boolean false', code, expectedTree, 13, 16)
            });

            describe('Print boolean literal true', () => {
                const code = 'print true'
                const expectedTree = 'Program(Command(Print(print,PrintArguments(Expression(true)))))'

                multiLevelTester('Print boolean literal true', code, expectedTree, 13, 16)
            });

            describe('Print boolean literal false', () => {
                const code = 'print false'
                const expectedTree = 'Program(Command(Print(print,PrintArguments(Expression(false)))))'

                multiLevelTester('Print boolean literal false', code, expectedTree, 13, 16)
            });

            describe('AssignList boolean values', () => {
                const code = 'options = [False, True]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,False,Op,True,Op)))'

                multiLevelTester('AssignList boolean values', code, expectedTree, 13, 16)
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

                multiLevelTester('AssignList boolean values', code, expectedTree, 13, 16)
            });
        })
        describe('Play tests', () => {
            describe('Play list access random', () => {
                const code = 'play list[random]'
                const expectedTree = 'Program(Command(Play(play,Expression(ListAccess(Text,Op,random,Op)))))'

                multiLevelTester('Play note', code, expectedTree, 13, 16)
            });

            describe('Play list access index', () => {
                const code = 'play list[1]'
                const expectedTree = 'Program(Command(Play(play,Expression(ListAccess(Text,Op,Number,Op)))))'

                multiLevelTester('Play note', code, expectedTree, 13, 16)
            });
        }),
        describe('AssignList tests', () => {
            describe('Assign empty list', () => {
                const code = 'empty = []'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Op)))'

                multiLevelTester('Assign empty list', code, expectedTree, 13, 16)
            });

            describe('Assign list with number', () => {
                const code = 'number = [1]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Number,Op)))'

                multiLevelTester('Assign list with number', code, expectedTree, 13, 16)
            });

            describe('Assign list with float', () => {
                const code = 'number = [42.1]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Number,Op)))'

                multiLevelTester('Assign list with float', code, expectedTree, 13, 16)
            });

            describe('Assign list with string', () => {
                const code = 'string = ["cat"]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,String,Op)))'

                multiLevelTester('Assign list with string', code, expectedTree, 13, 16)
            });

            describe('Assign list with var', () => {
                const code = 'incorrect = [variable]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Text,Op)))'

                multiLevelTester('Assign list with var', code, expectedTree, 13, 16)
            });

            describe('Assign list with multiple items', () => {
                const code = 'list = [1, 0.1, "cat", variable]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,Number,Op,Number,Op,String,Op,Text,Op)))'

                multiLevelTester('Assign list with multiple items', code, expectedTree, 13, 16)
            });

            describe('AssignList boolean values', () => {
                const code = 'options = [True, False]'
                const expectedTree = 'Program(Command(AssignList(Text,Op,Op,True,Op,False,Op)))'

                multiLevelTester('AssignList boolean values', code, expectedTree, 13, 16)
            });

            describe('List with quotes tests', () => {
                const code = "list = ['string 1', 'string 2', 'string 3']"
                const expectedTree =  'Program(Command(AssignList(Text,Op,Op,String,Op,String,Op,String,Op)))'
    
                multiLevelTester('List with quotes tests', code, expectedTree, 13, 16)
            })
        })

        describe('Function call tests', () => {
            describe('Test simple call function level ', () => {
                const code = `
                def test:
                    return 1
                test()
                `
                const expectedTree =
                `Program(
                    Command(Define(def,Text,Op)),
                    Command(Return(return,PrintArguments(Expression(Number)))),
                    Command(Call(Text,Op,Op))
                )`

                multiLevelTester('Test simple call function level ', code, expectedTree, 13, 16);
            })

            describe('Test simple call function with parameters ', () => {
                const code = 
                `def test(a, b):
                    return a + b
                test(1, 2)
                `
                const expectedTree =
                `Program(
                    Command(
                        Define(
                            def,
                            Text,
                            Op,
                            Arguments(Expression(Text),Op,Expression(Text)),
                            Op,
                            Op
                        )
                    ),
                    Command(
                        Return(
                            return,
                            PrintArguments(
                                Expression(Expression(Text),Op,Expression(Text)
                                )
                            )
                        )
                    ),
                    Command(
                        Call(
                            Text,
                            Op,
                            Arguments(Expression(Number),Op,Expression(Number)),
                            Op
                        )
                    )
                )`

                multiLevelTester('Test simple call with parameters', code, expectedTree, 13, 16);
            })
        })
    });
})
