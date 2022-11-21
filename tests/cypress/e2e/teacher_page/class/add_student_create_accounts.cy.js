import {loginForTeacher} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    
    createClass();
    cy.get(':nth-child(7) > [data-layer="Content"]').click();

    cy.get('.green-btn').contains("Add students").click();
    cy.get('.green-btn').contains("Create accounts").click();
    cy.get(':nth-child(2) > #username').type("student1");
    cy.get(':nth-child(2) > #password').type("password123");

    cy.get(':nth-child(3) > #username')
    .should('have.value', '')
    .then(($button) => {
      cy.get('#account_rows_container > :nth-child(3) > .fill-current').click();
      // $button is yielded
    })

    //cy.get('#account_rows_container > :nth-child(3) > .fill-current').click();
    //cy.get('#account_rows_container > :nth-child(3) > .fill-current').click();
    //cy.get('#account_rows_container > :nth-child(3) > .fill-current').click();


    cy.get('.blue-btn').contains("Create accounts").click();
    cy.get('#modal-yes-button').click();
    cy.get('form > .mt-4 > .green-btn').click();

    
  })
})