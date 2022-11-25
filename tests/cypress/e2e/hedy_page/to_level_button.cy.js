import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to use "Go to level x" button', () => {
    it('Passes', () => {
      let newUrl = Cypress.env('hedy_page') + '/2';

      // Test when code is unchanged
      goToHedyPage();
      cy.get('#next_level_button').click();
      cy.url().should('include', newUrl);

      // Test when code is changed
      goToHedyPage();
      cy.get('#editor').type('hello');
      cy.get('#next_level_button').click();
      cy.get('#modal-yes-button').click();
      cy.url().should('include', newUrl);
    })
  })