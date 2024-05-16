import {loginForTeacher} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

let className = "CLASS1"

beforeEach(() => {
    loginForTeacher("teacher4");
    goToTeachersPage();
    cy.get('[data-cy="view_class_link"]').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get('[data-cy="view_classes"]').click();
      }
    });
    cy.get('[data-cy="view_class_link"]').contains(new RegExp(`^${className}$`)).click();
    cy.get('[data-cy="survey_status_button"]').click();
})

describe('Class Survey View', () => {
  it("Can be cancelled", () => {
    cy.get('[data-cy="survey"]').should("be.visible");
    cy.get('[data-cy="cancel_survey"]').click();
    cy.get('[data-cy="survey"]').should("not.be.visible");
  })

  it('Can first respond to 1 question, then to last 3 questions', () => {
    cy.get('[data-cy="survey"]').should("be.visible");
    cy.get('[data-cy="input_1"]').type("test");
    cy.get('[data-cy="submit"]').click();
    cy.get('[data-cy="survey_status_button"]').click();
    const surveyInputs = Array.from({length:3},(v, k)=> k+1)
    cy.wrap(surveyInputs).each((index) => {
        cy.getBySel("input_" + index)
            .type("test")
            .invoke("val").then((text) => {
              expect("test").to.equal(text);
            });
        });
    cy.get('[data-cy="submit"]').click();
    cy.get('[data-cy="survey_status_button"]').contains("complete");
  })
})
