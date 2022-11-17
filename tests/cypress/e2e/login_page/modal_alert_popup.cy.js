import {goToLogin} from '../tools/navigation/nav.js'

describe('Modal alert popup test', () => {
  it('passes', () => {
    goToLogin();

    // Tests hidden modal alert text
    cy.get('#modal_alert_text')
      .should('not.be.visible')
      .should('be.empty');

    // Tests visibility of modal alert text/ login non existing account
    cy.get('#username')
      .type('anonexistingaccount123@#$%^!')
    cy.get('#password')
      .type('anonexistingpassword123@#$%^!')
    cy.get('#login_button')
       .click()
    cy.get('#modal_alert_text')
      .should('be.visible')
  })
})
