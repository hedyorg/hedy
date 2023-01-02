import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminStatsPage } from '../../tools/navigation/nav.js';

describe('This week toggle', () => {
  it('passes', () => {
    loginForAdmin();
    goToAdminStatsPage();

    cy.get('#period_toggle_this_week')
      .should('be.visible')
      .should('be.not.disabled');
  })
})
