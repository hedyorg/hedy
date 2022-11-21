import { loginForTeacher } from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";

describe('Testing if quiz_score has specific value', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();

    cy.get('#class_view_button').click() // Press on view class button

    cy.get('#customize-class-button').click(); // Press customize class button

    // testing quiz score feature
    cy.get('#quiz').type("50").should("have.value", "50")

  })
})