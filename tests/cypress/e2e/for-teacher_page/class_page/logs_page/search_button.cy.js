import {loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to press the search button', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click();
    cy.get('#logs_button').click();

    cy.get('#search-logs-button').click();
    cy.get('#search-logs-failed-msg').should('be.visible');
  })
})