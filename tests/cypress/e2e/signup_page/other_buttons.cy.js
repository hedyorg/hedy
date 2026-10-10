import { goToSignup } from '../tools/navigation/nav.js'

beforeEach(() => {
  goToSignup();
})

describe('Test other buttons sign up page', () => {
  it('As a student', () => {
    cy.getDataCy('signup_student').click()
    cy.getDataCy('privacy').click()
    cy.url().should('contain', Cypress.config('baseUrl') + Cypress.expose('privacy_page'));

    goToSignup();
    cy.getDataCy('signup_student').click()
    cy.getDataCy('login_button').click()
    cy.url().should('contain', Cypress.config('baseUrl') + Cypress.expose('login_page'));
  })

  it('As a teacher', () => {
    cy.getDataCy('signup_teacher').click()
    cy.getDataCy('privacy').click()
    cy.url().should('contain', Cypress.config('baseUrl') + Cypress.expose('privacy_page'));

    goToSignup();
    cy.getDataCy('signup_teacher').click()
    cy.getDataCy('login_button').click()
    cy.url().should('contain', Cypress.config('baseUrl') + Cypress.expose('login_page'));
  })
})
