import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminStatsPage } from '../../tools/navigation/nav.js';

describe('Past 4 weeks toggle', () => {
  it('passes', () => {
    loginForAdmin();
    goToAdminStatsPage();

    cy.get('#period_toggle_past_4_weeks')
      .should('be.visible')
      .should('be.not.disabled');
  })
})
