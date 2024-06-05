import { createClass, addCustomizations, openClassView } from '../../tools/classes/class.js';
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
    openClassView();
    cy.get('#duplicate_class').first().click();

    // Checks for input field
    cy.getDataCy('modal_prompt_input').type(duplicate_class);
    cy.getDataCy('modal_ok_button').click();

    cy.reload();
    cy.wait(500);

    openClassView();
    cy.getDataCy('view_class_link').contains(duplicate_class).click();
    cy.getDataCy('customize_class_button').click();
    cy.getDataCy('opening_date_container').should("not.be.visible")
    cy.getDataCy('opening_date_label').click();
    cy.getDataCy('opening_date_container').should("be.visible")
    cy.get("#enable_level_7").should('be.enabled');
    logout();
  })

  it('Is able to duplicate class with adding second teachers', () => {
    loginForTeacher();
    goToTeachersPage();

    openClassView();
    cy.get("tr") // This class has second teachers.
    cy.getDataCy("duplicate_CLASS1").click();

    cy.getDataCy('modal_yes_button').should('be.enabled').click();

    const duplicate_class = `test class ${Math.random()}`;
    cy.getDataCy('modal_prompt_input').type(duplicate_class);
    cy.getDataCy('modal_ok_button').click();

    cy.reload();
    cy.wait(500);

    openClassView();
    cy.getDataCy('view_class_link').contains(duplicate_class).click();
    cy.getDataCy('invites_block').should('be.visible');
    cy.getDataCy('customize_class_button').click();
    cy.getDataCy('opening_date_container').should("not.be.visible")
    cy.getDataCy('opening_date_label').click();
    cy.getDataCy('opening_date_container').should("be.visible")
    cy.get("#enable_level_7").should('be.enabled');
  })
})
