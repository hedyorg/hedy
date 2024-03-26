import {loginForTeacher} from '../../tools/login/login.js'
import {createClass} from '../../tools/classes/class.js'


describe('Is able to go to logs page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);

    cy.get(".view_class").then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get("#view_classes").click();
      }
    });
    cy.get(".view_class").first().click(); // Press view class button

    var currentUrl = '';
    cy.url().then(url => {
      currentUrl = url;
      cy.get('body').then($b => $b.find("#survey")).then($s => $s.length && $s.hide())
      cy.get('#customize-class-button').click(); // Press logs button

      let statsUrl = Cypress.env('customize_class_page') + currentUrl.substring(currentUrl.indexOf('class/')+6);
      cy.url().should('include', statsUrl); // Check if you are in the logs page
    })    
  })
})