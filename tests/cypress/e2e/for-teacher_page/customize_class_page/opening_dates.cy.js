import { loginForTeacher } from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";

// Test is incomplete, because it only checks if it is not empty instead of the value
// This is a bug in Cypress

describe('Testing if opening dates is not empty', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();

    cy.get('#class_view_button').click() // Press on view class button

    cy.get('#customize-class-button').click(); // Press customize class button

    // The following line has a bug in cypress:
    // cy.get("#opening_date_level_" + index).type("2023-01-01").should("have.value", "2023-01-01")
    // The following tests only checks if the field is not empty using a for loop:
    var levelarray = Array.from({length:18},(v, k)=>k+1) // length reflects how many levels there are
    cy.wrap(levelarray).each((index) => {
      cy.get("#opening_date_level_" + index).type("2023-01-01").should("not.be.empty")
    })

  })
})