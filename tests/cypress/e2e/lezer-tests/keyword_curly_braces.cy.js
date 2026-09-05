import { addCurlyBracesToCode, addCurlyBracesToKeyword } from '../../../../static/js/keyword-curly-braces'


describe('Adds curly braces around keywords, mainting the original code as much as possible', () => {
    describe('Level 1 tests', () => {
        it('print, ask and echo should work correctly', () => {
            const code = 'print hello world\nask what is your name\necho your name is'
            const expected = '{print} hello world\n{ask} what is your name\n{echo} your name is'
            const generatedCode = addCurlyBracesToCode(code, 1, 'en')

            expect(expected).to.equal(generatedCode)
        })

        it('print, ask and echo should work correctly in Spanish', () => {
            const code = 'imprimir hello world\npreguntar what is your name\neco your name is'
            const expected = '{print} hello world\n{ask} what is your name\n{echo} your name is'
            const generatedCode = addCurlyBracesToCode(code, 1, 'es')

            expect(expected).to.equal(generatedCode)
        })

        it('Code containing errors should still be added correctly', () => {
            const code = 'print hello world\nthis should be the same'
            const expected = '{print} hello world\nthis should be the same'
            const generatedCode = addCurlyBracesToCode(code, 1, 'en')

            expect(expected).to.equal(generatedCode)
        })

        it('Code containing errors should still be added correctly in Spanish', () => {
            const code = 'imprimir hello world\nthis should be the same'
            const expected = '{print} hello world\nthis should be the same'
            const generatedCode = addCurlyBracesToCode(code, 1, 'es')

            expect(expected).to.equal(generatedCode)
        })

        it('print, ask and echo should work correctly in French', () => {
            const code = 'affiche hello world\ndemande what is your name\nréponds your name is'
            const expected = '{print} hello world\n{ask} what is your name\n{echo} your name is'
            const generatedCode = addCurlyBracesToCode(code, 1, 'fr')

            expect(expected).to.equal(generatedCode)
        })

        it('print, ask and echo should work correctly in Dutch', () => {
            const code = 'print hello world\nvraag what is your name\necho your name is'
            const expected = '{print} hello world\n{ask} what is your name\n{echo} your name is'
            const generatedCode = addCurlyBracesToCode(code, 1, 'nl')

            expect(expected).to.equal(generatedCode)
        })

        it('print, ask and echo should work correctly in Arabic', () => {
            const code = 'قول hello world\nاسأل what is your name\nردد your name is'
            const expected = '{print} hello world\n{ask} what is your name\n{echo} your name is'
            const generatedCode = addCurlyBracesToCode(code, 1, 'ar')

            expect(expected).to.equal(generatedCode)
        })

        it('code already containing curly braces should remain unchanged', () => {
            const code = '{print} hello world\n{ask} what is your name\n{echo} your name is'
            const generatedCode = addCurlyBracesToCode(code, 1, 'en')

            expect(generatedCode).to.equal(code)
        })
    })

    describe('Level 3 tests', () => {
        it('add ... to command', () => {
            const code = `añadir gusta a animales`;
            const expected = `{add} gusta {to_list} animales`;
            const generatedCode = addCurlyBracesToCode(code, 3, 'es');

            expect(expected).to.equal(generatedCode);
        })
    })

    describe('Level 9 tests', () => {
        it('Spaces are maintained', () => {
            const code = `name = ask 'What is your name?'\nif name is Hedy\n    print 'Welcome Hedy'\n    print 'You can play on your computer!'`
            const expected = `name = {ask} 'What is your name?'\n{if} name {is} Hedy\n    {print} 'Welcome Hedy'\n    {print} 'You can play on your computer!'`
            const generatedCode = addCurlyBracesToCode(code, 9, 'en')

            expect(expected).equal(generatedCode)
        })

        it('Not in should be reduced to just one keyword', () => {
            const code = `if 1 not in list`
            const expected = `{if} 1 {not_in} list`
            const generatedCode = addCurlyBracesToCode(code, 9, 'en')

            expect(expected).equal(generatedCode)
        })
    })

    describe('Level 12 tests', () => {
        it('Spaces inside calculations should be maintained', () => {
            const code = `print 2.5 + 2.5 + 3 +4*3`
            const expected = `{print} 2.5 + 2.5 + 3 +4*3`
            const generatedCode = addCurlyBracesToCode(code, 12, 'en')

            expect(expected).equal(generatedCode)
        })
    })

    describe('Inline keyword tests', () => {
        it('wraps multi-word keyword not in', () => {
            const generatedKeyword = addCurlyBracesToKeyword('not in', 'en');

            expect(generatedKeyword).to.equal('{not_in}');
        })

        it('wraps direct keyword key not_in', () => {
            const generatedKeyword = addCurlyBracesToKeyword('not_in', 'en');

            expect(generatedKeyword).to.equal('{not_in}');
        })

        it('leaves unknown inline text unchanged', () => {
            const generatedKeyword = addCurlyBracesToKeyword('totally_unknown_keyword', 'en');

            expect(generatedKeyword).to.equal('totally_unknown_keyword');
        })

        it('wraps translated print keyword in Spanish', () => {
            const generatedKeyword = addCurlyBracesToKeyword('imprimir', 'es');

            expect(generatedKeyword).to.equal('{print}');
        })

        it('wraps translated ask keyword in French', () => {
            const generatedKeyword = addCurlyBracesToKeyword('demande', 'fr');

            expect(generatedKeyword).to.equal('{ask}');
        })

        it('wraps translated ask keyword in Dutch', () => {
            const generatedKeyword = addCurlyBracesToKeyword('vraag', 'nl');

            expect(generatedKeyword).to.equal('{ask}');
        })

        it('wraps translated print keyword in Arabic', () => {
            const generatedKeyword = addCurlyBracesToKeyword('قول', 'ar');

            expect(generatedKeyword).to.equal('{print}');
        })
    })
})