import {goToHedyLevel5Page, goToHedyPage} from "../tools/navigation/nav";

describe('Is able to run code', () => {
    it('Passes', () => {
      goToHedyPage();

      // Run with correct code
      cy.get('#runit').click();
      cy.get('#okbox').should('be.visible');

      // Run again with same code
      cy.get('#runit').click();
      cy.get('#okbox').should('not.be.visible');

      // Run with incorrect code when skipping faulty code is not possible
      goToHedyLevel5Page();
      cy.get('#editor').type("anders prind 'minder leuk!'\n");
      cy.get('#runit').click();
      cy.get('#errorbox').should('be.visible');
    })

    it('Show a warning dialog about logging in after clicking the run button X times', () => {
      goToHedyPage();

      clickRun(11);

      function clickRun(n) {
        if (n === 0) {
          expectWarning();
          return;
        }
        cy.get('#runit').click();
        clickRun(n - 1);
      }

      function expectWarning() {
        cy.get('#not-logged-in-warning').should('be.visible');
      }
    })
  })
