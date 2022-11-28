import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Save button test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    // should all not be visible at start
    cy.get('#modal-confirm')
      .should('not.be.visible');
    cy.get('#modal_alert_container')
      .should('not.be.visible');
    cy.get('#modal_alert_text')
      .should('not.be.visible');
    cy.get('#modal-no-button')
      .should('not.be.visible');
    cy.get('#modal-yes-button')
      .should('not.be.visible');

    // Not saving (clicking in save and than on 'yes')
    cy.get('#save_adventure_button')
      .should('be.visible')
      .should('not.be.disabled')
      .should('have.attr', 'type', 'submit')
      .click();

    cy.get('#modal-confirm')
      .should('be.visible');

    cy.get('#modal-yes-button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

    cy.get('#modal_alert_container')
      .should('be.visible');
    cy.get('#modal_alert_text')
      .should('be.visible');

    cy.wait(500);

    cy.get('#modal-confirm')
      .should('not.be.visible');
    cy.get('#modal_alert_container')
      .should('not.be.visible');
    cy.get('#modal_alert_text')
      .should('not.be.visible');
    cy.get('#modal-yes-button')
      .should('not.be.visible')

    // Not saving (clicking in save and than on 'no')
    cy.get('#save_adventure_button')
      .click();

    cy.get('#modal-no-button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

    cy.get('#modal_alert_container')
      .should('not.be.visible');
    cy.get('#modal_alert_text')
      .should('not.be.visible');
    cy.get('#modal-no-button')
      .should('not.be.visible');
  })
})
