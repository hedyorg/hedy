import {goToLogin} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Login button test', () => {
  it('passes', () => {
    goToLogin();

    // Tests login button type and visibility
    cy.get('button[class*="green-btn mt-2"]')
      .should('be.visible')
      .should('have.attr', 'type', 'submit')
      .should('have.text', 'Log in');

    // Tests login button on existing account
    loginForUser();
    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('landing_page'));
  })
})
