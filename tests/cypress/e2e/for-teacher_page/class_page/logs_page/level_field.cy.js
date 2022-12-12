import {loginForAdmin, loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to enter a level to be searched', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button from test class

    cy.get('#logs_button').click();
    
    cy.get('#logs-level')
      .should('be.visible')
      .should('be.empty')
      .type('1')
      .should('have.value', '1');
  })
})