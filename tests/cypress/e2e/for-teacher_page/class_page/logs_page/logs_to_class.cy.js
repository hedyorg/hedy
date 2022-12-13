import {loginForAdmin, loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to go back to teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click();

    var currentUrl = '';
    cy.url().then(currentUrl => {
      cy.get('#logs_button').click(); // Press the logs button

      cy.wait(500);

      cy.get('#to_class_button').click(); // Press go back to class button
      cy.url().should('eq', currentUrl); // Check if you go back to the correct page
    })
  
  })
})