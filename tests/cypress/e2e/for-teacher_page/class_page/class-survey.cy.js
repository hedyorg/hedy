import {loginForTeacher, logout} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'

const surveyView = body => body.find("#survey")
describe('Class Survey View', () => {
  it('Can respond to 1 questions', () => {
    
    loginForTeacher();
    cy.wait(500);

    cy.get("#total_students").should('not.have.value', '0').then(
        cy.get(".view_class").first().click(),
            cy.get("body").then(surveyView).then(survey => {
                if (survey.length){
                    survey = cy.get("#survey")
                    survey.should("exist")
                    survey.get("#input").type("test")
                    survey.get("#submit").click()
                }
            })
    )
  })

  it('Should have 3 questions remaning, can respond to those', () => {
    
    loginForTeacher();
    cy.wait(500);

    cy.get("#total_students").should('not.have.value', '0').then(
        cy.get(".view_class").first().click(),
        cy.get("body").then(surveyView).then(survey => {
            if (survey.length){
                survey = cy.get("#survey")
                survey.should("exist")
                var surveyInputs = Array.from({length:3},(v, k)=>k+1)
                cy.wrap(surveyInputs).each((index) => {
                    cy.getBySel("input_" + index)
                      .type("test")
                      .invoke('val').then((text) => {
                        expect('test').to.equal(text);
                      });
                  });
                survey.get("#submit").click()
            }
        })
    )
  })

  it('Can be skipped - never show again', () => {
    
    loginForTeacher();
    cy.wait(500);

    cy.get("#total_students").should('not.have.value', '0').then(
        cy.get(".view_class").eq(2).click(),
            cy.get("body").then(surveyView).then(survey => {
                if (survey.length){
                    survey = cy.get("#survey")
                    survey.should("exist")
                    survey.get("#skip").click()
                }
            })
    )
  })

  it('Can be skipped - remind me later', () => {
    
    loginForTeacher();
    cy.wait(500);

    cy.get("#total_students").should('not.have.value', '0').then(
        cy.get(".view_class").eq(3).click(),
            cy.get("body").then(surveyView).then(survey => {
                if (survey.length){
                    survey = cy.get("#survey")
                    survey.should("exist")
                    survey.get("#remind_later").click()
                }
            })
    )
  })
})
