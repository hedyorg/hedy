
import { loginForTeacher } from "../tools/login/login";

describe("Able to browse all public adventures and use filters", () => {
    beforeEach(() => {
        loginForTeacher();
        cy.getDataCy('public_adventures_link').click()
    });

    it("should have level 1 as the default one", () => {
        cy.get("#level_select > div > div > div.option.selected").should('have.attr', 'data-value', '1')
    })

    it("should have the language of the user as the default", () => {
        cy.get("#language_select > div > div > div.option.selected").should('have.attr', 'data-value', 'English')
    })

    it("should be able to filter by levels", () => {
        cy.getDataCy('level_select').click()

        cy.get('#level_select > div > div.dropdown-menu').should('be.visible');

        // The language of the user is preselected, so there should be 'en' adventures only
        // So, for level 1 adventure1 and adventure4 should be displayed
        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("contain.text", "adventure4")

        cy.get("#level_select > div > div > div.option[data-value='2']")
            .click()

        // For level 2 only adventure1 should be displayed
        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("not.contain.text", "adventure4")
    })

    it("should be able to filter by language", () => {
        cy.getDataCy('language_select').click()

        cy.get('#language_select > div > div.dropdown-menu').should('be.visible');

        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("contain.text", "adventure4")
        cy.getDataCy('adventures').should("not.contain.text", "adventure2")

        cy.get("#language_select > div > div > div.option[data-value='Nederlands']")
            .click()

        cy.getDataCy('adventures').should("not.contain.text", "adventure1")
        cy.getDataCy('adventures').should("not.contain.text", "adventure4")
        cy.getDataCy('adventures').should("contain.text", "adventure2")
    })

    it("removing the language filter should display adventures without a language", () => {
        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("contain.text", "adventure4")
        cy.getDataCy('adventures').should("not.contain.text", "language-less")

        cy.getDataCy('language_select').click()
        cy.get('#language_select > div > div.dropdown-menu').should('be.visible');
        cy.get("#language_select > div > div > div.option[data-value='']").click()

        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("contain.text", "adventure4")
        cy.getDataCy('adventures').should("contain.text", "adventure2")
    })

    it("should be able to filter by tags", () => {
        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("contain.text", "adventure4")

        // Apply a tag filter
        cy.getDataCy('tag_select').click()
        cy.get('#tag_select > div > div.dropdown-menu').should('be.visible');
        cy.get("#tag_select > div > div.dropdown-menu > .option[data-value='test']").click()

        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("not.contain.text", "adventure4")
    })

    it("should be able to filter by searching", () => {
        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("contain.text", "adventure4")

        cy.getDataCy('search_adventure').type("adventure4")

        cy.getDataCy('adventures').should("contain.text", "adventure4")
        cy.getDataCy('adventures').should("not.contain.text", "adventure1")
    })

    it("should be able to clone another teacher's adventure", () => {
        cy.getDataCy('adventures').should("contain.text", "adventure1")
        cy.getDataCy('adventures').should("contain.text", "adventure4")

        cy.getDataCy("adventure1").should("have.class", "tab-selected")
        cy.getDataCy("adventure4").click()

        cy.getDataCy("adventure4").should("have.class", "tab-selected")
        cy.getDataCy("adventure1").should("not.have.class", "tab-selected")

        cy.getDataCy("clone_adventure4").should("be.visible")
        cy.getDataCy("clone_adventure4").click()

        cy.getDataCy("edit_adventure4").should("be.visible")
    })
});
