import { loginForStudent, loginForTeacher } from '../../tools/login/login.js'
import { ensureClass, openClassView, removeCustomizations, selectLevel } from "../../tools/classes/class";
import { goToHedyLevel2Page, goToHedyLevel5Page } from '../../tools/navigation/nav.js';

// Do we also want this to be tested for a second_teacher?
describe('customize class page', () => {
    beforeEach(() => {
      loginForTeacher();
      ensureClass();
      openClassView("CLASS1");

      // Remove any customizations that already exist to get the class into a predictable state
      removeCustomizations();
    });

    it('Is able to remove the puzzle and quiz from level 2 and then add them back', () => {
      selectLevel('2');

      // remove the quiz
      cy.getDataCy('hide_quiz').scrollIntoView().should('be.visible');
      cy.getDataCy('hide_quiz').click();
      cy.getDataCy('quiz').should("not.exist")

      // remove the puzzle
      cy.getDataCy('hide_parsons').scrollIntoView().should('be.visible');
      cy.getDataCy('hide_parsons').click();
      cy.getDataCy('parsons').should("not.exist")

      // add them from available list
      cy.getDataCy('available_adventures_current_level').select("quiz")
      cy.getDataCy('available_adventures_current_level').select("parsons")

      // Now the order should be quiz as last, then parsons.
      cy.getDataCy('parsons').scrollIntoView().should("exist")
      // scrol to get quiz into view and make sure its the last one
      cy.getDataCy('quiz').scrollIntoView().last().should("exist");

      // make sure they are visible
      loginForStudent();
      goToHedyLevel2Page();
      cy.getDataCy('quiz').scrollIntoView().should('be.visible');
      cy.getDataCy('parsons').scrollIntoView().should('be.visible');
    });

    it('Is able to disable all quizes and parsons', () => {
      cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      

      cy.getDataCy('hide_quiz_setting')
          .should("not.be.checked")
          .click()

      cy.getDataCy('hide_quiz_setting')
          .should("be.checked")

      cy.getDataCy('hide_parsons_setting')
          .should("not.be.checked")
          .click()

      cy.getDataCy('hide_parsons_setting')
          .should("be.checked")

      cy.wait(1000)
      cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);
      cy.reload();

      cy.getDataCy('level_3 quiz')
        .should("not.exist")

      cy.getDataCy('level_3 parsons')
        .should("not.exist")

      loginForStudent();
      goToHedyLevel5Page();
      cy.getDataCy('quiz').should('not.exist');
      cy.getDataCy('parsons').should('not.exist');
    });


    it('Is able to hide the explore page', () => {
      cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      

      cy.getDataCy('hide_explore_setting')
          .should("not.be.checked")
          .click()

      cy.getDataCy('hide_explore_setting')
          .should("be.checked")

      cy.wait(1000)
      cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);
      cy.reload();
    
      loginForStudent();
      cy.getDataCy('explorebutton').should("not.exist")
    });
});