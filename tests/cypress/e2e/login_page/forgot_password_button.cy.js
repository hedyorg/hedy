import {goToLogin} from '../tools/navigation/nav.js'

it('Is able to click on forgot password', () => {
  goToLogin();
  cy.getDataCy('forgot_password_button').click();

  cy.location().should((loc) => {
    expect(loc.pathname).equal("/recover");
  })
})
