import {goToRecover} from '../tools/navigation/nav.js'

describe('Send recovery link button test', () => {
  it('passes', () => {
    goToRecover();

    // Tests send recovery link button type and visibility
    cy.get('button[class*="green-btn mt-2"]')
      .should('be.visible')
      .should('have.attr', 'type', 'submit')
      .contains('Send me a password recovery link');
  })
})
