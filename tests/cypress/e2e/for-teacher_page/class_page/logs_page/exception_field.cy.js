import {loginForAdmin, loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to enter an exception', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button from test class

    cy.get('#logs_button').click();
    
    cy.get('#logs-exception')
      .should('be.visible')
      .should('be.empty')
      .type('ParseException')
      .should('have.value', 'ParseException');
  })
})