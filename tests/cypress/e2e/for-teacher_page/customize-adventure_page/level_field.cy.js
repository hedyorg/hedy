import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Level Field test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    // Tests level field interaction
    cy.get('#custom_adventure_level')
      .should('be.visible')
      .should('not.be.disabled')
      .select('1')
      .should('have.value', '1');
  })
})
