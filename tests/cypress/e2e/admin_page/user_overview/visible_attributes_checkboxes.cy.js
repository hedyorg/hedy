
import { goToAdminUsersPage } from '../../tools/navigation/nav.js';

it('checkboxes should be visible', () => {
  goToAdminUsersPage();

  cy.get('.p-2 input[type=checkbox]').each((el) => {
      cy.wrap(el).check();
      cy.wrap(el).uncheck();
  })
})
