import { loginForTeacher } from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";

describe('Testing all checkboxes', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();

    cy.get('#class_view_button').click() // Press on view class button

    cy.get('#customize-class-button').click(); // Press customize class button
    
    // following code checks every single checkbox on the current page:
    cy.get('[type="checkbox"]').check({force:true})
    cy.get('[type="checkbox"]').should('be.checked')
    cy.get('[type="checkbox"]').uncheck()
    cy.get('[type="checkbox"]').should('be.not.checked')

  })
})