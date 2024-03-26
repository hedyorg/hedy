import {loginForTeacher} from '../../tools/login/login.js'
import {createClassAndAddStudents} from '../../tools/classes/class.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

let className = "CLASS1"

beforeEach(() => {
    loginForTeacher("teacher4");
    goToTeachersPage();
    cy.get(".view_class").then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get("#view_classes").click();
      }
    });
    cy.get(".view_class").contains(new RegExp(`^${className}$`)).click();
    cy.get("#survey_status_button").click();
})

describe('Class Survey View', () => {
  it.only("Can be cancelled", () => {
    cy.get("#survey").should("be.visible");
    cy.get("#cancel_survey").click();
    cy.get("#survey").should("not.be.visible");
  })

  it('Can first respond to 1 question, then to last 3 questions', () => {
    cy.get("#survey").should("be.visible");
    cy.get("#input").type("test");
    cy.get("#submit").click();
    cy.get("#survey_status_button").click();
    const surveyInputs = Array.from({length:3},(v, k)=> k+1)
    cy.wrap(surveyInputs).each((index) => {
        cy.getBySel("input_" + index)
            .type("test")
            .invoke("val").then((text) => {
              expect("test").to.equal(text);
            });
        });
    cy.get("#submit").click();
    cy.get("#survey_status_button").contains("complete");
  })


  // TODO: add and adjust the following when the survey view renders by default.
  // it('Can be skipped and survey is not shown after', () => {
  //   cy.get("#skip").click();
  //   goToTeachersPage();
  //   cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
  //   cy.get("#survey").should('not.exist');
  // })

  // it('Can be skipped and survey is not shown after', () => {
  //   cy.get("#remind_later").click();
  //   goToTeachersPage();
  //   cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
  //   cy.get("#survey").should('not.exist');
  // })
})
