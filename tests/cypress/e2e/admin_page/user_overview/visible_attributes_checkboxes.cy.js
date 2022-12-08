



import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';

describe('View all users', () => {
  it('passes', () => {
    loginForAdmin();
    cy.get('[onclick="window.open(\'/admin/users\', \'_self\')"]').click();
    
    cy.get('.p-2 input[type=checkbox]').each((el) => {
        cy.wrap(el).check();
        cy.wrap(el).uncheck();
    })

    
  })
})
