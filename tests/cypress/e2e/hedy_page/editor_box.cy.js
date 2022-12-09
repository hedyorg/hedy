import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to type in the editor box', () => {
    it('Passes', () => {
      goToHedyPage();

      cy.get('#editor').type('ask What is your name?\necho hello');
      cy.get('#editor > .ace_scroller > .ace_content').should('have.text', 'ask What is your name?');
      cy.get('#editor > .ace_scroller > .ace_content').should('have.text', 'echo hello');
    })
})