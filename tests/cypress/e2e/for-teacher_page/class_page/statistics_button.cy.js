import {loginForTeacher} from '../../tools/login/login.js'
import {createClass} from '../../tools/classes/class.js'


describe('Is able to go to class statistics page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button

    var currentUrl = '';
    cy.url().then(url => {
      currentUrl = url;
      cy.get('#stats_button').click(); // Press class statistics button

      let statsUrl = Cypress.env('stats_page') + currentUrl.substring(currentUrl.indexOf('class/')+6);
      cy.url().should('include', statsUrl); // Check if you are in the statistics page
    })    
  })
})