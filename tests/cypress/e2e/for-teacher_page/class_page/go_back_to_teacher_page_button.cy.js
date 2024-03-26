import {loginForTeacher} from '../../tools/login/login.js'
import {createClass} from '../../tools/classes/class.js'


describe('Is able to go to logs page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);

    cy.get(".view_class").then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get("#view_classes").click();
      }
    });
    cy.get(".view_class").first().click(); // Press view class button
    cy.get('body').then($b => $b.find("#survey")).then($s => $s.length && $s.hide())

    cy.get('#go_back_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();   

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
  })
})