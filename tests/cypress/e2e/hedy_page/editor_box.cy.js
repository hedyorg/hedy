import {goToHedyPage} from "../tools/navigation/nav";
const YAML = require('js-yaml')
describe('Is able to type in the editor box', () => {
  it('This might work', () => {
    cy.readFile('../content/adventures/en.yaml').then((yamlString) =>{
      var adventures = YAML.load(yamlString)
      cy.log(adventures.adventures.default.levels['1'].example_code);
    })
  });  
  it('Passes', () => {
      goToHedyPage();
      // click on textaread to get focus
      cy.getBySel('language-dropdown').click();
      var languages = []
      cy.get("[data-cy^='switch-lang-']").each(($el, index, $list) => {
       languages.push($el.data('cy'));
      }).then(() => {
        cy.getBySel('language-dropdown').click();
        for (let i = 0; i < languages.length; i++) {
          cy.getBySel('language-dropdown').click();
          cy.getBySel(languages[i]).click();
          cy.get('#editor > .ace_scroller > .ace_content').click();
          // empty textarea
          cy.focused().clear()
          cy.get('#editor').type('print Hello world');
          cy.get('#editor > .ace_scroller > .ace_content').should('contain.text', 'print Hello world');
          cy.get('#runit').click();
          cy.get('#output').should('contain.text', 'Hello world');
        }
      })
    })
})