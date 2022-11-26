import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Agree public checkbox test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    cy.get('#agree_public')
      .should('be.visible')
      .check()
      .should('be.checked')
      .uncheck()
      .should('not.be.checked');
  })
})
