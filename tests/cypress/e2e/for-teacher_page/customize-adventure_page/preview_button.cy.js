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
      .click();

    cy.get('#modal-content')
      .should('be.visible');

    cy.wait(500);

    // closing preview
    cy.get('#modal-preview-button')
      .click();

    cy.get('#modal-content')
      .should('not.be.visible');
  })
})
