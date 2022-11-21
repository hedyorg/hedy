import {loginForTeacher, loginForStudent, logout} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to see teacher page', () => {
  it('Passes', () => {

    loginForTeacher();
    
    cy.wait(500);
    
    createClass();
    cy.get(':nth-child(1) > :nth-child(3) > .no-underline').click();

    cy.get('.green-btn').contains("Add students").click();
    cy.get('.green-btn').contains("Invite by username").click();
    cy.get('#modal-prompt-input').type("student1");
    cy.get('#modal-ok-button').click();
 
    //logout:
    cy.get('.dropdown > .menubar-text').click();
    cy.get(':nth-child(6) > .dropdown-item').click();

    cy.wait(500);
    loginForStudent();
    cy.wait(500);
    cy.get('.dropdown > .menubar-text > .fas').click();
    cy.get(':nth-child(3) > .dropdown-item').click();
    cy.contains("My messages").click();
    cy.get('#messages > :nth-child(2) > .flex > .green-btn').click();
    cy.get('.green-btn').contains("Join class").click();


  })
})