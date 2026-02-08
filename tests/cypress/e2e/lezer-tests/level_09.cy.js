import { multiLevelTester } from "../tools/lezer/lezer_tester";
import { codeMirrorContent } from '../tools/programs/program';

describe('Tests level 9', () => {    

    describe('Test elif clause', () => {
        const code = `if color is red\nprint 'red'\nelif color is blue\nprint 'blue'\nelse\nprint 'other color'`
        const expectedTree =
            `Program(
                Command(
                    If(if,Condition(EqualityCheck(Expression(Text),is,Expression(Text))))
                ),
                Command(Print(print,String)),
                Command(
                    Elif(
                        elif,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        )
                    )
                ),
                Command(Print(print,String)),
                Command(Else(else)),
                Command(Print(print,String))
            )`

        multiLevelTester('Test elif clause', code, expectedTree, 9, 12);
    }) 

    describe('Test if clause with print same line', () => {
        const code = "if name is Hedy\nprint 'hello Hedy'";
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
                        )
                    )
                ),
                Command(Print(print,String))
            )`

        multiLevelTester('Test simple if clause', code, expectedTree, 9, 12);
    });
    
    describe('Test if clause with every command different line', () => {
        const code = `if name is Hedy\nprint 'cute name'\nelse\nprint 'Hedy is better'`
        const expectedTree =
            `Program(
                Command(If(if,Condition(EqualityCheck(Expression(Text),is,Expression(Text))))),
                Command(Print(print,String)),
                Command(Else(else)),
                Command(Print(print,String))
            )`

        multiLevelTester('Test if clause with every command different line', code, expectedTree, 9, 12);
    });
    
    describe('Test if text in list print', () => {
        const code = `
                    if text in list
                      print 'in'`
        const expectedTree =
            `Program(
                        Command(If(if,Condition(InListCheck(Expression(Text),in,Text)))),
                        Command(Print(print,String)))`

        multiLevelTester('Test if text in list print', code, expectedTree, 9, 11);
    })
    
    
    describe('Test if number in list print', () => {
        const code =
            `if 5 in list
                        print 'in'`
        const expectedTree =
            `Program(
                        Command(If(if,Condition(InListCheck(Expression(Number),in,Text)))),
                        Command(Print(print,String))
                    )`

        multiLevelTester('Test if number in list print', code, expectedTree, 9, 11);
    })
        
    
    describe('Test if text not in list print', () => {
        const code = `
                    if text not in list
                      print 'in'`
        const expectedTree =
            `Program(
                Command(If(if,Condition(NotInListCheck(Expression(Text),not_in,not_in,Text)))),
                Command(Print(print,String))
            )`

        multiLevelTester('Test if text not in list print', code, expectedTree, 9, 11);
    })
        
    
    describe('Test if number not in list print', () => {
        const code =
            `if 5 not in list
                        print 'in'`
        const expectedTree =
            `Program(
                Command(If(if,Condition(NotInListCheck(Expression(Number),not_in,not_in,Text)))),
                Command(Print(print,String))
            )`

        multiLevelTester('Test if number not in list print', code, expectedTree, 9, 11);
    })
  
    describe('Test equality check equal sign', () => {
        const code =
            `if order = burger
                price is 5`
        const expectedTree =
            `Program(
                Command(If(if,Condition(EqualityCheck(Expression(Text),Op,Expression(Text))))),
                Command(Assign(Text,is,Expression(Number)))
            )`

        multiLevelTester('Test equality check equal sign', code, expectedTree, 9, 11);
    })

    describe('Max amount of lines for level 9', () => {
        it('Typing more than 200 lines should not be posible', () => {
            cy.focused().type('a line!\n'.repeat(201));
            codeMirrorContent().should('have.text', 'a line!\n'.repeat(200)); // First 200 lines should be in editor

            cy.get('#warningbox').should('be.visible');
            cy.get('#warningbox p.details').should('contain.text', 'Your program may not be longer than 200 lines!');
        });
    });
})  