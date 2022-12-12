import { loginForAdmin } from '../../tools/login/login.js'

describe('Users overview button', () => {
  it('passes', () => {
    loginForAdmin();


      cy.get('#adventures_button')
      .should('be.visible')
      .should('be.not.disabled')
      .click();

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('admin_adventures_page'));
  })
})
