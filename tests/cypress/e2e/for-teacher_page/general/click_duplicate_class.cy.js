import { createClass, openClassView } from '../../tools/classes/class.js';
import { loginForTeacher, logout } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';


describe('Is able to click on duplicate class', () => {
  it('Passes', () => {
    loginForTeacher();
    createClass();

    // Click on duplicate icon
    openClassView();
    cy.get('#duplicate_class').first().click();

    // Checks for duplicate class name
    cy.getDataCy('modal_prompt_input').should('be.empty');
    cy.getDataCy('modal_prompt_input').should('be.visible');
    cy.getDataCy('modal_prompt_input').should('be.enabled');

    cy.getDataCy('modal_ok_button').should('be.visible');
    cy.getDataCy('modal_ok_button').should('be.enabled');

    cy.get('#modal_cancel_button').should('be.visible');
    cy.get('#modal_cancel_button').should('be.enabled');
    logout();
  })

  it("Second teacher can click on duplicate button of main teacher's class", () => {
    loginForTeacher("teacher4");
    goToTeachersPage();

    // Take actions only when teacher2 is a second teacher; i.e., having teacher1 as a teacher.
    openClassView();
    cy.get("#classes_table tbody #teacher_cell")
      .each(($username, i) => {
        if ($username.text().includes("teacher1")) {
          // Click on duplicate icon
          cy.get(`tbody :nth-child(${i+1}) #duplicate_class`).first().click();
          
          cy.wait(50)
              //Checks for Second Teachers duplication
          cy.getDataCy('modal_yes_button').should('be.visible');
          cy.getDataCy('modal_yes_button').should('be.enabled');

          cy.getDataCy('modal_no_button').should('be.visible');
          cy.getDataCy('modal_no_button').should('be.enabled').click();

          // Checks for input field
          cy.getDataCy('modal_prompt_input').should('not.have.value', '');
          cy.getDataCy('modal_prompt_input').should('be.visible');
          cy.getDataCy('modal_prompt_input').should('be.enabled');
          
          // Checks for ok button
          cy.getDataCy('modal_ok_button').should('be.visible');
          cy.getDataCy('modal_ok_button').should('be.enabled');
          
          // Checks for cancel button
          cy.get('#modal_cancel_button').should('be.visible');
          cy.get('#modal_cancel_button').should('be.enabled');
        }
      })
  })
})