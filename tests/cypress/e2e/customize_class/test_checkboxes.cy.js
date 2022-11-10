import {loginForAdmin, loginForTeacher} from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";
//import { goToPage } from "../navigation/nav";

describe('Testing all checkboxes', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    
    createClass();
    cy.get(':nth-child(3) > .no-underline').click()
    cy.get('.green-btn').contains("Customize class").click()
    
    //cy.get('.adventure_level_1').uncheck()

    cy.get('[type="checkbox"]').check({force:true})
    cy.get('[type="checkbox"]').should('be.checked')
    cy.get('[type="checkbox"]').uncheck()
    cy.get('[type="checkbox"]').should('be.not.checked')

  })
})