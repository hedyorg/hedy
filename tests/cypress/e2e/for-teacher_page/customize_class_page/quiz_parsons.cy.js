import { loginForStudent, loginForTeacher } from '../../tools/login/login.js'
import { ensureClass, openClassView, removeCustomizations } from "../../tools/classes/class";
import { goToHedyLevel2Page, goToHedyLevel5Page } from '../../tools/navigation/nav.js';

describe('customize class page', () => {
    beforeEach(() => {
      loginForTeacher();
      ensureClass();
      openClassView();
      cy.getDataCy('view_class_link').contains("CLASS1").click(); // Press on view class button
      cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())

      // Remove any customizations that already exist to get the class into a predictable state
      // This always throws up a modal dialog
      removeCustomizations();
      cy.getDataCy('opening_date_label').click();
    });

    it('Is able to remove the puzzle and quiz from level 2 and then add them back', () => {
      // Click on level 2
      cy.getDataCy("levels_dropdown")
        .select('2')
        .should('have.value', '2');

      // validate and then remove the quiz
      cy.get('[data-cy="level_2"] div:last input')
        .should('have.value', 'quiz')

      cy.get('[data-cy="level_2"] div:last [data-cy="hide"]')
        .click();

      cy.getDataCy('level_2 quiz')
        .should("not.exist")

      // validate and then remove the puzzle
      cy.get('[data-cy="level_2"] div:last input')
        .should('have.value', 'parsons')

      cy.get('[data-cy="level_2"] div:last [data-cy="hide"]')
        .click();

      cy.getDataCy('level_2 parsons')
        .should("not.exist")

      // add them from available list
      cy.getDataCy("available_adventures_current_level")
        .select("quiz")

      cy.getDataCy("available_adventures_current_level")
        .select("parsons")

      // Now the order should be quiz as last, then parsons.
      cy.getDataCy('level_2 parsons')
        .should("exist")

      cy.get('[data-cy="level_2"] div:last input')
        .should('have.value', 'quiz')
      
      cy.wait(1000);

      loginForStudent();
      goToHedyLevel2Page();
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

      cy.getDataCy('hide_explore')
          .should("not.be.checked")
          .click()

      cy.getDataCy('hide_explore')
          .should("be.checked")

      cy.wait(1000)
      cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);
      cy.reload();
    
      loginForStudent();
      cy.getDataCy('explorebutton').should("not.exist")
    });
});