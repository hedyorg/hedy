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
    cy.get('button[class*="green-btn mt-2"]')
       .click()
    cy.get('#modal_alert_text')
      .should('be.visible')
      .contains('Your username is invalid.');

    // Reset fields
    cy.get('#username')
      .clear();

    // Tests visibility of succes modal alert text/ recover existing account
    cy.get('#username')
      .type('user1')
    cy.get('button[class*="green-btn mt-2"]')
       .click()
    cy.get('#modal_alert_text')
      .should('be.visible')
      .contains('You should soon receive an email with instructions on how to reset your password.');
  })
})
