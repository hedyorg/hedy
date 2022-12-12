import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminStatsPage } from '../../tools/navigation/nav.js';

describe('Past year toggle', () => {
  it('passes', () => {
    loginForAdmin();
    goToAdminStatsPage();

    cy.get('#period_toggle_past_year')
      .should('be.visible')
      .should('be.not.disabled');
  })
})
