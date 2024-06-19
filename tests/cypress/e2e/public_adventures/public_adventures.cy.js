
import { loginForTeacher } from "../tools/login/login";

describe("Able to browse all public adventures and use filters", () => {
    beforeEach(() => {
        loginForTeacher();
        cy.get("#public_adventures_link").click()
    });

    it("should have level 1 as the default one", () => {
        cy.get("#level_select > div > div > div.option.selected").should('have.attr', 'data-value', '1')
    })

    it("should be able to filter by levels", () => {
        cy.getDataCy('level_select')
            .click()

        cy.get('#level_select > div > div.dropdown-menu').should('be.visible');

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("contain.text", "adventure2")
        cy.get("#level_select > div > div > div.option[data-value='2']")
            .click()

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("not.contain.text", "adventure2")
    })

    it("should be able to filter by language", () => {
        cy.get("#language_select")
            .click()

        cy.get('#language_select > div > div.dropdown-menu').should('be.visible');

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("contain.text", "adventure2")
        cy.get("#language_select > div > div > div.option[data-value='English']")
            .click()

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("not.contain.text", "adventure2")
    })

    it("should be able to filter by tags", () => {
        cy.get("#tag_select")
            .click()

        cy.get('#tag_select > div > div.dropdown-menu').should('be.visible');

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("contain.text", "adventure2")
        cy.get("#tag_select > div > div.dropdown-menu > .option[data-value='test']")
            .click()

        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("not.contain.text", "adventure2")
    })

    it("should be able to filter by searching", () => {
        cy.get("#adventures").should("contain.text", "adventure1")
        cy.get("#adventures").should("contain.text", "adventure2")

        cy.get('#search_adventure')
            .type("adventure2")

        cy.get("#adventures").should("contain.text", "adventure2")
        cy.get("#adventures").should("not.contain.text", "adventure1")
    })

    it("should be able to clone another teacher's adventure", () => {
        cy.getDataCy("adventure1").should("have.class", "tab-selected")
        cy.getDataCy("adventure2")
            .click()

        cy.getDataCy("adventure2").should("have.class", "tab-selected")
        cy.getDataCy("adventure1").should("not.have.class", "tab-selected")

        cy.getDataCy("clone_adventure2")
            .should("be.visible")
            .click()

        cy.reload()
        cy.getDataCy("adventure2")
            .click()
        cy.getDataCy("edit_adventure2").should("be.visible")
    })
});