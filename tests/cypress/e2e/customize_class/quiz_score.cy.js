import {loginForAdmin, loginForTeacher, loginForStudent} from '../tools/login/login.js'
import { createClass } from "../tools/classes/class";

// Test is incomplete, because it only checks if it is not empty instead of the value
// This is a bug in Cypress

describe('Testing if quiz_score has specific value', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();

    // click on view class:
    cy.get(':nth-child(3) > .no-underline').click()

    // get correct url:
    var currentUrl = '';
    cy.url().then(url => {
      currentUrl = url;
      let classUrl = `[onclick="window.location.href = '/for-teachers/customize-class/` + currentUrl.substring(currentUrl.indexOf('class/')+6) + `'"]`; // get statistics class url
      cy.get(classUrl).click();
    })

    cy.get('#quiz').type("50").should("have.value", "50")

  })
})