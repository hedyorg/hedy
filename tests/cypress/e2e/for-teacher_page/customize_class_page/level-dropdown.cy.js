import {loginForTeacher} from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";

describe('Back to class button', () => {
  it('passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();

    cy.wait(500);

    cy.get(".view_class").first().click(); // Press on view class button
    cy.get('#customize-class-button').click(); // Press customize class button

    // Click on level 1
    cy.get("#adventures")
      .select('1')
      .should('have.value', '1');    
    
    // level 1 should be visible and level 2 not
    cy.get("#level-1")
      .should('be.visible');
    
    cy.get("#level-2")
      .should('not.be.visible');
    
    // after selecting level 2 it should be visible and level 1 not
    cy.get("#adventures")
      .select('2')
      .should('have.value', '2');

    cy.get("#level-1")
      .should('not.be.visible');
    
    cy.get("#level-2")
      .should('be.visible');
        
  })
})