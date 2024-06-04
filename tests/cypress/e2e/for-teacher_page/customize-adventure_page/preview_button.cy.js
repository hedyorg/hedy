import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Preview button test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    cy.get('#modal_content')
      .should('not.be.visible');

    // opening preview
    cy.get('#preview_adventure_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

    cy.get('#modal_content')
      .should('be.visible');

    cy.wait(500);

    // closing preview
    cy.get('#modal_preview_button')
      .should('not.be.disabled')
      .click();

    cy.get('#modal_content')
      .should('not.be.visible');

    cy.get('#modal_preview_button')
      .should('not.be.visible')
  })
})
