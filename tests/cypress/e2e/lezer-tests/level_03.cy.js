import { multiLevelTester, singleLevelTester } from "../tools/lezer/lezer_tester"

describe('Lezer parser tests for level 3', () => {
    describe('Successfull tests', () => {
        describe('List tests', () => {
            describe('Test assign list', () => {
                const code = 'animals is dogs, cats, turtles';
                const expectedTree = 
                    `Program(
                        Command(
                            AssignList(Text,is,Text,Comma,Text,Comma,Text)
                        )
                    )`
                
                multiLevelTester('Test assign list', code, expectedTree, 3, 5);
            });

            describe('Test list random access inside print', () => {
                const code = 'print animals at random'
                const expectedTree = 
                    `Program(
                        Command(
                            Print(print,ListAccess(Text,at,random))
                        )
                    )`
                
                multiLevelTester('Test list random access inside print', code, expectedTree, 3, 5);
            });

            describe('Test list access with number', () => {
                const code = 'print animals at 1'
                const expectedTree = 
                    `Program(
                        Command(
                            Print(print,ListAccess(Text,at,Text))
                        )
                    )`
                
                multiLevelTester('Test list random access inside print', code, expectedTree, 3, 5);            
            });

            describe('Assign with list access', () => {
                const code = 'choice is choices at 1';
                const expectedTree = `Program(Command(Assign(Text,is,ListAccess(Text,at,Text))))`;

                multiLevelTester('Assign with list access', code, expectedTree, 3, 5);
            })
        });
        describe('Add tests', () => {
            describe('Add single word to list', () => {
                const code = 'add word to list'
                const expectedTree = 'Program(Command(Add(add,Text,toList,Text)))'

                multiLevelTester('Add single word to list', code, expectedTree, 3, 11)
            });

            describe('Add multiple words to list', () => {
                const code = 'add sour cream to sauces'
                const expectedTree = 'Program(Command(Add(add,Text,Text,toList,Text)))'

                multiLevelTester('Add multiple words to list', code, expectedTree, 3, 11)
            });

            describe('Remove single word from list', () => {
                const code = 'remove word from list'
                const expectedTree = 'Program(Command(Remove(remove,Text,from,Text)))'

                multiLevelTester('Remove single word from list', code, expectedTree, 3, 11)
            });

            describe('Remove multiple words from list', () => {
                const code = 'remove sour cream from sauces'
                const expectedTree = 'Program(Command(Remove(remove,Text,Text,from,Text)))'

                multiLevelTester('Remove multiple words from list', code, expectedTree, 3, 11)
            });
        })
    });
})