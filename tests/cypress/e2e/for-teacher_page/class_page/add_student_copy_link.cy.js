import {loginForTeacher, logout} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to see copy link to add student to class', () => {
  it('Passes', () => {
    
    loginForTeacher();
    cy.wait(500);
    
    cy.get(".view_class").then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get("#view_classes").click();
      }
    });
    cy.get(".view_class").first().click();
    cy.get('body').then($b => $b.find("#survey")).then($s => $s.length && $s.hide())
    cy.get('#add-student').click();
    cy.get('#copy-join-link').should('be.visible').should('be.enabled').click();

  })
})
