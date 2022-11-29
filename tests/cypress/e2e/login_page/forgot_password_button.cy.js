import {goToLogin} from '../tools/navigation/nav.js'

describe('Forgot password button test', () => {
  it('passes', () => {
    goToLogin();

    // Tests forgot password button type and visibility
    cy.get('#forgot_password_button')
      .should('be.visible')
      .should('not.be.disabled')
      .should('have.attr', 'type', 'submit')
      .click()

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('recover_page'));
  })
})
