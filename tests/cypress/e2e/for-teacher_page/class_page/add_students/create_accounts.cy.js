import { loginForTeacher } from '../../../tools/login/login.js'
import { createClassAndAddStudents, createClass, navigateToClass } from '../../../tools/classes/class.js'

const teachers = ["teacher1", "teacher4"];

beforeEach(() => {
  loginForTeacher();
})

teachers.forEach((teacher) => {
  describe(`Testing creating accounts for ${teacher}`, () => {
    it('Is able to create student accounts with usernames', () => {
      const className = createClass();

      navigateToClass(className);
      cy.wait(500);

      cy.getDataCy('add_student').click();
      cy.getDataCy('create_accounts').click();

      const students = Array.from({length:5}, (_, index) => `student_${index}_${Math.random()}`)
      cy.getDataCy('create_accounts_input').type(students.join('\n'));

      cy.getDataCy('create_accounts_button').click();
      cy.getDataCy('modal_yes_button').click();

      ensureStudentsCreatedSuccessfully(students);
    })

    it('Is able to create student accounts with usernames and passwords', () => {
      // This test is relying on the util method used to create a class with students
      let {_, students} = createClassAndAddStudents();

      ensureStudentsCreatedSuccessfully(students);
    })
  })
})

function ensureStudentsCreatedSuccessfully(students)
{
  // Accounts are created successfully when the input textarea is hidden and the results table is displayed
  cy.getDataCy('create_accounts_output').should('be.visible');
  cy.getDataCy('create_accounts_input').should('not.be.visible');

  // Go back to the class overview and check that all students appear in the class table
  cy.getDataCy('go_back_button').click();
  cy.url().should('include', 'class/');

  cy.wrap(students).each((_, index) => {
    cy.getDataCy(`student_${students[index]}`).should('contain.text', students[index])
  });
}
