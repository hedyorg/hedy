import { loginForTeacher } from "../../tools/login/login.js"
import { goToProfilePage } from "../../tools/navigation/nav";
import { createClass, navigateToClass } from "../../tools/classes/class";

const secondTeachers = ["teacher2", "teacher3"]

// NOTE: These test steps must execute in sequence. Each of them depends on the previous
// test having executed, in the order they are listed in the file.
// They cannot be made independent until https://github.com/hedyorg/hedy/issues/4804 is resolved
describe("Second teachers: invitations", () => {
  // Before all: create a single class
  let className;
  before(() => {
    loginForTeacher();
    className = createClass()
  });

  it(`Invites ${secondTeachers.length} second teachers: by username`, () => {
    loginForTeacher();
    navigateToClass(className);

    for (const teacher of secondTeachers) {
      cy.getDataCy('add_second_teacher').click();
      cy.getDataCy('modal_prompt_input').type(teacher);
      cy.getDataCy('modal_ok_button').click();
    }

    // Check that both invited teachers are in the table
    for (const teacher of secondTeachers) {
      cy.getDataCy('invites_block')
        .contains(teacher);
    }
  })

  it(`Tries duplicating ${secondTeachers[0]}'s invitation`, () => {
    loginForTeacher();
    navigateToClass(className);

    cy.getDataCy('add_second_teacher').click();
    cy.getDataCy('modal_prompt_input').type(secondTeachers[0]);
    cy.getDataCy('modal_ok_button').click();

    cy.getDataCy('modal_alert_container')
      .contains('pending invitation')
  })

  it(`Deletes ${secondTeachers[1]}'s invitation`, () => {
    loginForTeacher();
    navigateToClass(className);

    cy.getDataCy('invites_block invite_username_cell')
      .contains(secondTeachers[1])
      .parent('tr')
      .find('[data-cy="remove_user_invitation"]')
      .click();

    cy.getDataCy('modal_confirm modal_yes_button').click();

    // This needs to come before we accept teacher2's invitation, otherwise
    // after this there are no invites and so this table isn't rendered at all.
    cy.getDataCy('invites_block')
      .should("not.contain", secondTeachers[1]);
  });

  it(`Accepts invitation sent to ${secondTeachers[0]}`, () => {
    cy.intercept('class/join/**').as('join');
    loginForTeacher(secondTeachers[0]);
    goToProfilePage();
    cy.getDataCy('join_link').click();
    // Give the Ajax request that gets sent as a result of the click enough time to complete
    cy.wait('@join');
  })

  it(`After accepting, the teacher table now contains ${secondTeachers[0]}`, () => {
    loginForTeacher();
    navigateToClass(className);

    cy.getDataCy('second_teacher_username_cell').contains(secondTeachers[0]);
  })
})
