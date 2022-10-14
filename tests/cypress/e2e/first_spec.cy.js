import {loginForAdmin, loginForTeacher} from './tools/login/login.js'

describe('Is able to see classes', () => {
  it('passes', () => {
    loginForTeacher();
    // cy.visit(Cypress.env('base_url'))
  })
})