import {goToHedyPage} from "../tools/navigation/nav";

describe('Navigating through the tabs with the buttons', () => {
    it('should be able to go to the next and previous tab', () => {
      // Test when code is unchanged
      goToHedyPage();
      cy.wait(500)
      cy.get('.next-tab').click();
      cy.wait(500)
      cy.url().should('include', "print_command");

      // Test when code is changed
      goToHedyPage();
      cy.wait(500)
      cy.get('#editor').type('hello');
      cy.get('.next-tab').click();
      cy.wait(500)
      cy.url().should('include', "print_command");


      // Now go back to #default
      cy.get('.previous-tab').click();
      cy.wait(500)
      cy.url().should('include', "default");
    })
  })