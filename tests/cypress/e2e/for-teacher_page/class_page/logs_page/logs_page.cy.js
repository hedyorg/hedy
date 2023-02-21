import {ensureClass} from '../../../tools/classes/class.js'
import { loginForTeacher } from '../../../tools/login/login.js';

describe('Tests for logs page for a class', () => {
  beforeEach(() => {
    loginForTeacher();
    ensureClass();
    cy.getBySel('view_class_link').first().click(); // Press on view class button
    cy.getBySel('logs_button');
  });
    
  it('Is able to enter an exception', () => {
    cy.getBySel('logs-exception')
      .should('be.visible')
      .should('be.empty')
      .type('ParseException')
      .should('have.value', 'ParseException');
  })

  it('Is able to enter a level to be searched', () => {
    cy.getBySel('logs-level')
      .should('be.visible')
      .should('be.empty')
      .type('1')
      .should('have.value', '1');
  })

  it('Pressing the go back to class button returns to view class page', () => {
    cy.getBySel('to_class_button').click(); // Press go back to class button
    cy.url().should('include',Cypress.config('baseUrl') + Cypress.env('class_page')); // Check if you go back to the correct page
  })

  it('Is able to press the search button and display error message', () => {
    cy.getBySel('search-logs-button').click();
    cy.getBySel('search-logs-failed-msg').should('be.visible');
  })
})