
import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';

describe('Return to admin page', () => {
  it('passes', () => {
    loginForAdmin();
    cy.get('[onclick="window.open(\'/admin/users\', \'_self\')"]').click();

    cy.get('.fle > .green-btn').should('be.not.disabled').should('be.visible').click();

    cy.location().should((loc) => {
        expect(loc.pathname).equal('/admin');
    })
    
  })
})
