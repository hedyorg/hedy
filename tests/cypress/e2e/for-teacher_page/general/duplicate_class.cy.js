import { createClass, addCustomizations, openClassView } from '../../tools/classes/class.js';
import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

beforeEach(() => {
  loginForTeacher();
  goToTeachersPage();
})

describe('Duplicate class tests', () => {
  it('Is able to duplicate a class without second teachers', () => {
    const classname = `TEST_CLASS_${Math.random()}`
    const duplicate_class = `test class ${Math.random()}`;
    createClass(classname);
    addCustomizations(classname);

    cy.reload();
    cy.wait(500);
    openClassView();
    cy.getDataCy(`duplicate_${classname}`).click();

    cy.getDataCy('modal_prompt_input').type(duplicate_class);
    cy.getDataCy('modal_ok_button').click();

    cy.getDataCy('view_class_link').contains(duplicate_class).click();
    checkCustomizations();
  })

  it('Is able to duplicate class with second teachers, but do not add them', () => {
    openClassView();
    cy.getDataCy("duplicate_CLASS1").click();
    // do not add second teachers
    cy.getDataCy('modal_no_button').should('be.enabled').click();

    const duplicate_class = `test class ${Math.random()}`;
    cy.getDataCy('modal_prompt_input').type(duplicate_class);
    cy.getDataCy('modal_ok_button').click();

    cy.reload();
    cy.wait(500);
    openClassView();
    cy.getDataCy('view_class_link').contains(duplicate_class).click();
    cy.getDataCy('invites_block').should('not.exist');
    checkCustomizations();
  })

  it('Is able to duplicate class with second teachers, do add them', () => {
    openClassView();
    cy.getDataCy("duplicate_CLASS1").click();
    // add second teachers
    cy.getDataCy('modal_yes_button').should('be.enabled').click();

    const duplicate_class = `test class ${Math.random()}`;
    cy.getDataCy('modal_prompt_input').type(duplicate_class);
    cy.getDataCy('modal_ok_button').click();

    cy.reload();
    cy.wait(500);
    openClassView();
    cy.getDataCy('view_class_link').contains(duplicate_class).click();
    cy.getDataCy('invites_block').should('be.visible');
    checkCustomizations();
  })

  it("Is able to click on duplicate button of main teacher's class when second teacher, should not be able to add teachers", () => {
    loginForTeacher("teacher4");
    goToTeachersPage();

    // Take actions only when teacher2 is a second teacher; i.e., having teacher1 as a teacher.
    openClassView();
    cy.get("#classes_table tbody #teacher_cell")
      .each(($username, i) => {
        if ($username.text().includes("teacher1")) {

          cy.getDataCy(`duplicate_CLASS1`).click();
          cy.getDataCy('modal_ok_button').click();

          openClassView();
          cy.getDataCy('view_class_link').contains('CLASS1').click();
          cy.getDataCy('invites_block').should('not.exist');
          checkCustomizations();
        }
      })
  })

  function checkCustomizations() {
    cy.getDataCy('customize_class_button').click();
    cy.getDataCy('opening_date_container').should("not.be.visible")
    cy.getDataCy('opening_date_label').click();
    cy.getDataCy('opening_date_container').should("be.visible")
    cy.getDataCy('enable_level_7').should('be.enabled');
  }
})
