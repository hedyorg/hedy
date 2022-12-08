import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminStatsPage } from '../../tools/navigation/nav.js';

describe('Return to admin page button', () => {
  it('passes', () => {
    loginForAdmin();
    goToAdminStatsPage()

    cy.get('#return_to_admin_page_button')
      .should('be.visible')
      .should('be.not.disabled')
      .click();

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('admin_page'));
  })
})
