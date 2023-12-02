import {loginForTeacher} from "../../tools/login/login.js"
import {goToEditAdventure} from "../../tools/navigation/nav.js"

describe("Tags of adventures", () => {
  beforeEach(() => {
    loginForTeacher();
    goToEditAdventure();
  })

  it("has tags input and button", () => {
    cy.get("#search_tags_input")
      .should("be.visible")
      .should("be.empty")

    cy.get("#add_adventure_tags")
      .should("be.visible")
  })

  it("has no tags initially", () => {
    cy.get("#tags-list")
      .should("be.not.visible")
  })

  it("adds a tag to adventure by pressing enter within the input field", () => {
    cy.get("#search_tags_input")
      .should("be.empty")
      .type("statements{enter}")
    cy.wait(500)
    cy.get("#tags-list")
      .should("be.visible")

    cy.get("#tags-list li")
      .should("include.text", "statements")
  })

  it("adds a tag to adventure by pressing the add button", () => {
    cy.get("#search_tags_input")
      .should("be.empty")
      .type("training")
    cy.get("#add_adventure_tags")
      .should("be.visible")
      .click()
    cy.wait(500)
    cy.get("#tags-list")
      .should("be.visible")

    cy.get("#tags-list li")
      .should("include.text", "training")
  })

  it("declines adding duplicate", () => {
    cy.intercept({
      method: "POST",
      url: "*",
      times: 1,
    }).as("createTag")

    cy.get("#search_tags_input")
      .should("be.empty")
      .type("training{enter}")
    cy.wait("@createTag").should('have.nested.property', 'response.statusCode', 400)
    cy.get("#tags-list li")
      .should("include.text", "training")
  })

  it("remvoes a tag", () => {
    cy.intercept({
      method: "DELETE",
      url: "*",
      times: 1,
    }).as("deleteTag")

    cy.wait(500)
    cy.get("#tag_1")
      .should("be.visible")
      .should("include.text", "statements")
    cy.get("#tag_1 .fa-circle-xmark")
      .click()
    cy.wait("@deleteTag").should('have.nested.property', 'response.statusCode', 200)
    cy.get("#tags-list li")
      .should("not.include.text", "statements")
  })

})
