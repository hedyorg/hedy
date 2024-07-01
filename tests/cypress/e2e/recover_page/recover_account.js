import {goToRecover} from '../tools/navigation/nav.js'

it('Is not able to recover non existing account, then test existing account', () => {
  goToRecover();

  // Tests visibility of error modal alert text/ recover non existing account
  cy.getDataCy('username')
    .type('anonexistingaccount123@#$%^!')
  cy.getDataCy('send_recovery_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click()
  cy.getDataCy('modal_alert_text')
    .should('be.visible')

  // Reset fields
  cy.getDataCy('username')
    .clear();

  // Tests visibility of succes modal alert text/ recover existing account
  cy.getDataCy('username')
    .type('user1')
  cy.getDataCy('send_recovery_button')
      .click()
  cy.getDataCy('modal_alert_text')
    .should('be.visible')
})
