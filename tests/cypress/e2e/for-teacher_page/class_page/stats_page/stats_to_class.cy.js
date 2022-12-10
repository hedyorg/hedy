import {loginForAdmin, loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to go back to teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click();

    var currentUrl = '';
    cy.url().then(url => {
      currentUrl = url;
      cy.get('#stats_button').click(); // Press class statistics button

      cy.wait(500);

      cy.get('#to_class_button').click();
      cy.url().should('eq', currentUrl); // Check if you go back to the correct page
    })
  
  })
})