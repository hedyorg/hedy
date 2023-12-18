import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tets for level 2', () => {
    describe('Successfull tests level 2', () => {
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
    })
});