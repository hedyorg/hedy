import {goToLogin} from '../tools/navigation/nav.js'

describe('Login button test', () => {
  it('passes', () => {
    goToLogin();

    // Tests login button type and visibility
    cy.get('button[class*="green-btn mt-2"]')
      .should('be.visible')
      .should('have.attr', 'type', 'submit')
      .should('have.text', 'Log in');

    // Tests login button on existing account
    cy.get('#username')
      .type('student_user');
    cy.get('#password')
      .type('student_user123');
    cy.get('button[class*="green-btn mt-2"]')
       .click();
    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('landing_page'));
  })
})
