import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Name Field test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    // Tests name field interaction
    cy.get('#custom_adventure_name')
      .should('be.visible')
      .should('not.be.disabled')
      .clear()
      .should('be.empty')
      .type('some_name\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_name\"!#@\'( )*$%\'123\"');
  })
})
