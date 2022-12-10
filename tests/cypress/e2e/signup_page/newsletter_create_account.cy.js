import {goToRegisterTeacher} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Subscribe to newsletter test', () => {
  it('passes', () => {

    goToRegisterTeacher();

    // Tests username field interaction
       cy.get('#subscribe').check()
      .should('be.visible')
  })
})
