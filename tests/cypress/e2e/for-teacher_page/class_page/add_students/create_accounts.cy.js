import {loginForTeacher} from '../../../tools/login/login.js'
import {createClassAndAddStudents, navigateToClass} from '../../../tools/classes/class.js'

let classname;
let students;
const teachers = ["teacher1", "teacher4"];

before(() => {
  loginForTeacher();
  ({classname, students} = createClassAndAddStudents());
})

beforeEach(() => {
  loginForTeacher();
  navigateToClass(classname);
  cy.getDataCy('add_student').click();
  cy.getDataCy('create_accounts').click();
})

teachers.forEach((teacher) => {
  describe(`Testing creating accounts for ${teacher}`, () => {
    it('Is able to click on go back button and see if students created in createClassAndAddStudents() are present', () => {
        cy.getDataCy('go_back_button').click();
        cy.wait(1000);
        cy.url().should('include', 'class/'); 

      cy.getDataCy('student_username_cell').should(($div) => {
        const text = $div.text();
        expect(text).include(students[0]);
      }) 
    })

    it('Is able to download login credentials and generate passwords', () => {
      ({classname, students} = createClassAndAddStudents());
      // download login credentials
      cy.readFile('cypress/downloads/accounts.csv');

      // generate passwords
      cy.getDataCy('toggle_circle').click(); //switches the toggle on so that passwords are generated
      cy.wait(1000);
      cy.get(':nth-child(2) > [data-cy="password"]').should('have.length.greaterThan', 0);
    })

    it('Is able to add and remove a row and use the reset button', () => {
      // testing add a row
      cy.getDataCy('add_multiple_rows').click();
      cy.get(':nth-child(6) > [data-cy="username"]').should('have.value', '');
      // testing removing a row
      // fills in two rows
      cy.get(':nth-child(2) > [data-cy="username"]').type("student10");
      cy.get(':nth-child(2) > [data-cy="password"]').type("123456");
      cy.get(':nth-child(3) > [data-cy="username"]').type("student11");
      cy.get(':nth-child(3) > [data-cy="password"]').type("123456");
      cy.wait(1000);
      // checks if they are filled
      cy.get(':nth-child(2) > [data-cy="username"]').should('have.value', 'student10');
      cy.get(':nth-child(3) > [data-cy="username"]').should('have.value', 'student11');
      // deletes the first row
      cy.get(':nth-child(2) > .fill-current > path').click();
      cy.wait(1000);
      // check if the first row is now student12
      cy.get(':nth-child(2) > [data-cy="username"]').should('have.value', 'student11');
      // testing reseting
      cy.getDataCy('reset_button').click();
      cy.wait(1000);
      cy.get(':nth-child(2) > [data-cy="username"]').should('have.value', '');
      cy.get(':nth-child(3) > [data-cy="username"]').should('have.value', '');
    })
  })
})