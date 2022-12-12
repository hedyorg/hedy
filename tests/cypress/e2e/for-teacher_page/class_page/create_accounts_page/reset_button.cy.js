import {loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to use the reset button', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button
    cy.get('#add-student').click();
    cy.get('#create-accounts').click(); 
    cy.get(':nth-child(2) > #username').type("student10");
    cy.get(':nth-child(2) > #password').type("123456");
    cy.wait(1000);
    cy.get(':nth-child(2) > #username').should('have.value', 'student10');
    cy.get('#reset_button').click();
    cy.wait(1000);
    cy.get(':nth-child(2) > #username').should('have.value', '')


    
  })
})