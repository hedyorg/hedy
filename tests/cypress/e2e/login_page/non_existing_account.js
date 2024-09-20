import { goToLogin } from '../tools/navigation/nav.js'

it('Is not able to login with a non existing account', () => {
  goToLogin();

  cy.getDataCy('username').type('anonexistingaccount123@#$%^!')
  cy.getDataCy('password').type('anonexistingpassword123@#$%^!')
  cy.gegetDataCy('login_button').click()
  cy.getDataCy('modal_alert_text').should('be.visible')
})
