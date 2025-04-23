import {goToHedyLevel, goToHedyPage, clickAdventureIndexButton} from "../tools/navigation/nav";
import {codeEditorContent} from "../tools/programs/program";

describe('Is able to run code', () => {
  it('Show OK box only on the first program run', () => {
    goToHedyPage();

    codeEditorContent().click();
    codeEditorContent().type("print Hallo!'\n");
    // Run with correct code
    cy.get('#runit').click();
    cy.get('#okbox').should('be.visible');

    // Run again with same code
    cy.get('#runit').click();
    cy.get('#okbox').should('not.be.visible');
  })

  it('Show error box for incorrect program', () => {
    // Run with incorrect code when skipping faulty code is not possible
    goToHedyLevel(5);

    codeEditorContent().click();
    codeEditorContent().type("anders prind 'minder leuk!'\n");

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
      cy.get('#not_logged_in_warning').should('be.visible');
    }
  })

  it ("Old programs do not execute after cancellation", () => {
    // Only works for now if the old program is stuck in an ask, and doesn't return an
    // exception
    cy.visit('/hedy/14#tic')

    const program_1 = "for i in range 1 to 10\n  choice = ask 'What is your choice?'"
    cy.intercept('/parse').as('parse')
    codeEditorContent().clear()
    codeEditorContent().type(program_1)
    cy.get('#runit').click()
    cy.wait('@parse')

    clickAdventureIndexButton()
    cy.getDataCy('quizmaster').click()
    const program_2 = "name = ask 'what is your name?'"
    codeEditorContent().clear()
    codeEditorContent().type(program_2)
    cy.get('#runit').click()
    cy.wait('@parse')
    cy.get('#ask_modal').type('Hedy')
    cy.get('#ask_modal > form').submit()

    cy.get('#ask_modal').should('not.be.visible')
  })

  it("Hide the stop button after executing a program", () => {
    cy.intercept('/parse').as('parse')
    cy.visit('/hedy/2')

    const program = "var1 is 1\nvar2 is 2\nvar3 is 3\nvar4 is 4\nprint var1 var2 var3 var4"
    codeEditorContent().clear()
    codeEditorContent().type(program)

    cy.get('#runit').click()
    cy.wait('@parse')
    // A hardcoded wait to ensure that the program finishes execution
    cy.wait(500)
    cy.get('#stopit').should('not.be.visible')
    cy.get('#runit').should('be.visible')
    cy.get('#variable_list').should('be.visible').and('have.text', 'var1: 1var2: 2var3: 3var4: 4')
  })

  it('Running a program with the turtle, still should show the variables', () => {
    cy.intercept('/parse').as('parse')
    cy.visit('/hedy/2')

    let code = "forward 10";
    for(let i = 1; i <= 20; i++) {
      code += `\nangle${i} is 90`
    }
    codeEditorContent().clear()
    codeEditorContent().type(code)

    cy.get('#runit').click()
    cy.wait('@parse')

    cy.wait(500)
    cy.get('#stopit').should('not.be.visible')
    cy.get('#runit').should('be.visible')

    cy.get('#variable_button').click()
    cy.get('#variables').invoke('height').should('gte', 50)
  })
})
