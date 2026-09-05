import { multiLevelTester } from "../tools/lezer/lezer_tester";

describe('Tests level 10', () => {
    describe('Test and clause', () => {
        let code = `
        if c is red and name is pepa
            print 'Woooow'
        elif c is blue and name is Ana
            print 'blue'
        else
            print 'other color'
        `        
        const expectedTree =
            `Program(
                Command(
                    If(
                        if,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        ),
                        and,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        )
                    )
                ),
                Command(Print(print,String)),
                Command(
                    Elif(
                        elif,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        ),
                        and,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        )
                    )
                ),
                Command(Print(print,String)),
                Command(Else(else)),
                Command(Print(print,String))
            )`

        multiLevelTester('Test and clause', code, expectedTree, 10, 12);
    })
    
    describe('Test or clause', () => {
        let code = `
        if c is red or name is pepa
            print 'Woooow'
        elif c is blue or name is Ana
            print 'blue'
        else
            print 'other color'
        `
        const expectedTree =
            `Program(
                Command(
                    If(
                        if,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        ),
                        or,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        )
                    )
                ),
                Command(Print(print,String)),
                Command(
                    Elif(
                        elif,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        ),
                        or,
                        Condition(
                            EqualityCheck(Expression(Text),is,Expression(Text))
                        )
                    )
                ),
                Command(Print(print,String)),
                Command(Else(else)),
                Command(Print(print,String))
            )`

        multiLevelTester('Test or clause', code, expectedTree, 10, 12);
    })    
})  