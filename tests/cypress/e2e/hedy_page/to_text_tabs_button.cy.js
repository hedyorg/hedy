import {goToHedyPage} from "../tools/navigation/nav";

describe('Navigating through the tabs with the buttons', () => {
    beforeEach(() => {
      goToHedyPage();
    })
    it('should be able to go to the next and previous tab', () => {
      // Test when code is unchanged
      cy.get('.next-tab').click();
      cy.url().should('include', "print_command");

      // Test when code is changed
      goToHedyPage();
      cy.get('#editor').type('hello');
      cy.get('.next-tab').click();
      cy.url().should('include', "print_command");


      // Now go back to #default
      cy.get('.previous-tab').click();
      cy.url().should('include', "default");
    })
  })