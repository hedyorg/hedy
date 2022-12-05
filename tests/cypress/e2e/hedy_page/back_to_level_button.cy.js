import {goToHedyLevel2Page, goToHedyPage} from "../tools/navigation/nav";

describe('Is able to use "Go back to level x" button', () => {
    it('Passes', () => {
      // Test when code is unchanged
      goToHedyLevel2Page();
      cy.get('#prev_level_button').click();
      cy.url().should('include', Cypress.env('hedy_page'));

      // Test when code is changed
      goToHedyLevel2Page();
      cy.get('#editor').type('hello');
      cy.get('#prev_level_button').click();
      cy.get('#modal-yes-button').click();
      cy.url().should('include', Cypress.env('hedy_page'));
    })
  })