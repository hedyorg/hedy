import {loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to go to logs page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button

    var currentUrl = '';
    cy.url().then(url => {
      currentUrl = url;
      cy.get('#add-student').click();
      cy.get('#create-accounts').click(); 
      cy.get('#back_to_class_button').click();
      cy.wait(1000);
      let statsUrl = Cypress.env('class_page') + currentUrl.substring(currentUrl.indexOf('class/')+6);
      cy.url().should('include', statsUrl); 
    })    
  })
})