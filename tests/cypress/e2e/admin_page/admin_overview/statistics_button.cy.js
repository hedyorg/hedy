import { loginForAdmin } from '../../tools/login/login.js'

describe('Users overview button', () => {
  it('passes', () => {
    loginForAdmin();


      cy.get('#statistics_button')
      .should('be.visible')
      .should('be.not.disabled')
      .click();

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('admin_stats_page'));
  })
})
