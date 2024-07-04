import { loginForAdmin } from '../../tools/login/login.js'
import { goToAdminAdventuresPage } from '../../tools/navigation/nav.js';

it('adventure button should be visible', () => {
  loginForAdmin();
  goToAdminAdventuresPage();

  cy.get(':nth-child(1) > [data-cy="statistics_cell"] > a')
    .should('be.visible')
    .should('be.not.disabled');
})