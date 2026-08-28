import { createClass, addCustomizations, openClassView } from '../../tools/classes/class.js';
import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

beforeEach(() => {
  loginForTeacher();
  goToTeachersPage();
})

describe('Duplicate class tests', () => {
  it('Is able to duplicate a class without second teachers', () => {
    const classname = `TEST_CLASS_${Date.now()}`
    const duplicate_class = `test class ${Date.now()}_dup1`;
    createClass(classname);
    addCustomizations(classname);
    duplicateClassByApi(classname, duplicate_class, false);

    cy.reload();
    cy.wait(500);
    openClassView(duplicate_class);
    cy.url().should('include', '/for-teachers/legacy/class/');
    cy.getDataCy('customize_class_button').should('be.visible');
  })

  it('Is able to duplicate class with second teachers, but do not add them', () => {
    const classname = `TEST_CLASS_${Date.now()}_st1`;
    const duplicate_class = `test class ${Date.now()}_dup2`;

    createClass(classname);
    duplicateClassByApi(classname, duplicate_class, false);

    cy.reload();
    cy.wait(500);
    openClassView(duplicate_class);
    cy.getDataCy('invites_block').should('be.visible');
    cy.url().should('include', '/for-teachers/legacy/class/');
    cy.getDataCy('customize_class_button').should('be.visible');
  })

  it('Is able to duplicate class with second teachers, do add them', () => {
    const classname = `TEST_CLASS_${Date.now()}_st2`;
    const duplicate_class = `test class ${Date.now()}_dup3`;

    createClass(classname);
    duplicateClassByApi(classname, duplicate_class, true);

    cy.reload();
    cy.wait(500);
    openClassView(duplicate_class);
    cy.getDataCy('invites_block').should('be.visible');
    cy.url().should('include', '/for-teachers/legacy/class/');
    cy.getDataCy('customize_class_button').should('be.visible');
  })

  it("Is able to click on duplicate button of main teacher's class when second teacher, should not be able to add teachers", () => {
    loginForTeacher("teacher4");
    goToTeachersPage();

    // Take actions only when teacher2 is a second teacher; i.e., having teacher1 as a teacher.
    openClassView();
    cy.get("#classes_table tbody tr ")
      .each(($row, i) => {
        const $username_cell = $row.find('[data-cy="teacher_cell"]');
        const $name_cell = $row.find('[data-cy="view_class_link"]');
        if ($name_cell.text() === 'CLASS1' && $username_cell.text().includes("teacher1")) {

          cy.wrap($row.find('[data-cy="duplicate_CLASS1"]')).click();
          cy.getDataCy('modal_ok_button').click();

          openClassView("CLASS1");
          cy.getDataCy('invites_block').should('not.exist');
          cy.url().should('include', '/for-teachers/legacy/class/');
          cy.getDataCy('customize_class_button').should('be.visible');
        }
      })
  })

  function duplicateClassByApi(sourceClassName, duplicatedClassName, copySecondTeachers) {
    cy.visit('/for-teachers/class/all');
    cy.contains('[data-cy="view_class_link"]', sourceClassName)
      .invoke('attr', 'href')
      .then((href) => {
        const classId = href.split('/').pop();
        cy.request({
          method: 'POST',
          url: '/duplicate_class',
          body: {
            id: classId,
            name: duplicatedClassName,
            copy_second_teachers: copySecondTeachers,
          },
          failOnStatusCode: false,
        }).its('status').should('eq', 200);
      });
  }
})
