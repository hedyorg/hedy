import {goToLogin} from '../tools/navigation/nav.js'

describe('Login button test', () => {
  it('passes', () => {
    goToLogin();

     // Tests hidden modal alert text
    cy.get('#modal_alert_text')
      .should('not.be.visible')
      .should('be.empty');

    // Tests login button type and visibility
    cy.get('button[class*="green-btn mt-2"]')
      .should('be.visible')
      .should('have.attr', 'type', 'submit')
      .should('have.text', 'Log in');

    // Tests visibility of modal alert text/ login non existing account
    cy.get('#username')
      .type('anonexistingaccount123@#$%^!')
    cy.get('#password')
      .type('anonexistingpassword123@#$%^!')
    cy.get('button[class*="green-btn mt-2"]')
       .click()
    cy.get('#modal_alert_text')
      .should('be.visible')
      .should('have.text', 'Invalid username/password. No account?');

    // Reset fields
    cy.get('#username')
      .clear();
    cy.get('#password')
      .clear();

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