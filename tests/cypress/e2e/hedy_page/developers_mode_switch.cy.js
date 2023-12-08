import { loginForStudent, loginForTeacher, logout } from "../tools/login/login";
import { goToHedyPage } from "../tools/navigation/nav";
import { createClassAndAddStudents, navigateToClass } from '../tools/classes/class.js'

let classname;
let students;

describe('Developers mode', () => {
    it('Should toggle on and off', () => {
      goToHedyPage();
      
      cy.get('#toggle_circle').click(); // Developers mode is switched on
      cy.reload();
      cy.get('#adventures').should('not.be.visible');

      cy.get('#toggle_circle').click(); // Developers mode is switched off
      cy.reload();
      cy.get('#adventures').should('be.visible');
    })

    it('Should be enforced developer mode', () => {
      goToHedyPage();
      loginForTeacher();
      ({classname, students} = createClassAndAddStudents());
      navigateToClass(classname);

      cy.get("#customize-class-button").click();
      cy.get("#developers_mode").click();
      cy.getBySel("save_customizations").click();

      logout();
      loginForStudent(students[0]);
      goToHedyPage();
      
      cy.reload();
      cy.get('#adventures').should('not.be.visible');
    })
})