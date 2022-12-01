import {goToLogin, gotoRegisterTeacher, goToPage, gotoRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {
    goToPage(Cypress.env('register_student_page'));

//      goToRegisterStudent();
// This function is not working yet. Preferably we use the goToRegisterStudent function instead of the goToPage function.

    // Tests preferred language field interaction
       cy.get('#country').select('Australia').should('have.value', 'AU')
      .should('be.visible')

  })
})
