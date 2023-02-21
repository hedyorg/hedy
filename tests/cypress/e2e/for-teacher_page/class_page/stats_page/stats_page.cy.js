import {ensureClass} from '../../../tools/classes/class.js'

describe('Tests for stats page for a class', () => {
  beforeEach(() => {
    loginForTeacher();
    ensureClass();
    cy.getBySel('view_class_link').first().click(); // Press on view class button
    cy.getBySel('stats_button');
  });

  it('Is able to load data from different timelines', () => {
    // Test button visibility
    cy.getBySel('this_week_button').should('be.visible');
    cy.getBySel('two_weeks_button').should('be.visible');
    cy.getBySel('four_weeks_button').should('be.visible');
    cy.getBySel('year_button').should('be.visible');  
    
    cy.getBySel('this_week_button').click();
    cy.getBySel('two_weeks_button').click();
    cy.getBySel('four_weeks_button').click();
    cy.getBySel('year_button').click();
  })

  it('Pressing the back to class button returns to View class page', () => {
    cy.getBySel('to_class_button').click(); // Press go back to class button
    cy.url().should('include',Cypress.config('baseUrl') + Cypress.env('class_page')); // Check if you go back to the correct page
  });
})