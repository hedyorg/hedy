import {loginForAdmin, loginForTeacher} from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";
//import { goToPage } from "../navigation/nav";

// Test is incomplete, because it only checks if it is not empty instead of the value
// This is a bug in Cypress

describe('Testing if opening dates is not empty', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    
    createClass();
    cy.get(':nth-child(3) > .no-underline').click()
    cy.get('.green-btn').contains("Customize class").click()

    //cy.get('#opening_date_level_1 > .ltr\:pl-2 > .opening_date_input').click()
    cy.get("#opening_date_level_1").type("2022-12-01").should("not.be.empty")

  })
})