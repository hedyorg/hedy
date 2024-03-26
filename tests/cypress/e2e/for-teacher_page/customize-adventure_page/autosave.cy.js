import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('auto save', () => {
  it('should work when changing the name field.', () => {
    cy.intercept({
      method: "POST",
      url: "/for-teachers/customize-adventure",
    }).as("customizeAdventure")

    loginForTeacher("teacher1");
    goToEditAdventure();

    // the rest of the fields work similar to this.
    cy.get('#custom_adventure_name')
      .clear()
      .type('changed')

    // there's a debouncing of 1000 second before we issue an update.
    cy.wait(1000)
    cy.wait("@customizeAdventure").should('have.nested.property', 'response.statusCode', 200)

    cy.get('#modal_alert_container')
      .should('be.visible');
    cy.get('#modal_alert_text')
      .should('be.visible')
    
    // update it to its expected name
    cy.get('#custom_adventure_name')
      .clear()
      .type('adventure1')
    cy.wait(1000)
    cy.wait('@customizeAdventure').should('have.nested.property', 'response.statusCode', 200);
  })
})
