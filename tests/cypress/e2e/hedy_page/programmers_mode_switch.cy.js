import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to switch programmers mode on and of', () => {
    it('Passes', () => {
      goToHedyPage();
      
      cy.get('#toggle_circle').click(); // Programmers mode is switched on
      cy.get('#adventures-tab').should('not.be.visible');

      cy.get('#toggle_circle').click(); // Programmers mode is switched off
      cy.get('#adventures-tab').should('be.visible');
    })
  })