import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tets for level 6', () => {
    describe('Successfull tests level 6', () => {
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
            
            multiLevelTester('Test assign with keyword inside', code, expectedTree, 6, 11);
        });

        describe('Test sleep with number', () => {
            const code = `sleep 5`
            const expectedTree = `
                Program(
                    Command(
                        Sleep(sleep,Expression(Int))
                    )
                )`;

            multiLevelTester('Test sleep with number', code, expectedTree, 6, 11);
        });
        describe('If Tests', () => {
            describe('Test if clause with print same line', () => {
                const code = "if name is Hedy print 'hello Hedy'";
                const expectedTree = 
                    `Program(Command(
                        If(
                            if,
                            Condition(EqualityCheck(Text,is,Expression(Text))),
                            IfLessCommand(Print(print,String))
                        )
                    ))
                    `
                
                multiLevelTester('Test simple if clause', code, expectedTree, 6, 7);
            });

            describe('Test if clause with else same line', () => {
                const code = "if name is Hedy print 'cute name' else print 'Hedy is better'"
                const expectedTree = 
                    `Program(Command(
                        If(
                            if,
                            Condition(EqualityCheck(Text,is,Expression(Text))),
                            IfLessCommand(Print(print,String)),
                            Else(
                                else,
                                IfLessCommand(Print(print,String))
                            )
                        )
                    ))`

                    multiLevelTester('Test if clause with else same line', code, expectedTree, 6, 7);
            });

            describe('Test if clause with else and if different line', () => {
                const code = `if name is Hedy print 'cute name'\nelse print 'Hedy is better'`
                const expectedTree = 
                    `Program(
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Expression(Text))),
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
                
                multiLevelTester('Test if clause with else and if different line', code, expectedTree, 6, 7); 
            });
            
            describe('Test if clause with every command different line', () => {
                const code = `if name is Hedy\nprint 'cute name'\nelse\nprint 'Hedy is better'`
                const expectedTree = 
                    `Program(
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Expression(Text))),
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
                
                multiLevelTester('Test if clause with every command different line', code, expectedTree, 6, 7);            
            });        
        });

        describe('Test introduction adventure', () => {
            let code = `
            food_price is 0
            drink_price is 0
            total_price is 0
            print 'Welcome to McHedy'
            order is ask 'What would you like to eat?'
            if order is hamburger food_price is 5
            if order is fries food_price is 2
            drink is ask 'What would you like to drink?'
            if drink is water drink_price is 0
            else drink_price is 3
            total_price is food_price + drink_price
            print 'That will be ' total_price ' dollars, please'`

            code = code.split('\n').map(line => line.trim()).join('\n')

            const expectedTree = `
            Program(
                Command(Assign(Text,is,Expression(Int))),
                Command(Assign(Text,is,Expression(Int))),
                Command(Assign(Text,is,Expression(Int))),
                Command(Print(print,String)),
                Command(Ask(Text,is,ask,String)),
                Command(
                    If(
                        if,
                        Condition(EqualityCheck(Text,is,Expression(Text))),
                        IfLessCommand(Assign(Text,is,Expression(Int)))
                    )
                ),
                Command(
                    If(
                        if,
                        Condition(EqualityCheck(Text,is,Expression(Text))),
                        IfLessCommand(Assign(Text,is,Expression(Int)))
                    )
                ),
                Command(Ask(Text,is,ask,String)),
                Command(
                    If(
                        if,
                        Condition(EqualityCheck(Text,is,Expression(Text))),
                        IfLessCommand(Assign(Text,is,Expression(Int)))
                    )
                ),
                Command(
                    Else(
                        else,
                        IfLessCommand(Assign(Text,is,Expression(Int)))
                    )
                ),
                Command(
                    Assign(Text,is,Expression(Expression(Text),Op,Expression(Text)))
                ),
                Command(Print(print,String,Expression(Text),String))
            )
            `

            singleLevelTester('Test introduction adventure', code, expectedTree, 6);
        })

        describe('Test expressions', () => {
            let code = `print '5 plus 5 is ' 5 + 5
            print '5 minus 5 is ' 5 - 5
            print '5 times 5 is ' 5 * 5
            print '5 devided by 5 is ' 5 / 5`

            code = code.split('\n').map(line => line.trim()).join('\n')

            const expectedTree = `
            Program(
                Command(Print(print,String,Expression(Expression(Int),Op,Expression(Int)))),
                Command(Print(print,String,Expression(Expression(Int),Op,Expression(Int)))),
                Command(Print(print,String,Expression(Expression(Int),Op,Expression(Int)))),
                Command(Print(print,String,Expression(Expression(Int),Op,Expression(Int)))))
            `

            multiLevelTester('Test expressions', code, expectedTree, 6, 11);
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
                            Expression(Int),
                            Op,
                            Expression(Int)
                        )
                    )
                )
            )`

            multiLevelTester('Test assignment with expression', code, expectedTree, 6, 11);
        })

        describe('Test if number in list print', () => {
            const code = `if 5 in list print 'in'`
            const expectedTree =
            `Program(
                Command(
                    If(
                        if,
                        Condition(InListCheck(Int,in,Text)),
                        IfLessCommand(Print(print,String))
                    )
                )
            )`

            multiLevelTester('Test if number in list print', code, expectedTree, 6, 7);
        })

        describe('Test if number not in list print', () => {
            const code = `if 5 not in list print 'in'`
            const expectedTree =
            `Program(
                Command(
                    If(
                        if,
                        Condition(NotInListCheck(Int,not_in,not_in,Text)),
                        IfLessCommand(Print(print,String))
                    )
                )
            )`

            multiLevelTester('Test if number not in list print', code, expectedTree, 6, 7);
        })

        describe('Test equality check equal sign', () => {
            const code = 'if order = burger price is 5'
            const expectedTree =
                `Program(
                    Command(
                        If(if,
                           Condition(EqualityCheck(Text,Op,Expression(Text))),
                           IfLessCommand(Assign(Text,is,Expression(Int)))
                        )
                    )
                )`

            multiLevelTester('Test equality check equal sign', code, expectedTree, 6, 7);
        })

        describe('Play tests', () => {
            describe('Play note', () => {
                const code = 'play G4'
                const expectedTree = 'Program(Command(Play(play,Expression(Text))))'

                multiLevelTester('Play note', code, expectedTree, 6, 18)
            });

            describe('Play int', () => {
                const code = 'play 34'
                const expectedTree = 'Program(Command(Play(play,Expression(Int))))'

                multiLevelTester('Play note', code, expectedTree, 6, 11)
            });

            describe('Play list access index', () => {
                const code = 'play list at 1'
                const expectedTree = 'Program(Command(Play(play,ListAccess(Text,at,Int))))'

                multiLevelTester('Play note', code, expectedTree, 6, 11)
            })
        })
    })
});
