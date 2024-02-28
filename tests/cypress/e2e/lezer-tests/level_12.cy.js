import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester";

describe('Tests level 12', () => {
    describe('Successful tests', () => {
        describe('Test for Spanish', () => {
            const code =
            `para animal en animales
                imprimir 'Yo amo ' animal
            `

            const expectedTree = `
            Program(
                Command(For(for,Text,in,Text)),
                Command(Print(print,Expression(String),Expression(Text)))
            )`

            multiLevelTester('Test for Spanish', code, expectedTree, 12, 16, 'es');
        })

        describe('Test if text in list print', () => {
            const code = `
            if text in list
              print 'in'`
            const expectedTree =
            `Program(
                Command(If(if,Condition(InListCheck(Text,in,Text)))),
                Command(Print(print,Expression(String)))
            )`

            multiLevelTester('Test if text in list print', code, expectedTree, 12, 13);
        })

        describe('Test if number in list print', () => {
            const code =
            `if 5 in list
                print 'in'`
            const expectedTree =
            `Program(
                Command(If(if,Condition(InListCheck(Number,in,Text)))),
                Command(Print(print,Expression(String)))
            )`

            multiLevelTester('Test if number in list print', code, expectedTree, 12, 13);
        })

        describe('Test if quoted text in list print', () => {
            const code =
            `if 'bird' in list:
                print 'fly'
            `
            const expectedTree =
            `Program(
                Command(If(if,Condition(InListCheck(String,in,Text)))),
                Command(Print(print,Expression(String)))
            )`

            multiLevelTester('Test if quoted text in list print', code, expectedTree, 12, 13);
        })

        describe('Test if text not in list print', () => {
            const code = `
            if text not in list
              print 'in'`
            const expectedTree =
            `Program(
                Command(If(if,Condition(NotInListCheck(Text,not_in,not_in,Text)))),
                Command(Print(print,Expression(String)))
            )`

            multiLevelTester('Test if text not in list print', code, expectedTree, 12, 13);
        })

        describe('Test if number not in list print', () => {
            const code =
            `if 5 not in list
                print 'in'`
            const expectedTree =
            `Program(
                Command(If(if,Condition(NotInListCheck(Number,not_in,not_in,Text)))),
                Command(Print(print,Expression(String)))
            )`

            multiLevelTester('Test if number not in list print', code, expectedTree, 12, 13);
        })

        describe('Test if quoted text not in list print', () => {
            const code =
            `if 'bird' not in list:
                print 'fly'
            `
            const expectedTree =
            `Program(
                Command(If(if,Condition(NotInListCheck(String,not_in,not_in,Text)))),
                Command(Print(print,Expression(String)))
            )`

            multiLevelTester('Test if quoted text not in list print', code, expectedTree, 12, 13);
        })

        describe('Test equality check equal sign', () => {
            const code =
                `if order = burger
                    price is 5`
            const expectedTree =
                `Program(
                    Command(If(if,Condition(EqualityCheck(Text,Op,Expression(Text))))),
                    Command(Assign(Text,is,Expression(Number)))
                )
                `

            multiLevelTester('Test equality check equal sign', code, expectedTree, 12, 13);
        })

        describe('Play tests', () => {
              describe('Play int', () => {
                  const code = 'play 34'
                  const expectedTree = 'Program(Command(Play(play,Expression(Number))))'

                  multiLevelTester('Play note', code, expectedTree, 12, 18)
              })

              describe('Play list access index', () => {
                  const code = 'play list at 1'
                  const expectedTree = 'Program(Command(Play(play,ListAccess(Text,at,Number))))'

                  multiLevelTester('Play note', code, expectedTree, 12, 15)
              })
        })
    })
})
