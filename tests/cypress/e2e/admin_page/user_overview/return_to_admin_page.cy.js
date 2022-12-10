
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';

describe('Return to admin page', () => {
  it('passes', () => {
    goToAdminUsersPage();
    cy.get('#return_button').should('be.not.disabled').should('be.visible').click();

    cy.location().should((loc) => {
        expect(loc.pathname).equal(Cypress.env('admin_page'));
    })
    
  })
})
