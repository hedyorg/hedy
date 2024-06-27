import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

it('Preview button test', () => {
    loginForTeacher();
    goToEditAdventure();

    cy.getDataCy('modal_content')
      .should('not.be.visible');

    // opening preview
    cy.getDataCy('preview_adventure_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

      cy.getDataCy('modal_content')
      .should('be.visible');

    cy.wait(500);

    // closing preview
    cy.getDataCy('modal_preview_button')
      .should('not.be.disabled')
      .click();

      cy.getDataCy('modal_content')
      .should('not.be.visible');

    cy.getDataCy('modal_preview_button')
      .should('not.be.visible')
})
