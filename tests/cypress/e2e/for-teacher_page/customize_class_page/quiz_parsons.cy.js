import { loginForStudent, loginForTeacher } from '../../tools/login/login.js'
import { ensureClass, openClassView, removeCustomizations, selectLevel } from "../../tools/classes/class";
import { goToHedyLevel } from '../../tools/navigation/nav.js';

const teachers = ["teacher1", "teacher4"];

teachers.forEach((teacher) => {
  describe(`customize class page - quiz parsons for ${teacher}`, () => {
      beforeEach(() => {
        loginForTeacher(teacher);
        ensureClass();
        openClassView("CLASS1");

        // Remove any customizations that already exist to get the class into a predictable state
        removeCustomizations();
      });

      it('Is able to remove the puzzle and quiz from level 2 and then add them back', () => {
        selectLevel('2');

        // remove the quiz
        cy.getDataCy('hide_quiz').click();
        cy.getDataCy('quiz').should("not.exist")

        // remove the puzzle
        cy.getDataCy('hide_parsons').click();
        cy.getDataCy('parsons').should("not.exist")

        // add them from available list
        cy.getDataCy('available_adventures_current_level').select("quiz")
        cy.getDataCy('available_adventures_current_level').select("parsons")

        // Now the order should be quiz as last, then parsons.
        cy.getDataCy('parsons').should("exist")
        cy.getDataCy('quiz').last().should("exist");

        // make sure they are visible
        loginForStudent();
        goToHedyLevel(2);
        cy.getDataCy('quiz').scrollIntoView().should('be.visible');
        cy.getDataCy('parsons').scrollIntoView().should('be.visible');
      });

      it('Is able to disable all quizes and parsons', () => {
        cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      

        cy.getDataCy('hide_quiz')
            .should("not.be.checked")
            .click()

        cy.getDataCy('hide_quiz')
            .should("be.checked")

        cy.getDataCy('hide_parsons')
            .should("not.be.checked")
            .click()

        cy.getDataCy('hide_parsons')
            .should("be.checked")

        cy.wait('@updateCustomizations');

        selectLevel('3');
        cy.getDataCy('level_3 quiz')
          .should("not.exist")

        cy.getDataCy('level_3 parsons')
          .should("not.exist")

        loginForStudent();
        goToHedyLevel(5);
        cy.getDataCy('quiz').should('not.exist');
        cy.getDataCy('parsons').should('not.exist');
      });
  });
});
