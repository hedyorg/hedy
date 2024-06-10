import { loginForTeacher } from "../../tools/login/login.js"
import { goToProfilePage } from "../../tools/navigation/nav";
import { createClass, navigateToClass } from "../../tools/classes/class";

const testSecondTeachers = ["teacher2", "teacher3", "teacher4"]
const secondTeachers = ["teacher2", "teacher3"]
let className;

before(() => {
  loginForTeacher();
  className = createClass()
});

beforeEach(() => {
  loginForTeacher();
  navigateToClass(className);
});

it(`Is able to invite second teachers by username, accept it and check it`, () => {
  // first add all teachers
  for (const teacher of testSecondTeachers) {
    cy.getDataCy('add_second_teacher').click();
    cy.getDataCy('modal_prompt_input').type(teacher);
    cy.getDataCy('modal_ok_button').click();
    cy.getDataCy('invites_block')
    .contains(teacher);
  }

  //duplicate third teacher
  cy.getDataCy('add_second_teacher').click();
  cy.getDataCy('modal_prompt_input').type(testSecondTeachers[2]);
  cy.getDataCy('modal_ok_button').click();
  cy.getDataCy('modal_alert_container')
  .contains('pending invitation')

  //delete third teacher
  cy.getDataCy('invites_block invite_username_cell')
  .contains(testSecondTeachers[2])
  .parent('tr')
  .find('[data-cy="remove_user_invitation"]')
  .click();
  cy.getDataCy('modal_confirm modal_yes_button').click();

  // This needs to come before we accept teacher2's invitation, otherwise
  // after this there are no invites and so this table isn't rendered at all.
  cy.getDataCy('invites_block')
    .should("not.contain", testSecondTeachers[2]);

  //then accept other teachers invitations
  for (const teacher of secondTeachers) {
    cy.intercept('class/join/**').as('join');
    loginForTeacher(teacher);
    goToProfilePage();
    cy.getDataCy('join_link').click();
    // Give the Ajax request that gets sent as a result of the click enough time to complete
    cy.wait('@join');
  }

  //check if teacher table now cotains the teachers
  loginForTeacher();
  navigateToClass(className);
  cy.getDataCy('second_teacher_username_cell').contains(secondTeachers[0]);
  cy.getDataCy('second_teacher_username_cell').contains(secondTeachers[1]);
})
