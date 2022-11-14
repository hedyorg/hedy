import {loginForAdmin, loginForTeacher} from '../tools/login/login.js'
import { createClass } from "../tools/classes/class";
//import { goToPage } from "../navigation/nav";

describe('Testing all checkboxes', () => {
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
    
    //cy.get('.adventure_level_1').uncheck()

    cy.get('[type="checkbox"]').check({force:true})
    cy.get('[type="checkbox"]').should('be.checked')
    cy.get('[type="checkbox"]').uncheck()
    cy.get('[type="checkbox"]').should('be.not.checked')

  })
})