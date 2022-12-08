

import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';

describe('View all users', () => {
  it('passes', () => {
    loginForAdmin();
    cy.get('[onclick="window.open(\'/admin/users\', \'_self\')"]').click();
    cy.get('.yellow-btn').should('be.not.disabled').should('be.visible').click();

    cy.location().should((loc) => {
        console.log(loc);
        expect(loc.pathname).equal('/admin/users');
        expect(loc.search).equal('?filter=all');
    })
    
  })
})
