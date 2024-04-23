import { createClass } from '../../tools/classes/class.js';
import {loginForTeacher, logout} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';


describe('Is able to click on duplicate class', () => {
  it('Passes', () => {
    loginForTeacher();
    createClass();

    // Click on duplicate icon
    cy.get(".view_class").then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get("#view_classes").click();
      }
    });
    cy.get('#duplicate_class').first().click();

    // Checks for duplicate class name
    cy.get('#modal-prompt-input').should('be.empty');
    cy.get('#modal-prompt-input').should('be.visible');
    cy.get('#modal-prompt-input').should('be.enabled');

    cy.get('#modal-ok-button').should('be.visible');
    cy.get('#modal-ok-button').should('be.enabled');

    cy.get('#modal-cancel-button').should('be.visible');
    cy.get('#modal-cancel-button').should('be.enabled');
    logout();
  })

  it("Second teacher can click on duplicate button of main teacher's class", () => {
    loginForTeacher("teacher4");
    goToTeachersPage();

    // Take actions only when teacher2 is a second teacher; i.e., having teacher1 as a teacher.
    cy.get(".view_class").then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get("#view_classes").click();
      }
    });
    cy.get("#classes_table tbody #teacher_cell")
      .each(($username, i) => {
        if ($username.text().includes("teacher1")) {
          // Click on duplicate icon
          cy.get(`tbody :nth-child(${i+1}) #duplicate_class`).first().click();
          
          cy.wait(50)
              //Checks for Second Teachers duplication
          cy.get('[data-cy="modal_yes_button"]').should('be.visible');
          cy.get('[data-cy="modal_yes_button"]').should('be.enabled');

          cy.get('#modal-no-button').should('be.visible');
          cy.get('#modal-no-button').should('be.enabled').click();

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