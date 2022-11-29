import {goToLogin} from '../tools/navigation/nav.js'

describe('Username field test', () => {
  it('passes', () => {
    goToLogin();

    // Tests username field interaction
    cy.get('#username')
      .should('be.visible')
      .should('not.be.disabled')
      .should('be.empty')
      .type('some_username\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_username\"!#@\'( )*$%\'123\"');
  })
})
