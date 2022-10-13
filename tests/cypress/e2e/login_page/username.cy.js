describe('Field interaction test', () => {
  it('passes', () => {
    cy.visit(Cypress.env('login_page'))

    // Tests username field interaction
    cy.get('#username')
      .should('be.visible')
      .should('be.empty')
      .should('have.attr', 'minlength', '3')
      .type('some_username\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_username\"!#@\'( )*$%\'123\"')

    // Tests password field interaction
    cy.get('#password')
      .should('be.visible')
      .should('be.empty')
      .should('have.attr', 'minlength', '6')
      .should('have.attr', 'type', 'password')
      .type('some_password\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_password\"!#@\'( )*$%\'123\"')
  })
})