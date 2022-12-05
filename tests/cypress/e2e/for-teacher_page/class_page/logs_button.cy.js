import {loginForTeacher} from '../../tools/login/login.js'
import {createClass} from '../../tools/classes/class.js'


describe('Is able to go to logs page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get("#class_view_button > .no-underline").click(); // Press view class button

    var currentUrl = '';
    cy.url().then(url => {
      currentUrl = url;
      cy.get('#logs_button').click(); // Press logs button

      let statsUrl = Cypress.env('logs_page') + currentUrl.substring(currentUrl.indexOf('class/')+6);
      cy.url().should('include', statsUrl); // Check if you are in the logs page
    })    
  })
})