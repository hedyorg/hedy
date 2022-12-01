import {goToLogin} from '../tools/navigation/nav.js'

describe('Password field test', () => {
  it('passes', () => {
    goToLogin();

    // Tests password field interaction
    cy.get('#password')
      .should('be.visible')
      .should('not.be.disabled')
      .should('be.empty')
      .should('have.attr', 'type', 'password')
      .type('some_password\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_password\"!#@\'( )*$%\'123\"');
  })
})
