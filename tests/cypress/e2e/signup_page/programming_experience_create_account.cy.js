import {goToLogin, gotoRegisterTeacher, goToPage, gotoRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {
    goToPage(Cypress.env('register_student_page'));

//      goToRegisterStudent();
// This function is not working yet. Preferably we use the goToRegisterStudent function instead of the goToPage function.

    // Tests programming experience checkbox interaction

        // Checks the 'no' button
        cy.get('#prog_experience_no')
        .should('be.visible')
        .check()

        // before checking the 'Yes' checkbox, programming languages should not be visible
       cy.get('#experience_language_python')
       .should('not.be.visible')
       cy.get('#prog_experience_yes')
       .should('be.visible')
       .check()
        // After checking the 'Yes' checkbox, programming languages should  be visible
       cy.get('#experience_language_python')
       .should('be.visible')
       .check()

  })
})
