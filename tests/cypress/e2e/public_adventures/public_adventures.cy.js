
import { loginForTeacher } from "../tools/login/login";

describe("Able to browse all public adventures and use filters", () => {
    beforeEach(() => {
        loginForTeacher();
        cy.getDataCy('public_adventures_link').click()
    });

    it("should have the language of the user as the default", () => {
        // This relies on teacher1 having 'en' as a language
        cy.get("#language_select").should('have.value', 'en')
    })

    it("should be able to filter by levels", () => {
        // The language of the user is preselected, so there should be 'en' adventures only
        // Adventure1 and adventure4 should be displayed
        cy.getDataCy('search-results').should("contain.text", "adventure1")
        cy.getDataCy('search-results').should("contain.text", "adventure4")

        cy.getDataCy('level_select').select('2')

        // For level 2 only adventure1 should be displayed
        cy.getDataCy('search-results').should("contain.text", "adventure1")
        cy.getDataCy('search-results').should("not.contain.text", "adventure4")
    })

    it("should be able to filter by language", () => {
        cy.getDataCy('search-results').should("contain.text", "adventure1")
        cy.getDataCy('search-results').should("contain.text", "adventure4")
        cy.getDataCy('search-results').should("not.contain.text", "adventure2")

        cy.getDataCy('language_select').select('Nederlands')

        cy.getDataCy('search-results').should("not.contain.text", "adventure1")
        cy.getDataCy('search-results').should("not.contain.text", "adventure4")
        cy.getDataCy('search-results').should("contain.text", "adventure2")
    })

    it("should be able to filter by tags", () => {
        cy.getDataCy('search-results').should("contain.text", "adventure1")
        cy.getDataCy('search-results').should("contain.text", "adventure4")

        // Apply a tag filter
        cy.get("#tag_select").select('test')

        cy.getDataCy('search-results').should("contain.text", "adventure1")
        cy.getDataCy('search-results').should("not.contain.text", "adventure4")
    })

    it("should be able to filter by searching", () => {
        cy.getDataCy('search-results').should("contain.text", "adventure1")
        cy.getDataCy('search-results').should("contain.text", "adventure4")

        cy.getDataCy('search_adventure').type("adventure4")

        cy.getDataCy('search-results').should("contain.text", "adventure4")
        cy.getDataCy('search-results').should("not.contain.text", "adventure1")
    })

    it("should be able to clone another teacher's adventure", () => {
        cy.getDataCy('search-results').should("contain.text", "adventure1")
        cy.getDataCy('search-results').should("contain.text", "adventure4")

        cy.getDataCy("search-results").contains("adventure4").click();

        cy.getDataCy("clone_adventure4").should("be.visible")
        cy.getDataCy("clone_adventure4").click()

        cy.contains("Go to your clone").click()

        // This brings you to the edit page where the title input element contains "adventure4"
        cy.getDataCy("custom_adventure_name").should("have.value", "adventure4")
    })
});
