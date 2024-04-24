import {goToHedyLevel5Page, goToHedyPage} from "../tools/navigation/nav";

describe('Is able to run code', () => {
    it('Passes', () => {
      goToHedyPage();

      cy.get('#editor > .cm-editor > .cm-scroller > .cm-content').click();
      cy.focused().type("print Hallo!'\n");
      // Run with correct code
      cy.get('#runit').click();
      cy.get('#okbox').should('be.visible');

      // Run again with same code
      cy.get('#runit').click();
      cy.get('#okbox').should('not.be.visible');

      // Run with incorrect code when skipping faulty code is not possible
      goToHedyLevel5Page();
      cy.get('#editor >.cm-editor').click(); // Wait for the editor to be initialized
      cy.focused().type("anders prind 'minder leuk!'\n");
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

    it ("Old programs doesn't execute after cancelled", () => {
      // Only works for now if the old program is stuck in an ask, and doesn't return an
      // exception
      cy.visit('/hedy/14#tic')
      
      const program_1 = "for i in range 1 to 10\n  choice = ask 'What is your choice?'"
      cy.get('#editor > .cm-editor > .cm-scroller > .cm-content').clear()
      cy.get('#editor > .cm-editor > .cm-scroller > .cm-content').type(program_1)
      cy.get('#runit')

      cy.getBySel('quizmaster').click()
      const program_2 = "name = ask 'what is your name?'"
      cy.get('#editor > .cm-editor > .cm-scroller > .cm-content').clear()
      cy.get('#editor > .cm-editor > .cm-scroller > .cm-content').type(program_2)
      cy.get('#runit').click()
      cy.get('#ask-modal').type('Hedy')
      cy.get('#ask-modal > form').submit()

      cy.get('#ask-modal').should('not.be.visible')
    })
  })
