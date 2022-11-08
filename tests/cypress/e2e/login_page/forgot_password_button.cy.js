import {goToLogin} from '../tools/navigation/nav.js'

describe('Forgot password button test', () => {
  it('passes', () => {
    goToLogin();

    // Tests forgot password button type and visibility
    cy.get('button[class*="blue-btn"]')
      .should('be.visible')
      .should('have.attr', 'type', 'submit')
      .contains('Forgot your password?')
      .click()

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('recover_page'));
  })
})
