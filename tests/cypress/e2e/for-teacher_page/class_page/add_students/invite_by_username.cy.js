import {loginForTeacher, logout, login} from '../../../tools/login/login.js'
import { navigateToClass } from "../../../tools/classes/class.js";

const teachers = ["teacher1", "teacher4"];

teachers.forEach((teacher) => {
  it(`Is able to add student by name for ${teacher}`, () => {
    let student = 'student5'
    cy.intercept('/invite-student').as('invite')
    loginForTeacher();
    navigateToClass();

    // delete student if in class
    cy.getDataCy('class_user_table').then(($div) => {
        if ($div.text().includes(student)){
          cy.getDataCy('remove_student').first().click();
          cy.getDataCy('modal_yes_button').click();
        }
    })

    cy.wait(500);

    cy.getDataCy('add_student').click();

    cy.getDataCy('invite_student').click();
    cy.getDataCy('modal_prompt_input').type(student);
    cy.getDataCy('modal_ok_button').click();
    cy.wait(3000);
    cy.wait('@invite');
    
    login(student, "123456");

    cy.getDataCy('user_dropdown').click();
    cy.getDataCy('my_account_button').click();
    cy.getDataCy('join_link').click();

    logout();
    loginForTeacher();
    navigateToClass();

    cy.getDataCy('student_username_cell').should(($div) => {
      const text = $div.text()
      expect(text).include('student5');
    })
  })
})
