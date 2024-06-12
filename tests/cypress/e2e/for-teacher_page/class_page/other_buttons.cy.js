import {loginForTeacher} from '../../tools/login/login.js'
import { navigateToClass } from "../../tools/classes/class.js";
import { goToTeachersPage } from '../../tools/navigation/nav.js';

beforeEach(() => {
  // do we want this test to be run for a second teacher as well?
  loginForTeacher("teacher1");
  navigateToClass();
})

it('Is able to click on customize class page button', () => {
  var currentUrl = '';
  cy.url().then(url => {
    currentUrl = url;
    cy.getDataCy('customize_class_button').click();

    let statsUrl = Cypress.env('customize_class_page') + currentUrl.substring(currentUrl.indexOf('class/')+6);
    cy.url().should('include', statsUrl);
  })    
})

it('Is able to click on go back button', () => {
  cy.getDataCy('go_back_button').click();   

  cy.url()
    .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
})

it('Is able to click on survey button, cancel it, respond to 1 question, then 3 to finish', () => {
  // cancel survey
  cy.getDataCy('survey_status_button').click();
  cy.getDataCy('survey').should("be.visible");
  cy.getDataCy('cancel_survey').click();
  cy.getDataCy('survey').should("not.be.visible");
  // respond to 1 question
  cy.getDataCy('survey_status_button').click();
  cy.getDataCy('survey').should("be.visible");
  cy.getDataCy('input_1').type("test");
  cy.getDataCy('submit').click();
  // respond to last 3 questions
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