import {loginForTeacher} from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";

describe('Back to class button', () => {
  it('passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    
    cy.wait(500);
    
    cy.get(".view_class").first().click(); // Press on view class button
    cy.get('#customize-class-button').click(); // Press customize class button

    cy.get('#back_to_class')
      .should('be.visible')
      .should('not.be.disabled')
      .click();
    
    // We should be in the view class page
      cy.url()
      .should('include', Cypress.config('baseUrl') + Cypress.env('class_page'));
  })

})