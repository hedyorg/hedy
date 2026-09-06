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

      const seed = Date.now();
      const students = Array.from({length:5}, (_, index) => `student_${index}_${seed}`)
      cy.getDataCy('create_accounts_input').type(students.join('\n'));

      cy.intercept('POST', '/for-teachers/create-accounts').as('createAccounts');
      cy.getDataCy('create_accounts_button').click();
      cy.getDataCy('modal_yes_button').click();
      cy.wait('@createAccounts').its('response.statusCode').should('eq', 200);

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
  // After successful creation, the output table should contain one header row + created student rows.
  cy.getDataCy('create_accounts_output').find('tr').should('have.length', students.length + 1);

  // Go back to the class overview and check that all students appear in the class table
  cy.getDataCy('go_back_button').click();
  cy.url().should('include', 'class/');

  cy.location('pathname').then((pathname) => {
    const classId = pathname.split('/').pop();
    cy.visit(`/for-teachers/legacy/class/${classId}`);
  });

  cy.wrap(students).each((_, index) => {
    cy.contains('[data-cy^="student_"]', students[index]).should('be.visible');
  });
}
