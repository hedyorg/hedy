import { createClass, addCustomizations } from '../../tools/classes/class.js';
import { loginForTeacher, logout} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

describe('Duplicate class tests', () => {
  it('Is able to duplicate class without adding second teachers', () => {
    loginForTeacher();
    const classname = createClass();
    addCustomizations(classname);
    goToTeachersPage();
    const duplicate_class = `test class ${Math.random()}`;

    // Click on duplicate icon
    cy.reload();
    cy.wait(500);
    cy.getBySel('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getBySel('view_classes').click();
      }
    });
    cy.get('#duplicate_class').first().click();

    // Checks for input field
    cy.getBySel('modal_prompt_input').type(duplicate_class);
    cy.getBySel('modal_ok_button').click();

    cy.reload();
    cy.wait(500);

    cy.getBySel('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getBySel('view_classes').click();
      }
    });
    cy.getBySel('view_class_link').contains(duplicate_class).click();
    cy.getBySel('customize_class_button').click();
    cy.get("#opening_date_container").should("not.be.visible")
    cy.get("#opening_date_label").click();
    cy.get("#opening_date_container").should("be.visible")
    cy.get("#enable_level_7").should('be.enabled');
    logout();
  })

  it('Is able to duplicate class with adding second teachers', () => {
    loginForTeacher();
    goToTeachersPage();

    cy.getBySel('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getBySel('view_classes').click();
      }
    });
    cy.get("tr") // This class has second teachers.
    cy.get("[data-cy='duplicate_CLASS1']").click();

    cy.getBySel('modal_yes_button').should('be.enabled').click();

    const duplicate_class = `test class ${Math.random()}`;
    cy.getBySel('modal_prompt_input').type(duplicate_class);
    cy.getBySel('modal_ok_button').click();

    cy.reload();
    cy.wait(500);

    cy.getBySel('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getBySel('view_classes').click();
      }
    });
    cy.getBySel('view_class_link').contains(duplicate_class).click();
    cy.getBySel('invites_block').should('be.visible');
    cy.getBySel('customize_class_button').click();
    cy.get("#opening_date_container").should("not.be.visible")
    cy.get("#opening_date_label").click();
    cy.get("#opening_date_container").should("be.visible")
    cy.get("#enable_level_7").should('be.enabled');
  })
})
