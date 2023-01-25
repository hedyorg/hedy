import {loginForTeacher} from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";

// Test both of these buttons together since their functionalites are intertwined
describe('Save and remove customizations buttons', () => {
  it('passes', () => {
  loginForTeacher();
  cy.wait(500);
  createClass();
  
  cy.wait(500);
  
  cy.get(".view_class").first().click(); // Press on view class button
  cy.get('#customize-class-button').click(); // Press customize class button

  // Since this class is new it shouldn't have customizations
  cy.get('#remove_customizations_button')
    .should('not.be.visible');
  
  //  We save the customizations first
  cy.get("#save_customizations")
    .should('be.visible')
    .should('not.be.disabled')
    .click();


  cy.get('#modal_alert_text')
    .should('be.visible');

  // Now that it has customizations we can remove them
  cy.get('#remove_customizations_button')
    .should('be.visible')
    .should('not.be.disabled')
    .click();

  cy.get('#modal-yes-button')
    .should('be.visible')
    .click();

  // It shouldn't have the button again
  cy.get('#remove_customizations_button')
    .should('not.be.visible');
  })
})