import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tets for level 7', () => {
    describe('Successful tests', () => {
        describe('Test repeat with integer', () => {
            const code = "repeat 3 times print 'Hedy is fun!'"
            const expectedTree = `
            Program(
                Command(
                    Repeat(
                        repeat,
                        Int,
                        times,
                        Command(
                            Print(print,String)
                        )
                    )
                )
            )`

            singleLevelTester('Test repeat with integer ', code, expectedTree, 7)
        })

        describe('Test repeat with text', () => {
            const code = "repeat n times print 'Hedy is fun!'"
            const expectedTree = `
            Program(
                Command(
                    Repeat(
                        repeat,
                        Text,
                        times,
                        Command(
                            Print(print,String)
                        )
                    )
                )
            )`

            singleLevelTester('Test repeat with text', code, expectedTree, 7)
        })

        describe('Test repeat with if inside', () => {
            const code = "repeat 3 times if name is Hedy print 'hello world'"
            const expectedTree = `
            Program(
                Command(
                    Repeat(
                        repeat,
                        Int,
                        times,
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Expression(Text))),
                                IfLessCommand(Print(print,String))
                            )
                        )
                    )
                )
            )`

            singleLevelTester('Test repeat with if inside', code, expectedTree, 7)
        })

        describe('Test repeat with if and else inside', () => {
            const code = "repeat 3 times if name is Hedy print 'hello world' else print 'hello world'"
            const expectedTree = `
            Program(
                Command(
                    Repeat(
                        repeat,
                        Int,
                        times,
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Expression(Text))),
                                IfLessCommand(Print(print,String)),
                                Else(
                                    else,
                                    IfLessCommand(Print(print,String))
                                )
                            )
                        )
                    )
                )
            )
            `

            singleLevelTester('Test repeat with if and else inside', code, expectedTree, 7)
        })

        describe('Test repeat with if and else inside, if command on new line', () => {
            const code = "repeat 3 times if name is Hedy\nprint 'hello world' else print 'hello world'"
            const expectedTree = `
            Program(
                Command(
                    Repeat(
                        repeat,
                        Int,
                        times,
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Expression(Text))),
                                IfLessCommand(Print(print,String)),
                                Else(
                                    else,
                                    IfLessCommand(Print(print,String))
                                )
                            )
                        )
                    )
                )
            )
            `

            singleLevelTester('Test repeat with if and else inside, if command on new line', code, expectedTree, 7)
        })

        describe('Test repeat with if and else inside, if command on new line', () => {
            const code = "repeat 3 times if name is Hedy\nprint 'hello world'\nelse print 'hello world'"
            const expectedTree = `
            Program(
                Command(
                    Repeat(
                        repeat,
                        Int,
                        times,
                        Command(
                            If(
                                if,
                                Condition(EqualityCheck(Text,is,Expression(Text))),
                                IfLessCommand(Print(print,String))))
                            )
                        ),
                        Command(
                            Else(
                                else,
                                IfLessCommand(Print(print,String)
                            )
                        )
                    )
                )
            `

            singleLevelTester('Test repeat with if and else inside, if command on new line', code, expectedTree, 7)
        })

        describe('Test if with repeat inside', () => {
            const code = "if name is Hedy repeat 3 times print 'hello world'"
            const expectedTree = `
            Program(
                Command(
                    If(
                        if,
                        Condition(EqualityCheck(Text,is,Expression(Text))),
                        IfLessCommand(
                            Repeat(
                                repeat,
                                Int,
                                times,
                                Command(Print(print,String))
                            )
                        )
                    )
                )
            )
            `

            singleLevelTester('Test if with repeat inside', code, expectedTree, 7)
        })

        describe('Combined test', () => {
            let code = `repeat 2 times answer = ask 'Did you know you could ask a question multiple times?'
            if answer is yes repeat 2 times print 'You knew that already!'
            else repeat 3 times print 'You have learned something new!'
            `

            code = code.split('\n').map(line => line.trim()).join('\n')

            const expectedTree = `
            Program(
                Command(
                    Repeat(
                        repeat,
                        Int,
                        times,
                        Command(Ask(Text,Op,ask,String))
                    )
                ),
                Command(
                    If(if,
                        Condition(EqualityCheck(Text,is,Expression(Text))),
                        IfLessCommand(
                            Repeat(
                                repeat,
                                Int,
                                times,
                                Command(Print(print,String)))
                            )
                    )
                ),
                Command(
                    Else(
                        else,
                        IfLessCommand(
                            Repeat(
                                repeat,
                                Int,
                                times,
                                Command(Print(print,String))
                            )
                        )
                    )
                )
            )`

        singleLevelTester('Combined test', code, expectedTree, 7)
        })
    })
})