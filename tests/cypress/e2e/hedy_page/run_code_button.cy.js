import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to run code', () => {
    it('Passes', () => {
      goToHedyPage();
      
      // Run with correct code
      cy.get('#runit').click();
      cy.get('#okbox').should('be.visible');

      // Run with incorrect code
      cy.get('#editor').type('\np');
      cy.get('#runit').click();
      cy.get('#errorbox').should('be.visible');
    })
  })