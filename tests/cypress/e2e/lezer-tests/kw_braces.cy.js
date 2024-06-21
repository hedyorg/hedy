const YAML = require('yaml')
import { addCurlyBracesToCode } from '../../../../static/js/adventure'

describe('YAML opening test', () => {
    it('should be able to open the yaml file and parse the snippets', () => {
        cy.readFile('../content/pages/es.yaml').then((str) => {
            const spanish = YAML.parse(str)
            let code_snippets = []
            for (let i = 0; i < 18; i++) {
                const sections = spanish['teacher-guide'][8].levels[i].sections                
                for (const section of sections) {
                    let examples = []
                    for (const code of [section.example.solution_code, section.example.error_code]) {
                        examples.push(addCurlyBracesToCode(code, i + 1, 'es'))
                    }
                    code_snippets.push(examples);
                }
            }            
            for (let i = 0, j = 0; i < 18; i++) {
                const sections = spanish['teacher-guide'][8].levels[i].sections
                for (const section of sections) {
                    section.example.solution_code = code_snippets[j][0];
                    section.example.error_code = code_snippets[j][1];
                    j++;
                }
            }
            cy.writeFile('../content/pages/es.yaml', YAML.stringify(spanish, {flowCollectionPadding: false, lineWidth: 4000, singleQuote: true}))
            cy.writeFile('code_snippets.txt', code_snippets.join('\n'))
        })
    })
})