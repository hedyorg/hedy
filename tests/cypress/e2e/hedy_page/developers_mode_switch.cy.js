import { loginForStudent, loginForTeacher, logout } from "../tools/login/login";
import { goToHedyPage } from "../tools/navigation/nav";
import { createClassAndAddStudents, navigateToClass } from '../tools/classes/class.js'

let classname;
let students;

it('Should be able to enforce developer mode as a teacher', () => {
  loginForTeacher();
  cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      

  ({classname, students} = createClassAndAddStudents());
  navigateToClass(classname);

  cy.getDataCy('customize_class_button').click();
  cy.getDataCy('developers_mode')
    .should("not.be.checked")
    .click()

  cy.getDataCy('developers_mode')
    .should("be.checked")
  
  cy.wait(1000)
  cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);

  logout();
  loginForStudent(students[0]);
  goToHedyPage();
  
  cy.getDataCy('adventures_tab').should('not.exist');
})