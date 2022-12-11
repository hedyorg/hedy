import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminAdventuresPage } from '../../tools/navigation/nav.js';

describe('View adventure button', () => {
  it('passes', () => {
    loginForAdmin();
    goToAdminAdventuresPage();

    cy.get(':nth-child(1) > #statistics_cell > a')
      .should('be.visible')
      .should('be.not.disabled');
  })
})
