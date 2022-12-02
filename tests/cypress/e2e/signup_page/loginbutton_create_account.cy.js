import {goToLogin, gotoRegisterTeacher, goToPage, goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {
    goToPage(Cypress.env('register_student_page'));

    goToRegisterStudent();

    // Tests username field interaction
       cy.get('.btn')
      .should('be.visible')
      .click()

    cy.url().should('eq', Cypress.config('baseUrl') + Cypress.env('login_page'));
  })
})
