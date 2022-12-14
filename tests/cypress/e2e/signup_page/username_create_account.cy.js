import {goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

    // Tests username field interaction
       cy.get('#username')
      .should('be.visible')
      .should('be.empty')
      .type('some_username123')
      .should('have.value', 'some_username123');
  })
})
