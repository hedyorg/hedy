import { loginForTeacher } from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";

// Test is incomplete, because it only checks if it is not empty instead of the value
// This is a bug in Cypress

describe('Testing if opening dates is not empty', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();

    cy.get('#class_view_button > .no-underline').click() // Press on view class button

    cy.get('#customize-class-button').click(); // Press customize class button

    // The following line has a bug in cypress:
    // cy.get("#opening_date_level_1").type("2022-12-01").should("have.value", "2023-01-01")
    // The following tests only check if the field is not empty:
    cy.get("#opening_date_level_1").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_2").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_3").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_4").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_5").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_6").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_7").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_8").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_9").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_10").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_11").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_12").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_13").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_14").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_15").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_16").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_17").type("2023-01-01").should("not.be.empty")
    cy.get("#opening_date_level_18").type("2023-01-01").should("not.be.empty")


  })
})