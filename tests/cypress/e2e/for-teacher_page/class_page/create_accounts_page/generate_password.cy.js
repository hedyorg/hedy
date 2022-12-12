import {loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to generate passwords', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button
    cy.get('#add-student').click();
    cy.get('#create-accounts').click(); 
    cy.get('#toggle_circle').click(); //switches the toggle on so that passwords are generated
    cy.wait(1000);
    cy.get(':nth-child(2) > #password').should('have.length.greaterThan', 0)


    
  })
})