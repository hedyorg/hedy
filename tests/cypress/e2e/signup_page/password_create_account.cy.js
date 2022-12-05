import {goToLogin, gotoRegisterTeacher, goToPage, goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

    // Tests password field interaction
       const some_password = 'some_password\"!#@\'( )*$%\'123\"'
       cy.get('#password')
      .should('be.visible')
      .should('be.empty')
      .should('have.attr', 'type', 'password')
      .type(some_password)
      .should('have.value', some_password);

    // Tests password repeat field interaction

      cy.get('#password_repeat')
      .should('be.visible')
      .should('be.empty')
      .should('have.attr', 'type', 'password')
      .type(some_password)
      .should('have.value', some_password);


  })
})
