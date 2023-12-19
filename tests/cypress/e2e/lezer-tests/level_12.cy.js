import { multiLevelTester } from "../tools/lezer/lezer_tester";

describe('Tests level 12', () => {
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
})