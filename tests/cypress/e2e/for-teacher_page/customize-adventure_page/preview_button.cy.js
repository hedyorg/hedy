import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Preview button test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    cy.get('#modal-content')
      .should('not.be.visible');

    // opening preview
    cy.get('#preview_adventure_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

    cy.get('#modal-content')
      .should('be.visible');

    cy.wait(500);

    // closing preview
    cy.get('#modal-preview-button')
      .should('not.be.disabled')
      .click();

    cy.get('#modal-content')
      .should('not.be.visible');

    cy.get('#modal-preview-button')
      .should('not.be.visible')
  })
})
