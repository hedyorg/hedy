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
                    `Program(
                        Command(
                            If(if,
                                Condition(EqualityCheck(Text,is,Text)),
                                IfLessCommand(Print(print,String))
                            )
                        )
                    )
                    `
                
                multiLevelTester('Test simple if clause', code, expectedTree, 6, 7);
            });

            describe('Test if clause with else same line', () => {
                const code = "if name is Hedy print 'cute name' else print 'Hedy is better'"
                const expectedTree = 
                    `Program(
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Text)),
                                IfLessCommand(Print(print,String)),
                                else,
                                IfLessCommand(Print(print,String))
                            )
                        )
                    )`
                
                    multiLevelTester('Test if clause with else same line', code, expectedTree, 6, 7);
            });

            describe('Test if clause with else and if different line', () => {
                const code = `if name is Hedy print 'cute name'\nelse print 'Hedy is better'`
                const expectedTree = 
                    `Program(
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Text)),
                                IfLessCommand(Print(print,String)),
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
                                Condition(EqualityCheck(Text,is,Text)),
                                IfLessCommand(Print(print,String)),
                                else,
                                IfLessCommand(Print(print,String))
                            )
                        )
                    )`
                
                multiLevelTester('Test if clause with every command different line', code, expectedTree, 6, 7);            
            });        
        });
    })
});