import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tests for level 5', () => {
    describe('Successfull tests', () => {
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
                
                singleLevelTester('Test simple if clause', code, expectedTree, 5);
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
                
                singleLevelTester('Test if clause with else', code, expectedTree, 5);
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
                
                singleLevelTester('Test if clause with else and if different line', code, expectedTree, 5); 
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
                
                singleLevelTester('Test if clause with every command different line', code, expectedTree, 5);            
            });
            
            describe('Test if clause in list', () => {
                const code = `if color_favorito in colores_bonitos print '¡bonito!'\nelse print 'meh'`
                const expectedTree =
                `Program(
                    Command(
                        If(
                            if,
                            Condition(InListCheck(Text,in,Text)),
                            IfLessCommand(Print(print,String)),
                            else,
                            IfLessCommand(Print(print,String))
                        )
                    )
                )`

                multiLevelTester('Test if clause in list', code, expectedTree, 5, 7);
            })

            describe('Test if clause with pressit', () => {
                const code = `if g is pressed print 'Vivieron felices para siempre ❤'\nelse print 'El príncipe fue comido por un hipopótamo 😭'`
                const expectedTree = 
                    `Program(
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,pressed)),
                                IfLessCommand(Print(print,String)),
                                else,
                                IfLessCommand(Print(print,String))
                            )
                        )
                    )
                    `
                
                multiLevelTester('Test if clause with pressit', code, expectedTree, 5, 7);
            })
        });

    });
})