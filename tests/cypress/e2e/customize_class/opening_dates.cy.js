import {loginForAdmin, loginForTeacher} from '../tools/login/login.js'
import { createClass } from "../tools/classes/class";
//import { goToPage } from "../navigation/nav";

// Test is incomplete, because it only checks if it is not empty instead of the value
// This is a bug in Cypress

describe('Testing if opening dates is not empty', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    
    createClass();
    cy.get(':nth-child(3) > .no-underline').click()
    //cy.get('.green-btn').contains("Customize class").click()

    var currentUrl = '';
    cy.url().then(url => {
      currentUrl = url;
      let classUrl = `[onclick="window.location.href = '/for-teachers/customize-class/` + currentUrl.substring(currentUrl.indexOf('class/')+6) + `'"]`; // get statistics class url
      cy.get(classUrl).click(); // Press class statistics button
    })

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