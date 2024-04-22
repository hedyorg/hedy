
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';

it('should return to admin page', () => {
  goToAdminUsersPage();
  cy.get('[data-cy="return_button"]').should('be.not.disabled').should('be.visible').click();

  cy.location().should((loc) => {
      expect(loc.pathname).equal(Cypress.env('admin_page'));
  })
})
