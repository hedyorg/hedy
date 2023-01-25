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


    // Click on level 1
    cy.get("#adventures")
      .select('1')
      .should('have.value', '1');

    // Now it should be visible
    cy.get('#level-1').should('be.visible');

    cy.wait(500)

    // Get the first and second adventure
    cy.get('#level-1')
      .children()
      .eq(0)
      .invoke('attr', 'adventure')
      .as('first_adventure');

    cy.get('#level-1')
      .children()
      .eq(1)
      .invoke('attr', 'adventure')
      .as('second_adventure');
    
    // Getting their values first, and then moving them around
    cy.get('@first_adventure').then(first_adventure => {
      cy.get('@second_adventure').then(second_adventure => {
       
        // Move the second adventure to the first place
        cy.get('#level-1')
          .children()
          .eq(1)
          .trigger('dragstart')
          .siblings()
          .should('have.attr', 'class')
          .and('contain', 'drop-adventures-hint');
  
        cy.get('#level-1')
          .children()
          .eq(0)      
          .trigger('drop')
          .trigger('dragend');
        
        // they should be inverted now
        cy.get('#level-1')
        .children()
        .eq(0)
        .should('have.attr', 'adventure')
        .and('eq', second_adventure);
        
        cy.get('#level-1')
          .children()
          .eq(1)
          .should('have.attr', 'adventure')
          .and('eq', first_adventure);
      })
    })
  })
})