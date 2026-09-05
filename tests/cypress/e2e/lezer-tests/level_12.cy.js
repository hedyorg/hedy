import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester";

describe('Tests level 12', () => {
    describe('Test simple call function', () => {
        const code = `
        define func
            print 'hello'
            return 1
        call func
        `
        const expectedTree =
            `Program(
                Command(Define(define,Text)),
                Command(Print(print,String)),
                Command(Return(return,Expression(Number))),
                Command(Call(call,Text))
            )`

        singleLevelTester('Test simple call function level ', code, expectedTree, 12);
    })

    describe('Test simple call function with parameters', () => {
        const code = `
        define func with a, b
            print a ' ' b
        call func with 1, 2
        `
        const expectedTree =
            `Program(
                Command(
                    Define(
                        define,
                        Text,
                        with,
                        Arguments(
                            Expression(Text),
                            Op,
                            Expression(Text)
                        )
                    )
                ),
                Command(
                    Print(print,Expression(Text),String,Expression(Text))
                ),
                Command(
                    Call(
                        call,
                        Text,
                        with,
                        Arguments(Expression(Number),Op,Expression(Number))
                    )
                )
            )`

        singleLevelTester('Test simple call function with parameters with level', code, expectedTree, 12);
    })

    describe('Test simple call function with parameters', () => {
        const code = `print call func with 1, 2`
        const expectedTree =
            `Program(
                Command(
                    Print(
                        print,
                        Expression(
                            Call(
                                call,
                                Text,
                                with,
                                Arguments(Expression(Number),Op,Expression(Number))
                            )
                        )
                    )
                )
            )`

        singleLevelTester('Test simple call function with parameters with level', code, expectedTree, 12);
    })
})
