import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tets for level 7', () => {
    describe('Successful tests', () => {
        
        describe('Test assign with keyword inside', () => {
            const code = 
                `command is print hello world
                `
            const expectedTree = 
                `Program(
                    Command(
                        Assign(Text,is,Expression(Text),Expression(Text),Expression(Text))
                    )
                )
                `
            
            multiLevelTester('Test assign with keyword inside', code, expectedTree, 7, 11);
        });

        describe('Test sleep with number', () => {
            const code = `sleep 5`
            const expectedTree = `
                Program(
                    Command(
                        Sleep(sleep,Expression(Number))
                    )
                )`;

            multiLevelTester('Test sleep with number', code, expectedTree, 7, 12);
        });

        describe('If Tests', () => {
            describe('Test if clause with print same line', () => {
                const code = "if name is Hedy\nprint 'hello Hedy'";
                const expectedTree = 
                    `Program(Command(
                        If(
                            if,
                            Condition(EqualityCheck(Expression(Text),is,Expression(Text))),
                            IfLessCommand(Print(print,String))
                        )
                    ))
                    `
                
                multiLevelTester('Test simple if clause', code, expectedTree, 7, 8);
            });
            
            describe('Test if clause with every command different line', () => {
                const code = `if name is Hedy\nprint 'cute name'\nelse\nprint 'Hedy is better'`
                const expectedTree = 
                    `Program(
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Expression(Text),is,Expression(Text))),
                                IfLessCommand(Print(print,String))
                            )
                        ),
                        Command(
                            Else(
                                else,
                                IfLessCommand(Print(print,String))
                            )
                        )
                    )`
                
                multiLevelTester('Test if clause with every command different line', code, expectedTree, 7, 8);
            });
        });        

        describe('Test expressions', () => {
            let code = `print '5 plus 5 is ' 5 + 5
            print '5 minus 5 is ' 5 - 5
            print '5 times 5 is ' 5 * 5
            print '5 devided by 5 is ' 5 / 5`

            code = code.split('\n').map(line => line.trim()).join('\n')

            const expectedTree = `
            Program(
                Command(Print(print,String,Expression(Expression(Number),Op,Expression(Number)))),
                Command(Print(print,String,Expression(Expression(Number),Op,Expression(Number)))),
                Command(Print(print,String,Expression(Expression(Number),Op,Expression(Number)))),
                Command(Print(print,String,Expression(Expression(Number),Op,Expression(Number)))))
            `

            multiLevelTester('Test expressions', code, expectedTree, 7, 11);
        })

        describe('Test assignment with expression', () => {
            const code = 'respuesta = 20 + 4'
            const expectedTree = `
            Program(
                Command(
                    Assign(
                        Text,
                        Op,
                        Expression(
                            Expression(Number),
                            Op,
                            Expression(Number)
                        )
                    )
                )
            )`

            multiLevelTester('Test assignment with expression', code, expectedTree, 7, 11);
        })

        describe('Test if number in list print', () => {
            const code = `if 5 in list print 'in'`
            const expectedTree =
            `Program(
                Command(
                    If(
                        if,
                        Condition(InListCheck(Expression(Number),in,Text)),
                        IfLessCommand(Print(print,String))
                    )
                )
            )`

            singleLevelTester('Test if number in list print', code, expectedTree, 7);
        })

        describe('Test if number not in list print', () => {
            const code = `if 5 not in list print 'in'`
            const expectedTree =
            `Program(
                Command(
                    If(
                        if,
                        Condition(NotInListCheck(Expression(Number),not_in,not_in,Text)),
                        IfLessCommand(Print(print,String))
                    )
                )
            )`

            singleLevelTester('Test if number not in list print', code, expectedTree, 7);
        })
        describe('Test elif clause', () => {
            const code = `if color is red\nprint 'red'\nelif color is blue\nprint 'blue'\nelse\nprint 'other color'`
            const expectedTree =
                `Program(
                    Command(
                        If(
                            if,
                            Condition(
                                EqualityCheck(
                                    Expression(Text),
                                    is,
                                    Expression(Text)
                                )
                            ),
                            IfLessCommand(
                                Print(print, String)
                            )
                        )
                    ),
                    Command(
                        Elif(
                            elif,
                            Condition(
                                EqualityCheck(
                                    Expression(Text),
                                    is,
                                    Expression(Text)
                                )
                            ),
                            IfLessCommand(
                                Print(print, String)
                            )
                        )
                    ),
                    Command(
                        Else(
                            else,
                            IfLessCommand(
                                Print(print, String)
                            )
                        )
                    )
                )`

            multiLevelTester('Test elif clause', code, expectedTree, 7, 8);
        })
 
        describe('Play tests', () => {
            describe('Play note', () => {
                const code = 'play G4'
                const expectedTree = 'Program(Command(Play(play,Expression(Text))))'

                multiLevelTester('Play note', code, expectedTree, 7, 16)
            });

            describe('Play int', () => {
                const code = 'play 34'
                const expectedTree = 'Program(Command(Play(play,Expression(Number))))'

                multiLevelTester('Play note', code, expectedTree, 7, 16)
            });

            describe('Play list access index', () => {
                const code = 'play list at 1'
                const expectedTree = 'Program(Command(Play(play,ListAccess(Text,at,Number))))'

                multiLevelTester('Play note', code, expectedTree, 7, 12)
            })
        })
    })
})