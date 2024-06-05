import {loginForTeacher} from "../../tools/login/login.js"
import {goToEditAdventure} from "../../tools/navigation/nav.js"

describe("Tags of adventures", () => {
  beforeEach(() => {
    loginForTeacher();
    goToEditAdventure();
  })

  it("has tags input and button", () => {
    cy.getDataCy('search_tags_input')
      .should("be.visible")
      .should("be.empty")

    cy.getDataCy('add_adventure_tags')
      .should("be.visible")
  })

  it("adds a tag to adventure by pressing enter within the input field", () => {
    cy.getDataCy('search_tags_input')
      .should("be.empty")
      .type("statements{enter}")
    cy.wait(500)
    cy.getDataCy('tags_list')
      .should("be.visible")

    cy.get("#tags_list li")
      .should("include.text", "statements")
  })

  it("adds a tag to adventure by pressing the add button", () => {
    cy.getDataCy('search_tags_input')
      .should("be.empty")
      .type("training")
    cy.getDataCy('add_adventure_tags')
      .should("be.visible")
      .click()
    cy.wait(500)
    cy.getDataCy('tags_list')
      .should("be.visible")

    cy.get("#tags_list li")
      .should("include.text", "training")
  })

  it("declines adding duplicate", () => {
    cy.intercept({
      method: "POST",
      url: "*",
      times: 1,
    }).as("createTag")

    cy.getDataCy('search_tags_input')
      .should("be.empty")
      .type("training{enter}")
    cy.wait("@createTag").should('have.nested.property', 'response.statusCode', 400)
    cy.get("#tags_list li")
      .should("include.text", "training")
  })

  it("removes a tag", () => {
    cy.intercept({
      method: "DELETE",
      url: "*",
      times: 1,
    }).as("deleteTag")

    cy.wait(500)
    cy.getDataCy('tag_2')
      .should("be.visible")
      .should("include.text", "statements")
    cy.get("#tag_2 .fa-circle-xmark")
      .click()
    cy.wait("@deleteTag").should('have.nested.property', 'response.statusCode', 200)
    cy.get("#tags_list li")
      .should("not.include.text", "statements")
  })

})
