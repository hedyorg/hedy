import {goToLogin, gotoRegisterTeacher, goToPage, gotoRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {
    goToPage(Cypress.env('register_student_page'));

//      goToRegisterStudent();
// This function is not working yet. Preferably we use the goToRegisterStudent function instead of the goToPage function.

    // Tests programming experience checkbox interaction

        // before checking the 'Yes' checkbox, programming languages should not be visible
       cy.get(':nth-child(3) > .flex > input')
       .should('not.be.visible')
       cy.get('.mr-5 > .ltr\\:mr-2')
       .should('be.visible')
       .check()
        // After checking the 'Yes' checkbox, programming languages should  be visible
       cy.get(':nth-child(3) > .flex > input')
       .should('be.visible')
       .check()

  })
})
