
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';


describe('Test for users page within admins UI', () => {
  it('should view all users', () => {
    goToAdminUsersPage();
  
    cy.getDataCy('view_all_button').should('be.not.disabled').should('be.visible').click();
  
    cy.location().should((loc) => {
        console.log(loc);
        expect(loc.pathname).equal(Cypress.env('admin_users_page'));
        expect(loc.search).equal('?filter=all');
    })
  })

  it('should be able to use the filter', () => {
    goToAdminUsersPage();
    cy.getDataCy('admin_filter_category').select('last_login')
    cy.getDataCy('admin_start_date').type('2024-10-10')
    cy.getDataCy('admin_end_date').type('2024-10-11')
    cy.getDataCy('submit').click()
    cy.location().should((loc) => {
      expect(loc.search).equal('?filter=last_login&start=2024-10-10&end=2024-10-11')
    })
  })
})