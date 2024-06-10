import { loginForTeacher } from '../../tools/login/login.js'

// TODO
it('Is able to click on create new class', () => {
  loginForTeacher();

  // Click 'Create class' button
  cy.getDataCy('create_class_button').click();

  // Assert that the input field is empty,
  // the ok button is visible and
  // the cancel button is visible
  cy.getDataCy('modal_prompt_input').should('be.empty');
  cy.getDataCy('modal_prompt_input').should('be.visible');
  cy.getDataCy('modal_prompt_input').should('be.enabled');

  cy.getDataCy('modal_ok_button').should('be.visible');
  cy.getDataCy('modal_ok_button').should('be.enabled');

  cy.getDataCy('modal_cancel_button').should('be.visible');
  cy.getDataCy('modal_cancel_button').should('be.enabled');
})