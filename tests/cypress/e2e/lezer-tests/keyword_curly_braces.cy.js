import { addCurlyBracesToCode } from '../../../../static/js/adventure'


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
    })

    describe('Level 8 tests', () => {
        it('Spaces are maintained', () => {
            const code =  `name = ask 'What is your name?'\nif name is Hedy\n    print 'Welcome Hedy'\n    print 'You can play on your computer!'`
            const expected = `name = {ask} 'What is your name?'\n{if} name {is} Hedy\n    {print} 'Welcome Hedy'\n    {print} 'You can play on your computer!'`
            const generatedCode = addCurlyBracesToCode(code, 8, 'en')

            expect(expected).equal(generatedCode)
        })

        it('Not in should be reduced to just one keyword', () => {
            const code =  `if 1 not in list`
            const expected = `{if} 1 {not_in} list`
            const generatedCode = addCurlyBracesToCode(code, 8, 'en')

            expect(expected).equal(generatedCode)
        })
    })

    describe('Level 12 tests', () => {
        it('Spaces inside calculations should be maintained', () => {
            const code =  `print 2.5 + 2.5 + 3 +4*3`
            const expected = `{print} 2.5 + 2.5 + 3 +4*3`
            const generatedCode = addCurlyBracesToCode(code, 12, 'en')

            expect(expected).equal(generatedCode)
        })
    })
})