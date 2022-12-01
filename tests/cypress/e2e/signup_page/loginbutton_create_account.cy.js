import {goToLogin, gotoRegisterTeacher, goToPage, gotoRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {
    goToPage(Cypress.env('register_student_page'));

//      goToRegisterStudent();
// This function is not working yet. Preferably we use the goToRegisterStudent function instead of the goToPage function.

    // Tests username field interaction
       cy.get('#username')
      .should('be.visible')
      .should('be.empty')
      .type('some_username123')
      .should('have.value', 'some_username123');
  })
})
