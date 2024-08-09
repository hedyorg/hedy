import { loginForTeacher } from "../tools/login/login";
import { goToTeachersPage } from "../tools/navigation/nav";

const feedback_options = ['bug', 'feature', 'feedback']

describe("Test the feedback feature", () => {
    beforeEach(() => {
        loginForTeacher();
        goToTeachersPage();
    })

    feedback_options.forEach((feedback) => {
        it(`Is able to submit ${feedback}`, () => {
            cy.intercept({
                method: "POST",
                url: "/feedback",
            }).as("postFeedback")
        
            cy.getDataCy('feedback_button').click()
            cy.getDataCy('modal_feedback_input').type(`I'm writing: ${feedback}`)
            cy.getDataCy(feedback).click()
            cy.getDataCy('modal_feedback_submit').click()
            cy.getDataCy('modal_feedback_input').should("not.be.visible")
        
            cy.wait("@postFeedback").should('have.nested.property', 'response.statusCode', 200)
        });
    })

    it("Is able to cancel feedback modal", () => {
        cy.getDataCy('feedback_button').click()
        cy.getDataCy('modal_feedback_cancel').click()
        cy.getDataCy('modal_feedback_input').should("not.be.visible")
    });
});