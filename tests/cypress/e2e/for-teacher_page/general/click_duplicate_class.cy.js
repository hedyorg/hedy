import { createClass } from '../../tools/classes/class.js';
import {loginForTeacher} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

describe('Is able to click on duplicate class', () => {
  it('Passes', () => {
    loginForTeacher();
    createClass();
    goToTeachersPage();

    // Click on duplicate icon
    cy.get('.no-underline > .fas').first().click();

    // Checks for input field
    cy.get('#modal-prompt-input').should('be.empty');
    cy.get('#modal-prompt-input').should('be.visible');
    cy.get('#modal-prompt-input').should('be.enabled');

    // Checks for ok button
    cy.get('#modal-ok-button').should('be.visible');
    cy.get('#modal-ok-button').should('be.enabled');

    // Checks for cancel button
    cy.get('#modal-cancel-button').should('be.visible');
    cy.get('#modal-cancel-button').should('be.enabled');
  })

  it("Second teacher can click on duplicate button of main teacher's class", () => {
    loginForTeacher("teacher4");
    goToTeachersPage();

    // Take actions only when teacher2 is a second teacher; i.e., having teacher1 as a teacher.
    cy.get("#teacher_classes tbody .username_cell")
      .each(($username, i) => {
        if ($username.text().includes("teacher1")) {
          // Click on duplicate icon
          cy.get(`tbody :nth-child(${i+1}) .no-underline > .fas`).first().click();
          
          cy.wait(50)
          // Checks for input field
          cy.get('#modal-prompt-input').should('not.have.value', '');
          cy.get('#modal-prompt-input').should('be.visible');
          cy.get('#modal-prompt-input').should('be.enabled');
          
          // Checks for ok button
          cy.get('#modal-ok-button').should('be.visible');
          cy.get('#modal-ok-button').should('be.enabled');
          
          // Checks for cancel button
          cy.get('#modal-cancel-button').should('be.visible');
          cy.get('#modal-cancel-button').should('be.enabled');
        }
      })
  })
})