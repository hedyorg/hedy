import {loginForTeacher, logout, login} from '../../../tools/login/login.js'
import { navigateToClass } from "../../../tools/classes/class.js";
import { goToProfilePage } from "../../../tools/navigation/nav.js";

const teachers = ["teacher1", "teacher4"];
const student = 'student5';
const test_class = 'CLASS1';

teachers.forEach((teacher) => {
  it(`Is able to add student by name for ${teacher}`, () => {
    loginForTeacher();
    navigateToClass(test_class);

    // delete student if in class
    cy.getDataCy('adventure_table').then(($div) => {
        if ($div.text().includes(student)){
          cy.getDataCy(`remove_student_${student}`).click();
          cy.getDataCy('htmx_modal_yes_button').click();
        }
    })

    cy.getDataCy('add_student').click();

    cy.getDataCy('invite_student').click();
    cy.getDataCy('modal_prompt_input').type(student);
    cy.getDataCy('modal_ok_button').click();
    cy.wait(500);
    login(student, "123456");

    goToProfilePage();
    cy.getDataCy('join_link').click();

    logout();
    loginForTeacher();
    navigateToClass(test_class);

    cy.getDataCy(`student_${student}`).should(($div) => {
      const text = $div.text()
      expect(text).include(student);
    })
  })
})
