import {goToRecover} from '../tools/navigation/nav.js'

describe('Password field test', () => {
  it('passes', () => {
    goToRecover();

    // Tests password field interaction
    cy.get('#username')
      .should('be.visible')
      .should('not.be.disabled')
      .should('be.empty')
      .type('some_username\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_username\"!#@\'( )*$%\'123\"');
  })
})
