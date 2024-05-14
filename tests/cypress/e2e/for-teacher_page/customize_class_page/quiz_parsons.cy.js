import { loginForStudent, loginForTeacher } from '../../tools/login/login.js'
import { ensureClass } from "../../tools/classes/class";

describe('customize class page', () => {
    beforeEach(() => {
      loginForTeacher();
      ensureClass();
      cy.get(".view_class").then($viewClass => {
        if (!$viewClass.is(':visible')) {
            cy.get("#view_classes").click();
        }
      });
      cy.getBySel('view_class_link').first().click(); // Press on view class button
      cy.get('body').then($b => $b.find("#survey")).then($s => $s.length && $s.hide())
      cy.getBySel('customize_class_button').click(); // Press customize class button

      // Remove any customizations that already exist to get the class into a predictable state
      // This always throws up a modal dialog
      cy.intercept('/for-teachers/restore-customizations*').as('restoreCustomizations');      
      cy.getBySel('remove_customizations_button').click();
      cy.getBySel('modal_yes_button').click();
      cy.wait('@restoreCustomizations');
    });

    it('checks that puzzle and quiz exist in list', () => {
      // validate and then remove the quiz
      cy.get('[data-cy="level-1"] [data-cy="quiz"]')
        .should("exist")

      cy.get('[data-cy="level-1"] [data-cy="parsons"]')
        .should("exist")

    });

    it('removes the puzzle and quiz from level 2', () => {
      // Click on level 2
      cy.getBySel("adventures")
        .select('2')
        .should('have.value', '2');

      // validate and then remove the quiz
      cy.get('[data-cy="level-2"] div:last input')
        .should('have.value', 'quiz')

      cy.get('[data-cy="level-2"] div:last [data-cy="hide"]')
        .click();

      cy.get('[data-cy="level-2"] [data-cy="quiz"]')
        .should("not.exist")

      // validate and then remove the puzzle
      cy.get('[data-cy="level-2"] div:last input')
        .should('have.value', 'parsons')

      cy.get('[data-cy="level-2"] div:last [data-cy="hide"]')
        .click();

      cy.get('[data-cy="level-2"] [data-cy="parsons"]')
        .should("not.exist")
    });

    it('remove and add puzzle and quiz (with order)', () => {
      // validate and then remove the quiz
      cy.get('[data-cy="level-1"] div:last input')
        .should('have.value', 'quiz')

      cy.get('[data-cy="level-1"] div:last [data-cy="hide"]')
        .click();

      cy.get('[data-cy="level-1"] [data-cy="quiz"]')
        .should("not.exist")

      // validate and then remove the puzzle
      cy.get('[data-cy="level-1"] div:last input')
        .should('have.value', 'parsons')

      cy.get('[data-cy="level-1"] div:last [data-cy="hide"]')
        .click();

      cy.get('[data-cy="level-1"] [data-cy="parsons"]')
        .should("not.exist")

      // add them from available list
      cy.getBySel("available_adventures_current_level")
        .select("quiz")

      cy.getBySel("available_adventures_current_level")
        .select("parsons")

      // Now the order should be quiz as last, then parsons.
      cy.get('[data-cy="level-1"] [data-cy="parsons"]')
        .should("not.exist")

      cy.get('[data-cy="level-1"] div:last input')
        .should('have.value', 'quiz')
    });

    it.only('disable all quizes', () => {
      cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      

      cy.get("#hide_quiz")
          .should("not.be.checked")
          .click()

      cy.get("#hide_quiz")
          .should("be.checked")

      cy.wait(1000)
      cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);

      cy.reload();

      cy.get('[data-cy="level-1"] [data-cy="quiz"]')
        .should("not.exist")
    });

    it('disable all parsons', () => {
      cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      

      cy.get("#hide_parsons")
          .should("not.be.checked")
          .click()

      cy.get("#hide_parsons")
          .should("be.checked")

      cy.wait(1000)
      cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);

      cy.reload();

      cy.get('[data-cy="level-1"] [data-cy="parsons"]')
        .should("not.exist")
    });

    it('hide explore page', () => {
      cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      

      cy.get("#hide_explore")
          .should("not.be.checked")
          .click()

      cy.get("#hide_explore")
          .should("be.checked")

      cy.wait(1000)
      cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);
      loginForStudent();
      cy.get("#explorebutton").should("not.exist")
    });
});