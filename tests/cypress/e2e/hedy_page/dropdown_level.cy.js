import { loginForStudent, loginForTeacher, logout } from "../tools/login/login";
import  { goToHedyLevel } from "../tools/navigation/nav";
import { createClassAndAddStudents, addCustomizations } from '../tools/classes/class.js'

describe('Go to level dropdown', () => {
  it('Is not able to go to disabled level 7', () => {  
    cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      
    
    loginForTeacher();
    cy.wait(500);
    
    let classname;
    let students;
    ({classname, students} = createClassAndAddStudents());
    addCustomizations(classname);
    logout()
    loginForStudent(students[0]);
    cy.wait(500);
    goToHedyLevel(2);

    cy.getDataCy('dropdown_level_button').click();
    cy.getDataCy('level_button_4').should('not.be.disabled');
    cy.getDataCy('level_button_7').should('be.disabled');
  })
})
