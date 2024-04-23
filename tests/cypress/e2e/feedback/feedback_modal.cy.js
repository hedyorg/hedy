import { loginForTeacher } from "../tools/login/login";
import { goToHedyPage, goToTeachersPage, goToProfilePage } from "../tools/navigation/nav";

describe("Test the feedback feature", () => {
    beforeEach(() => {
        loginForTeacher();
    })
    it("should be able to open the modal", () => {
        goToHedyPage();
        cy.get('[data-cy="feedback_button"]')
            .should("be.visible")
            .click()
        
        cy.get('[data-cy="modal-feedback"]')
            .should("be.visible")
    });

    it("should not submit if the message or category is empty/not selected", () => {
        goToTeachersPage();

        cy.get('[data-cy="feedback_button"]')
            .should("be.visible")
            .click()
        
        cy.get('[data-cy="modal-feedback-input"]')
            .type("should not work without a category")

        
        cy.get('[data-cy="modal-feedback-input"]')
            .should("be.visible")
        
        cy.get('[data-cy="modal-feedback-cancel"]')
            .click()
            
        cy.get('[data-cy="modal-feedback-input"]')
            .should("not.be.visible")
    });

    it("should be able to submit a feedback", () => {
        cy.intercept({
            method: "POST",
            url: "/feedback",
            // times: 1,
        }).as("postFeedback")

        goToProfilePage();

        cy.get('[data-cy="feedback_button"]')
            .should("be.visible")
            .click()
        
        cy.get('[data-cy="modal-feedback-input"]')
            .type("This feature is wonderful! Thanks a lot for making it happen ;)")

        cy.get("#feedback")
            .click()

        cy.get('[data-cy="modal-feedback-submit"]')
            .click()
        
        cy.get('[data-cy="modal-feedback-input"]')
            .should("not.be.visible")

        cy.wait("@postFeedback").should('have.nested.property', 'response.statusCode', 200)
    });
});