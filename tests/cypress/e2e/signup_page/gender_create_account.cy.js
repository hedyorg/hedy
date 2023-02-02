import {goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

    // Tests preferred language field interaction
       cy.get('#gender').select('Female').should('have.value', 'f')
      .should('be.visible')

  })
})
