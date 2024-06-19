import {loginForTeacher} from '../../../tools/login/login.js'
import {createClassAndAddStudents, navigateToClass} from '../../../tools/classes/class.js'

let classname;
let students;
const teachers = ["teacher1", "teacher4"];

before(() => {
  loginForTeacher();
})

beforeEach(() => {
  loginForTeacher();
  navigateToClass(classname);
  cy.getDataCy('add_student').click();
  cy.getDataCy('create_accounts').click();
})

teachers.forEach((teacher) => {
  describe(`Testing creating accounts for ${teacher}`, () => {
    it('Is able to download login credentials, generate passwords, click on go back button and see if students created in createClassAndAddStudents() are present', () => {
      ({classname, students} = createClassAndAddStudents());
      // download login credentials
      cy.readFile('cypress/downloads/accounts.csv');

      // generate passwords
      cy.getDataCy('toggle_circle').click();
      cy.getDataCy('password_1').should('have.length.greaterThan', 0);

      cy.getDataCy('go_back_button').click();
      cy.url().should('include', 'class/'); 

      cy.getDataCy('student_username_cell').should(($div) => {
        const text = $div.text();
        expect(text).include(students[0]);
      })
    })

    it('Is able to add and remove a row and use the reset button', () => {
      // testing add a row
      cy.getDataCy('add_multiple_rows').click();
      cy.getDataCy('username_6').should('have.value', '').should('have.value', '');
      // testing removing a row
      // fills in two rows
      cy.getDataCy('username_1').type("student10");
      cy.getDataCy('password_1').type("123456");
      cy.getDataCy('username_2').type("student11");
      cy.getDataCy('password_2').type("123456");

      // deletes the first row
      cy.getDataCy('remove_student_1').click();
      // check if the first row is now student11
      cy.getDataCy('username_2').should('have.value', 'student11');
      cy.getDataCy('username_3').should('have.value', '');
      // testing reseting
      cy.getDataCy('reset_button').click();
      cy.getDataCy('username_2').should('have.value', '');
      cy.getDataCy('username_3').should('have.value', '');
    })
  })
})