import {goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Username field test', () => {
  it('passes', () => {

    goToRegisterStudent();

    // Tests username field interaction
       cy.get('.btn')
      .should('be.visible')
      .click()

    cy.url().should('eq', Cypress.config('baseUrl') + Cypress.env('login_page'));
  })
})
