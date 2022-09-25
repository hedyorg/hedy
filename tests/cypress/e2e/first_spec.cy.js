describe("empty spec", () => {
  it("passes", () => {
    cy.visit(Cypress.env("base_url"));
  });
});
