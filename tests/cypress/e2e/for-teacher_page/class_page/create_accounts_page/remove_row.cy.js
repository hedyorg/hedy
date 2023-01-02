import {loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to remove row', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button
    cy.get('#add-student').click();
    cy.get('#create-accounts').click(); 
    //fills in first row
    cy.get(':nth-child(2) > #username').type("student10");
    cy.get(':nth-child(2) > #password').type("123456");
    cy.wait(1000);
    //checks if the first row is filled
    cy.get(':nth-child(2) > #username').should('have.value', 'student10');
    //deletes the first row
    cy.get(':nth-child(2) > .fill-current > path').click();
    cy.wait(1000);
    //check if the first row is now empty
    cy.get(':nth-child(2) > #username').should('have.value', '')


    
  })
})