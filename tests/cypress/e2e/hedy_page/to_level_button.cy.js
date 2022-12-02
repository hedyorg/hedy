import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to use "Go to level x" button', () => {
    it('Passes', () => {
      // Test when code is unchanged
      goToHedyPage();
      cy.get('#next_level_button').click();
      cy.url().should('include', Cypress.env('hedy_level2_page'));

      // Test when code is changed
      goToHedyPage();
      cy.get('#editor').type('hello');
      cy.get('#next_level_button').click();
      cy.get('#modal-yes-button').click();
      cy.url().should('include', Cypress.env('hedy_level2_page'));
    })
  })