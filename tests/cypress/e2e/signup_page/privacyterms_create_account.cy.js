import {goToLogin, gotoRegisterTeacher, goToPage, goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

    // Tests username field interaction
       cy.get('#agree_terms').check()
      .should('be.visible')
  })
})
