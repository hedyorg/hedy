import {parser} from "../../../../static/js/lezer-parsers/level1-parser"
import { initializeTranslation } from '../../../../static/js/lezer-parsers/tokens';
import { testTree } from "@lezer/generator/dist/test"

describe('Lezer parser tests for level 1', () => {    
    beforeEach(() => {
        initializeTranslation({keywordLanguage: 'en', level: 1});
    });

    describe('Successfull tests', () => {
        it ('Test print with text', () => {
            const code = 'print hello world\nprint how are you';
            const expectedTree =
            `Program(
                Command(
                    Print(print,Text,Text)
                ),
                Command(
                    Print(print,Text,Text,Text)
                )
            )` ;
            testTree(parser.parse(code), expectedTree);
        });
    
        it('Test ask with text', () => {
            const code = 'ask what is your name';
            const expectedTree = 
            `Program(
                Command(
                    Ask(ask,Text,Text,Text,Text)
                )
            )
            `
            testTree(parser.parse(code), expectedTree);
        });
    
        it('Test echo', () => {
            const code = 'echo hello'
            const expectedTree =
            `Program(
                Command(
                    Echo(echo, Text)
                )
            )
            `
            testTree(parser.parse(code), expectedTree);
        });
    
        it('Test print, ask, echo combined', () => {
            const code = `print Im Hedy the parrot
                ask whats your name?
                echo`
            
            const expectedTree = 
            `Program(
                Command(
                    Print(print,Text,Text,Text,Text)
                ),
                Command(
                    Ask(ask,Text,Text,Text)
                ),
                Command(
                    Echo(echo)
                )
            )`
    
            testTree(parser.parse(code), expectedTree);
        });
    
        it('Test turtle commands: forward, turn, color', () => {
            const code = `forward 20
            turn right
            color black`;
    
            const expectedTree = 
            `Program(
                Command(
                    Turtle(Forward(forward,Text))
                ),
                Command(
                    Turtle(Turn(turn,Text))
                ),
                Command(
                    Turtle(Color(color,Text))
                )
            )`
    
            testTree(parser.parse(code), expectedTree);
        });
    });

    describe('Error tests', () => {
        it('Misspelled command gives ErrorInvalid', () => {
            const code = 'hello world';
            const expectedTree = `Program(Command(ErrorInvalid(Text,Text)))`

            testTree(parser.parse(code), expectedTree);
        });

        it('Correct command after error parses correctly', () => {
            const code = `what is your name
            echo so your name is
            `
            const expectedTree = 
            `Program(
                Command(
                    ErrorInvalid(Text,Text,Text,Text)
                ),
                Command(
                    Echo(echo,Text,Text,Text,Text)
                )
            )`
            
            testTree(parser.parse(code), expectedTree);
        });
    })
})