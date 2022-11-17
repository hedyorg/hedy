import {goToRecover} from '../tools/navigation/nav.js'

describe('Send recovery link button test', () => {
  it('passes', () => {
    goToRecover();

    // Tests send recovery link button type and visibility
    cy.get('#send_recovery_button')
      .should('be.visible')
      .should('have.attr', 'type', 'submit')
  })
})
