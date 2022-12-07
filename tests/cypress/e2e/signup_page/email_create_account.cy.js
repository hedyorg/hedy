import {goToLogin, gotoRegisterTeacher, goToPage, goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

    // Tests email field interaction
       cy.get('#email')
      .should('be.visible')
      .should('be.empty')
      .type('arandomemail@gmail.com')
      .should('have.value', 'arandomemail@gmail.com');
  })
})
