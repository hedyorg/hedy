import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to type in the editor box', () => {
    it('Passes', () => {
      goToHedyPage();

      cy.get('#editor > .ace_scroller > .ace_content').type('\nask What is your name\necho hello');
      cy.get('#editor > .ace_scroller > .ace_content .ace_line').each((element, index) => {
        if(index == 0) {
          cy.get(element).should('have.text', 'print hello world!');
        }
        if(index == 1) {
          cy.get(element).should('have.text', 'ask What is your name');
        }
        if(index == 2) {
          cy.get(element).should('have.text', 'echo hello');
        }
      })
    })
})