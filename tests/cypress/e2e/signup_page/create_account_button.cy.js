import {goToLogin, gotoRegisterTeacher, goToPage, gotoRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {
    goToPage(Cypress.env('register_student_page'));

//      goToRegisterStudent();
// This function is not working yet. Preferably we use the goToRegisterStudent function instead of the goToPage function.

// This tests fills all field and tests create account button. Individual fields are tested in separated tests.

       cy.get('#username')
      .type('some_username123')

       cy.get('#email')
      .type('arandomemail@gmail.com')

       const some_password = 'some_password\"!#@\'( )*$%\'123\"'
       cy.get('#password')
      .type(some_password)

      cy.get('#password_repeat')
      .type(some_password)

      cy.get('#language').select('English')

       cy.get('#birth_year')
      .type('2000')

       cy.get('#gender').select('Female')

       cy.get('#country').select('Australia')

       cy.get('.mr-5 > .ltr\\:mr-2')
       .check()

        // After checking the 'Yes' checkbox, programming language 'Python' is checked
       cy.get(':nth-child(3) > .flex > input')
       .check()

       cy.get('#agree_terms').check()

       cy.get(':nth-child(16) > .green-btn').click()

       // Tests whether creating account is succesful [NOT WORKING YET]
       cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('landing_page'));


  })
})
