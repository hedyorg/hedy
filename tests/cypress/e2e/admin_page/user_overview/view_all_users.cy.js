
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';

describe('View all users', () => {
  it('passes', () => {
    goToAdminUsersPage();

    cy.get('#view_all_button').should('be.not.disabled').should('be.visible').click();

    cy.location().should((loc) => {
        console.log(loc);
        expect(loc.pathname).equal(Cypress.env('admin_users_page'));
        expect(loc.search).equal('?filter=all');
    })
    
  })
})
