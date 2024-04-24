import { loginForStudent, loginForTeacher, logout } from "../tools/login/login";
import { goToHedyPage } from "../tools/navigation/nav";
import { createClassAndAddStudents, navigateToClass } from '../tools/classes/class.js'

let classname;
let students;

describe('Developers mode', () => {
    beforeEach(() => {
      loginForTeacher();
    })
    it('Should toggle on and off', () => {
      goToHedyPage();
      
      cy.get('#toggle_circle').click(); // Developers mode is switched on
      cy.get('#adventures').should('not.be.visible');

      cy.get('#toggle_circle').click(); // Developers mode is switched off
      cy.get('#adventures').should('be.visible');
    })

    it('Should be enforced developer mode', () => {
      cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      

      ({classname, students} = createClassAndAddStudents());
      navigateToClass(classname);

      cy.get("#customize-class-button").click();
      cy.get("#developers_mode")
        .should("not.be.checked")
        .click()

      cy.get("#developers_mode")
        .should("be.checked")
      
      cy.wait(1000)
      cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);

      logout();
      loginForStudent(students[0]);
      goToHedyPage();
      
      cy.get('#adventures').should('not.be.visible');
    })
})