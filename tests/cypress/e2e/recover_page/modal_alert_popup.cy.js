import {goToRecover} from '../tools/navigation/nav.js'

describe('Modal alert popup test', () => {
  it('passes', () => {
    goToRecover();

    // Tests hidden modal alert text
    cy.get('#modal_alert_text')
      .should('not.be.visible')
      .should('be.empty');

    // Tests visibility of error modal alert text/ recover non existing account
    cy.get('#username')
      .type('anonexistingaccount123@#$%^!')
    cy.get('#send_recovery_button')
       .should('be.visible')
       .should('not.be.disabled')
       .click()
    cy.get('#modal_alert_text')
      .should('be.visible')

    // Reset fields
    cy.get('#username')
      .clear();

    // Tests visibility of succes modal alert text/ recover existing account
    cy.get('#username')
      .type('user1')
    cy.get('#send_recovery_button')
       .click()
    cy.get('#modal_alert_text')
      .should('be.visible')
  })
})
