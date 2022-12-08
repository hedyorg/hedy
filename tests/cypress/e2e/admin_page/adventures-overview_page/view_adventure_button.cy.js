import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminAdventuresOverviewPage } from '../../tools/navigation/nav.js';

describe('View adventure button', () => {
  it('passes', () => {
    loginForAdmin();
    goToAdminAdventuresOverviewPage()

    cy.get('#statistics_cell')
      .should('be.visible')
      .should('be.not.disabled')
      .click();

    cy.url()
      .should('not.eq', Cypress.config('baseUrl') + Cypress.env('admin_page'));
  })
})
