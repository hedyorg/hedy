import {loginForTeacher, logout} from "../../tools/login/login.js"
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
      cy.get("#add-second-teacher").click();
      cy.get("#modal-prompt-input").type(teacher);
      cy.get("#modal-ok-button").click();
    }

    // Check that both invited teachers are in the table
    for (const teacher of secondTeachers) {
      cy.get("#invites-block table")
        .contains(teacher);
    }
  })

  it(`Tries duplicating ${secondTeachers[0]}'s invitation`, () => {
    loginForTeacher();
    navigateToClass(className);

    cy.get("#add-second-teacher").click();
    cy.get("#modal-prompt-input").type(secondTeachers[0]);
    cy.get("#modal-ok-button").click();

    cy.get("#modal_alert_container")
      .contains('pending invitation')
  })

  it(`Deletes ${secondTeachers[1]}'s invitation`, () => {
    loginForTeacher();
    navigateToClass(className);

    cy.get("#invites-block table")
      .get('.username_cell')
      .contains(secondTeachers[1])
      .parent('tr')
      .children('.remove_user_invitation')
      .children('a')
      .click();

    cy.get('#modal-confirm #modal-yes-button').click();

    // This needs to come before we accept teacher2's invitation, otherwise
    // after this there are no invites and so this table isn't rendered at all.
    cy.get("#invites-block table")
      .should("not.contain", secondTeachers[1]);
  });

  it(`Accepts invitation sent to ${secondTeachers[0]}`, () => {
    loginForTeacher(secondTeachers[0]);
    goToProfilePage();
    cy.get("#messages #join").click();
  })

  it(`After accepting, the teacher table now contains ${secondTeachers[0]}`, () => {
    loginForTeacher();
    navigateToClass(className);

    cy.get("#second_teachers_container .username_cell").contains(secondTeachers[0]);
  })
})
