import {goToLogin, gotoRegisterTeacher, goToPage, goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

    // Tests preferred language field interaction
       cy.get('#language').select('English').should('have.value', 'en')
      .should('be.visible')

  })
})
