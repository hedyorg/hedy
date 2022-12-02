import {goToLogin, gotoRegisterTeacher, goToPage, goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

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
