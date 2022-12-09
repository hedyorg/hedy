import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to type in the editor box', () => {
    it('Passes', () => {
      goToHedyPage();

      // This doesn't work!
      cy.get('#editor > textarea').clear({force: true});
      cy.get('#editor').type('ask What is your name?\necho hello');
      cy.get('#editor > .ace_scroller > .ace_content .ace_line').each((element, index) => {
        if(index == 0) {
          cy.get(element).should('have.text', 'ask What is your name?');
        }
        if(index == 1) {
          cy.get(element).should('have.text', 'echo hello');
        }
      })
    })
})