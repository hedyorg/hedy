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

    cy.get('#sortadventures')
      .children()
      .should('not.be.visible');


    // Click on level 2
    cy.get("#adventures")
      .select('2')
      .should('have.value', '2');

    cy.wait(500);
    
    // The available adventures dropdown should only include the default option
    cy.get("#available")
      .children()
      .should('have.length', 1)
    
    // store the name of the adventure we're going to delete
    cy.get('#level-2 div:first')
      .invoke('attr', 'adventure')
      .as('adventure');
    
    cy.get("@adventure").then(adventure => {
      
      // Get the first adventure, and click its remove button
      cy.get("#level-2 div:first span")
        .click();
      // The available adventures dropdown should now include the new adventure
      cy.get("#available")
        .children()
        .should('have.length', 2);
      
      // the added option should be the last
      cy.get("#available option:last")
        .should('have.id', `remove-${adventure}`);

      // after selecting the adventure, it shouldn't be among the options
      cy.get("#available")
        .select(1)
        .children()
        .should('have.length', 1);
      
      // the adventure should now be last
      cy.get("#level-2 div:last")
        .should('have.attr', 'adventure')
        .and('eq', adventure);
    })
  })
})