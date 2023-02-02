import {goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

    // Tests preferred language field interaction
       cy.get('#country').select('Australia').should('have.value', 'AU')
      .should('be.visible')

  })
})
