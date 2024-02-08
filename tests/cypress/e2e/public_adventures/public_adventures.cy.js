
import { loginForTeacher } from "../tools/login/login";

describe("Able to browse all public adventures and use filters", () => {
    beforeEach(() => {
        loginForTeacher();
        cy.get("#public-adventures-link").click()
    });

    it("should have level 1 as the default one", () => {
        cy.get("#level-select").should('have.attr', 'data-value', '1')
    })

    it("should be able to filter by levels", () => {
        cy.get("#level-select")
            .click()

        cy.get('#level_dropdown').should('be.visible');

        cy.get("#level_dropdown .option[data-value='2']")
            .click()

        cy.reload()
        cy.url().should("include", "level=2")
    })

    it("should be able to filter by language", () => {
        cy.get("#language-select")
            .click()

        cy.get('#lang_dropdown').should('be.visible');

        cy.get("#lang_dropdown .option[data-value='en']")
            .click()

        cy.reload()
        cy.url().should("include", "lang=en")
    })

    it("should be able to filter by tags", () => {
        cy.get("#tag-select")
            .click()

        cy.get('#tags_dropdown').should('be.visible');

        cy.get("#tags_dropdown .option[data-value='test']")
            .click()

        cy.reload()
        cy.url().should("include", "tag=test")
    })

    it("should be able to filter by searching", () => {
        cy.get('#search_adventure')
            .type("adven")

        cy.wait(500) // due to the debouncing attached on the input.
        cy.reload()
        cy.url().should("include", "search=adven")

        cy.get('#adventure1').should('be.visible');

    })
});