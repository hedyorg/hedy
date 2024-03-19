import {loginForTeacher} from '../../tools/login/login.js'

describe('Is able to click on create new class', () => {
  it('Passes', () => {
    loginForTeacher();

    // Click 'Create class' button
    cy.get('#create_class_button').click();

    // Assert that the input field is empty,
    // the ok button is visible and
    // the cancel button is visible
    cy.get('#modal-prompt-input').should('be.empty');
    cy.get('#modal-prompt-input').should('be.visible');
    cy.get('#modal-prompt-input').should('be.enabled');

    cy.get('#modal-ok-button').should('be.visible');
    cy.get('#modal-ok-button').should('be.enabled');

    cy.get('#modal-cancel-button').should('be.visible');
    cy.get('#modal-cancel-button').should('be.enabled');
  })
})