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
                        Assign(Text,is,Text,Text,Text)
                    )
                )
                `
            singleLevelTester('Test assign with keyword inside', code, expectedTree, 6);
        });

        describe('Test sleep with number', () => {
            const code = `sleep 5`
            const expectedTree = `
                Program(
                    Command(
                        Sleep(sleep,Text)
                    )
                )`;

            singleLevelTester('Test sleep with number', code, expectedTree, 6);
        });

        describe('If Tests', () => {
            describe('Test if clause with print same line', () => {
                const code = "if name is Hedy print 'hello Hedy'";
                const expectedTree = `
                    Program(
                            Command(
                                If(
                                    if,
                                    Condition(
                                        EqualityCheck(
                                            Text,
                                            is,
                                            Text
                                        )
                                    ),
                                    IfLessCommand(
                                        Print(
                                            print,
                                            String
                                        )
                                    )
                                )
                            )
                        )`
                singleLevelTester('Test simple if clause', code, expectedTree, 6);
            });            

            describe('Test if clause with else and if different line', () => {
                const code = `if name is Hedy print 'cute name'\nelse print 'Hedy is better'`
                const expectedTree = 
                    `Program(
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Text)),
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
                
                singleLevelTester('Test if clause with else and if different line', code, expectedTree, 6); 
            });
            
            describe('Test if clause with every command different line', () => {
                const code = `if name is Hedy\nprint 'cute name'\nelse\nprint 'Hedy is better'`
                const expectedTree = 
                    `Program(
                        Command(
                            If(
                                if,
                                Condition(
                                    EqualityCheck(
                                        Text,
                                        is,
                                        Text
                                    )
                                ),
                                IfLessCommand(
                                    Print(
                                        print,
                                        String
                                    )
                                )
                            )
                        ),
                        Command(
                            Else(
                                else,
                                IfLessCommand(
                                    Print(
                                        print,
                                        String
                                    )
                                )
                            )
                        )
                    )`
            
                singleLevelTester('Test if clause with every command different line', code, expectedTree, 6);
            });
        });
        
        describe('Test introduction adventure', () => {
            let code = `
                food_price is 0
                drink_price is 0
                total_price is 0
                print 'Welcome to McHedy'
                order is ask 'What would you like to eat?'
                if order is hamburger
                food_price is 5
                if order is fries
                food_price is 2
                drink is ask 'What would you like to drink?'
                if drink is water
                drink_price is 0
                else
                drink_price is 3
                total_price is food_price + drink_price
                print 'That will be ' total_price ' dollars, please'`

            code = code.split('\n').map(line => line.trim()).join('\n')

            const expectedTree = `
            Program(
                Command(Assign(Text, is, Text)),
                Command(Assign(Text, is, Text)),
                Command(Assign(Text, is, Text)),
                Command(Print(print, String)),
                Command(Ask(Text, is, ask, String)),
                Command(If(
                    if,
                    Condition(EqualityCheck(Text, is, Text)),
                    IfLessCommand(Assign(Text, is, Text))
                )),
                Command(If(
                    if,
                    Condition(EqualityCheck(Text, is, Text)),
                    IfLessCommand(Assign(Text, is, Text))
                )),
                Command(Ask(Text, is, ask, String)),
                Command(If(
                    if,
                    Condition(EqualityCheck(Text, is, Text)),
                    IfLessCommand(Assign(Text, is, Text))
                )),
                Command(Else(
                    else,
                    IfLessCommand(Assign(Text, is, Text))
                )),
                Command(Assign(Text, is, Text, Text, Text)),
                Command(Print(print, String, Text, String))
            )
            `

            singleLevelTester('Test introduction adventure', code, expectedTree, 6);
        })
        
        
        describe('Test elif clause', () => {
            const code = `if color is red print 'red'\nelif color is blue print 'blue'\nelse print 'other color'`
            const expectedTree =
                `Program(
                    Command(If(
                        if,
                        Condition(EqualityCheck(Text, is, Text)),
                        IfLessCommand(Print(print, String))
                    )),
                    Command(Elif(
                        elif,
                        Condition(EqualityCheck(Text, is, Text)),
                        IfLessCommand(Print(print, String))
                    )),
                    Command(Else(
                        else,
                        IfLessCommand(Print(print, String))
                    ))
                )`

            singleLevelTester('Test elif clause', code, expectedTree, 6);
        })
        
        

        describe('Test equality check equal sign', () => {
            const code = 'if order = burger price is 5'
            const expectedTree =
                `Program(
                    Command(If(
                        if,
                        Condition(EqualityCheck(Text, Op, Text)),
                        IfLessCommand(Assign(Text, is, Text))
                    ))
                )`

            singleLevelTester('Test equality check equal sign', code, expectedTree, 6);
        })   
    });             
});
