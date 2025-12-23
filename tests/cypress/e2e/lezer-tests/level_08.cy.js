import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tests for level 8', () => {
    describe('Successful tests', () => {
        describe('Test if text in list print', () => {
            const code = `
            if text in list
              print 'in'`
            const expectedTree =
            `Program(
                Command(If(if,Condition(InListCheck(Text,in,Text)))),
                Command(Print(print,String)))`

            multiLevelTester('Test if text in list print', code, expectedTree, 8, 11);
        })

        describe('Test if number in list print', () => {
            const code =
            `if 5 in list
                print 'in'`
            const expectedTree =
            `Program(
                Command(If(if,Condition(InListCheck(Int,in,Text)))),
                Command(Print(print,String))
            )`

            multiLevelTester('Test if number in list print', code, expectedTree, 8, 11);
        })

        describe('Test if text not in list print', () => {
            const code = `
            if text not in list
              print 'in'`
            const expectedTree =
            `Program(
                Command(If(if,Condition(NotInListCheck(Text,not_in,not_in,Text)))),
                Command(Print(print,String)))`

            multiLevelTester('Test if text not in list print', code, expectedTree, 8, 11);
        })

        describe('Test if number not in list print', () => {
            const code =
            `if 5 not in list
                print 'in'`
            const expectedTree =
            `Program(
                Command(If(if,Condition(NotInListCheck(Int,not_in,not_in,Text)))),
                Command(Print(print,String))
            )`

            multiLevelTester('Test if number not in list print', code, expectedTree, 8, 11);
        })

        describe('Test equality check equal sign', () => {
            const code = 
                `if order = burger
                    price is 5`
            const expectedTree = 
                `Program(
                    Command(If(if,Condition(EqualityCheck(Text,Op,Expression(Text))))),
                    Command(Assign(Text,is,Expression(Int)))
                )
                `
            
            multiLevelTester('Test equality check equal sign', code, expectedTree, 8, 11);
        })
    })
})
