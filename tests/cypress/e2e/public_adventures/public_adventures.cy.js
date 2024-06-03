
import { loginForTeacher } from "../tools/login/login";

describe("Able to browse all public adventures and use filters", () => {
    beforeEach(() => {
        loginForTeacher();
        cy.get("#public-adventures-link").click()
    });

    it("should have level 1 as the default one", () => {
        cy.get("#level-select").should('have.attr', 'data-value', '1')
    })

    it("should have language en as the default one", () => {
        cy.get("#language-select").should('have.attr', 'data-value', 'en')
    })

    it("should be able to filter by levels", () => {
        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("not.contain.text", "adventure3")
        // disselect default language
        resetLang()

        cy.get("#level-select")
            .click()

        cy.get('#level_dropdown').should('be.visible');
        cy.get("#level_dropdown .option[data-value='2']")
            .click()

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("contain.text", "adventure3")
    })

    it("should be able to filter by language", () => {
        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("not.contain.text", "adventure2")
        // by default en is selected.
        cy.get("#language-select")
            .click()

        cy.get('#lang_dropdown').should('be.visible');

        cy.get("#lang_dropdown .option[data-value='nl']")
            .click()

        cy.get("#adventures").should("not.contain.text", "adventure1")
        cy.get("#adventures").should("contain.text", "adventure2")
    })

    it("should be able to filter by tags", () => {
        // disselect default language
        resetLang()

        cy.get("#tag-select")
            .click()
        cy.get('#tags_dropdown').should('be.visible');

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("contain.text", "adventure2")
        cy.get("#tags_dropdown .option[data-value='test']")
            .click()

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("not.contain.text", "adventure2")
    })

    it("should be able to filter by searching", () => {
        // disselect default language
        resetLang()

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("contain.text", "adventure2")

        cy.get('#search_adventure')
            .type("adventure2")

        cy.get("#adventures").should("contain.text", "adventure2")
        cy.get("#adventures").should("not.contain.text", "adventure1")
    })

    it("should be able to clone another teacher's adventure", () => {
        // disselect default language
        resetLang()

        cy.getDataCy("adventure2")
            .click()

        cy.getDataCy("adventure2").should("have.class", "tab-selected")
        cy.getDataCy("adventure1").should("not.have.class", "tab-selected")

        cy.getDataCy("clone_adventure2")
            .should("be.visible")
            .click()

        cy.reload()
        resetLang()
        cy.getDataCy("adventure2")
            .click()
        cy.getDataCy("edit_adventure2").should("be.visible")
    })
});

function resetLang() {
    // disselect default language
    cy.get("#language-select")
        .click()
    cy.get("#lang_dropdown .option[data-value='']")
        .click()
}