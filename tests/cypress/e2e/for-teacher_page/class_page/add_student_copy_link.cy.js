import {loginForTeacher, logout} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to see teacher page', () => {
  it('Passes', () => {
    
    loginForTeacher();
    cy.wait(500);
    

    cy.get(".view_class").first().click();
    cy.get('#add-student').click();
    cy.get('#copy-join-link').click();
    cy.wait(5000);
    cy.window().its('navigator.clipboard').invoke('readText').then(cy.visit);
    cy.wait(500);
    cy.url().should('include', '/prejoin/');

  })
})
