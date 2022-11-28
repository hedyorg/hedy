import {goToLogin, gotoRegisterTeacher, goToPage, gotoRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {
    goToPage(Cypress.env('register_student_page'));

//      goToRegisterStudent();
// This function is not working yet. Preferably we use the goToRegisterStudent function instead of the goToPage function.

// This tests fills all field and tests create account button. Individual fields are tested in separated tests.

const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

function generateString(length) {
    let result = ' ';
    const charactersLength = characters.length;
    for ( let i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }

    return result;
}

const username = generateString(12)
const email = username + '@gmail.com'

       cy.get('#username')
      .type(username)

       cy.get('#email')
      .type(email)

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

       cy.get('#prog_experience_yes').check()

        // After checking the 'Yes' checkbox, programming language 'Python' is checked
       cy.get('#experience_language_python').check()

       cy.get('#agree_terms').check()

       cy.get('#submit_button').click()

       // Tests whether creating account is succesful [NOT WORKING YET]
       cy.url().should('contain', Cypress.config('baseUrl') + Cypress.env('landing_page'));


})

})
