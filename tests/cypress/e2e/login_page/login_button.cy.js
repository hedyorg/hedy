import {goToLogin} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Login button test', () => {
  it('passes', () => {
    goToLogin();

    // Tests login button type and visibility
    cy.get('#login_button')
      .should('be.visible')
      .should('not.be.disabled')
      .should('have.attr', 'type', 'submit')

    // Tests login button on existing account
    loginForUser();
    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('landing_page'));
  })
})
