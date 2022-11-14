import { loginForTeacher} from '../tools/login/login.js'
import { createClass } from "../tools/classes/class";

describe('Testing all checkboxes', () => {
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
      cy.get(classUrl).click(); // Press class statistics button
    })
    
    // following code checks every single checkbox on the current page:
    cy.get('[type="checkbox"]').check({force:true})
    cy.get('[type="checkbox"]').should('be.checked')
    cy.get('[type="checkbox"]').uncheck()
    cy.get('[type="checkbox"]').should('be.not.checked')

  })
})