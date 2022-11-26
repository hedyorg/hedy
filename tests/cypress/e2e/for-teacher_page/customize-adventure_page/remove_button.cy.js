import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Preview button test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    cy.get('#modal-confirm')
      .should('not.be.visible');

    cy.get('#remove_adventure_button')
      .should('be.visible');
      .should('have.attr', 'type', 'reset')
      .click();

    cy.get('#modal-confirm')
      .should('be.visible');

    cy.get('#modal-yes-button')
      .should('be.visible');

    cy.get('#modal-no-button')
      .should('be.visible')
      .click();

    cy.wait(500);

    cy.get('#modal-confirm')
      .should('not.be.visible');
  })
})
