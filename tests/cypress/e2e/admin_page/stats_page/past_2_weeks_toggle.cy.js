import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminStatsPage } from '../../tools/navigation/nav.js';

describe('Past 2 weeks toggle', () => {
  it('passes', () => {
    loginForAdmin();
    goToAdminStatsPage();

    cy.get('#period_toggle_past_2_weeks')
      .should('be.visible')
      .should('be.not.disabled');
  })
})
