
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';

describe('View all users', () => {
  it('passes', () => {
    goToAdminUsersPage();
    
    cy.get('.p-2 input[type=checkbox]').each((el) => {
        cy.wrap(el).check();
        cy.wrap(el).uncheck();
    })

    
  })
})
