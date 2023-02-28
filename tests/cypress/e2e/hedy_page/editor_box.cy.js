import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to type in the editor box', () => {
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