import {loginForAdmin, loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to load data from different timelines', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get('#class_view_button').click();
    cy.get('#stats_button').click();

    // Test button visibility
    cy.get('#this_week_button').should('be.visible');
    cy.get('#two_weeks_button').should('be.visible');
    cy.get('#four_weeks_button').should('be.visible');
    cy.get('#year_button').should('be.visible');  
    
    cy.get('#this_week_button').click();
    cy.get('#two_weeks_button').click();
    cy.get('#four_weeks_button').click();
    cy.get('#year_button').click();
  })
})