import { multiLevelTester } from "../tools/lezer/lezer_tester";

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

    multiLevelTester('Test for Spanish', code, expectedTree, 11, 12, 'es');
})

describe('Quoted list values', () => {
    const code = `animals is 'cat', "dog"`
    const expectedTree =
        'Program(Command(AssignList(Text,is,String,Op,String)))'

    multiLevelTester('Quoted list values', code, expectedTree, 11, 12)
})
