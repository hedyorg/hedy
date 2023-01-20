import { loginForStudent } from '../tools/login/login';

beforeEach(() => {
  loginForStudent();
  cy.visit('/tutorial');
});

it('initial tutorial page has popup text and editor is visible', () => {
  cy.contains('In this tutorial we will explain').should('be.visible');
  cy.get('#editor').should('be.visible');
});

it('after clicking next, code appears in the editor', () => {
  advanceToStep(2);
  cy.get('#editor').contains('print ___');
});

it('step 6 of the tutorial has translated keywords', () => {
  advanceToStep(6);

  // Untranslated this looks like '{print} Hello world!'
  cy.get('#editor').contains('print Hello world!');
});

/**
 * Go to step 1, 2, 3... of the tutorial
 */
function advanceToStep(step) {
  for (let i = 0; i < step - 1; i++) {
    cy.get('#tutorial_next_button').click();
  }
}