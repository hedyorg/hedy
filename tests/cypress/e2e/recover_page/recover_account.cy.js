import { goToRecover } from '../tools/navigation/nav.js'

beforeEach(() => {
  goToRecover();
})

describe('Recover account', () => {
  it('Is not able to recover non existing account', () => {
    cy.getDataCy('username').type('anonexistingaccount123@#$%^!')
    cy.getDataCy('send_recovery_button').click()
    cy.getDataCy('modal_alert_text').should('be.visible')
  })

  it('Is able to recover existing account', () => {
    cy.getDataCy('username').type('user1')
    cy.getDataCy('send_recovery_button').click()
    cy.getDataCy('modal_alert_text').should('be.visible')
  })
})