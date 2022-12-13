import {loginForTeacher} from '../../tools/login/login.js'
import {createClass} from '../../tools/classes/class.js'


describe('Is able to go to logs page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);

    cy.get(".view_class").first().click(); // Press view class button

    cy.get('#go_back_to_teacher_page_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();   

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
  })
})