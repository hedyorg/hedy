import {loginForTeacher} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';
import { openClassView } from "../../tools/classes/class";

let className = "CLASS1"

beforeEach(() => {
    loginForTeacher("teacher4");
    goToTeachersPage();
    openClassView();
    cy.getDataCy('view_class_link').contains(new RegExp(`^${className}$`)).click();
    cy.getDataCy('survey_status_button').click();
})

describe('Class Survey View', () => {
  it("Can be cancelled", () => {
    cy.getDataCy('survey').should("be.visible");
    cy.getDataCy('cancel_survey').click();
    cy.getDataCy('survey').should("not.be.visible");
  })

  it('Can first respond to 1 question, then to last 3 questions', () => {
    cy.getDataCy('survey').should("be.visible");
    cy.getDataCy('input_1').type("test");
    cy.getDataCy('submit').click();
    cy.getDataCy('survey_status_button').click();
    const surveyInputs = Array.from({length:3},(v, k)=> k+1)
    cy.wrap(surveyInputs).each((index) => {
        cy.getDataCy("input_" + index)
            .type("test")
            .invoke("val").then((text) => {
              expect("test").to.equal(text);
            });
        });
    cy.getDataCy('submit').click();
    cy.getDataCy('survey_status_button').contains("complete");
  })
})
