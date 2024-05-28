import {loginForTeacher} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

let className = "CLASS1"

beforeEach(() => {
    loginForTeacher("teacher4");
    goToTeachersPage();
    cy.getBySel('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getBySel('view_classes').click();
      }
    });
    cy.getBySel('view_class_link').contains(new RegExp(`^${className}$`)).click();
    cy.getBySel('survey_status_button').click();
})

describe('Class Survey View', () => {
  it("Can be cancelled", () => {
    cy.getBySel('survey').should("be.visible");
    cy.getBySel('cancel_survey').click();
    cy.getBySel('survey').should("not.be.visible");
  })

  it('Can first respond to 1 question, then to last 3 questions', () => {
    cy.getBySel('survey').should("be.visible");
    cy.getBySel('input_1').type("test");
    cy.getBySel('submit').click();
    cy.getBySel('survey_status_button').click();
    const surveyInputs = Array.from({length:3},(v, k)=> k+1)
    cy.wrap(surveyInputs).each((index) => {
        cy.getBySel("input_" + index)
            .type("test")
            .invoke("val").then((text) => {
              expect("test").to.equal(text);
            });
        });
    cy.getBySel('submit').click();
    cy.getBySel('survey_status_button').contains("complete");
  })
})
