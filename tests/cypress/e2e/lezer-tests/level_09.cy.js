import { multiLevelTester } from "../tools/lezer/lezer_tester";

describe('Tests level 9', () => {
    describe('Test for Spanish', () => {
        const code = 
        `para animal en animales
            imprimir 'Yo amo ' animal
        `
        
        const expectedTree = `
        Program(
            Command(For(for,Text,in,Text)),
            Command(Print(print,String,Expression(Text)))
        )`

        multiLevelTester('Test for Spanish', code, expectedTree, 10, 11, 'es');
    })
})