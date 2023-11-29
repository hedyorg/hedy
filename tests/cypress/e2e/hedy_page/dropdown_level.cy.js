import { loginForStudent, loginForTeacher } from "../tools/login/login";
import {goToHedyLevel2Page, goToTeachersPage} from "../tools/navigation/nav";
import {createClassAndAddStudents} from '../tools/classes/class.js'

describe('Go to level dropdown', () => {
  it('Is not able to go to disabled level 5', () => {  
    let classname;
    let students;

    loginForTeacher();
    cy.wait(500);

    ({classname, students} = createClassAndAddStudents());
    goToTeachersPage();

    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
    cy.get('body').then($b => $b.find("#survey")).then($s => $s.length && $s.hide());
    cy.getBySel('customize_class_button').click();
    cy.get('#enable_level_5').parent('.switch').click();
    cy.getBySel('save_customizations').click();

    loginForStudent(students[0]);
    cy.wait(500);
    goToHedyLevel2Page();

    cy.get('#dropdown_level_button').click();
    cy.get('#level_button_4').should('not.be.disabled');
    cy.get('#level_button_5').should('be.disabled');
  })
})