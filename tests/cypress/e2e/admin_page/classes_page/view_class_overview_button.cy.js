import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminClassesPage } from '../../tools/navigation/nav.js';

describe('View class overview button', () => {
  it('passes', () => {
    loginForAdmin();
    goToAdminClassesPage();

    cy.get(':nth-child(1) > #overview_cell > a')
      .should('be.visible')
      .should('be.not.disabled');
  })
})
