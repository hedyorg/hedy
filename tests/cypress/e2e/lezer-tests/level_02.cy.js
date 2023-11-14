import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tets for level 2', () => {
    describe('Successfull tests level 2', () => {
        describe('Test assign with keyword inside', () => {
            const code = `command is print hello world`
            const expectedTree =
                `Program(
                    Command(
                        Assign(Text,is,Text,Text,Text)
                    )
                )
                `

            multiLevelTester('Test assign with keyword inside', code, expectedTree, 2, 5);
        });

        describe('Test ask assignment', () => {
            const code = `name is ask what is your name`
            const expectedTree =
                `Program(
                    Command(
                        Ask(Text,is,ask,Text,Text,Text,Text)
                    )
                )`

            multiLevelTester('Test ask assignment', code, expectedTree, 2, 3);
        })

        describe('Test sleep with number', () => {
            const code = `sleep 5`
            const expectedTree =
                `Program(
                    Command(
                        Sleep(sleep,Text)
                    )
                )`;

            multiLevelTester('Test sleep with number', code, expectedTree, 2, 5);
        });

        describe('Tests empty sleep', () => {
            const code = `sleep`
            const expectedTree =
                `Program(
                    Command(
                        Sleep(sleep)
                    )
                )`;

            multiLevelTester('Test empty sleep', code, expectedTree, 2, 18);
        });

        describe('Test turtle assignment', () => {
            const code = `angle is 90
                turn angle
                forward 20`;

            const expectedTree = `Program(
                    Command(
                        Assign(Text,is,Text)
                    ),
                    Command(
                        Turtle(Turn(turn,Text))
                    ),
                    Command(
                        Turtle(Forward(forward,Text))
                    )
                )`
            
            multiLevelTester('Test turtle assignment', code, expectedTree, 2, 5);
        });
    });
});