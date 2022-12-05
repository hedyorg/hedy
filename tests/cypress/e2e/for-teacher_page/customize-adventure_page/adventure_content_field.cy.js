import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Adventure content Field test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    cy.get('#custom_adventure_content')
      .should('be.visible')
      .should('not.be.disabled')
      .clear()
      .should('have.value', '')
      .type('this is the content of this adventure \"!#@\'( )*$%\'123\"')
      .should('have.value', 'this is the content of this adventure \"!#@\'( )*$%\'123\"');
  })
})
