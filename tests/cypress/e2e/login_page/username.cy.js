import {goToLogin} from '../tools/navigation/nav.js'

describe('Login form test', () => {
  it('passes', () => {
    goToLogin();

    // Tests username field interaction
    cy.get('#username')
      .get('#username')
      .should('be.visible')
      .should('be.empty')
      .should('have.attr', 'minlength', '3')
      .type('some_username\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_username\"!#@\'( )*$%\'123\"');

    // Tests password field interaction
     cy.get('#password')
      .should('be.visible')
      .should('be.empty')
      .should('have.attr', 'minlength', '6')
      .should('have.attr', 'type', 'password')
      .type('some_password\"!#@\'( )*$%\'123\"')
      .should('have.value', 'some_password\"!#@\'( )*$%\'123\"');

    // Tests invisibility of modal alert text
    cy.get('#modal_alert_text')
      .should('not.be.visible')
      .should('be.empty')

    // Tests button type and visualisation
    cy.get('button[class*="green-btn mt-2"]')
      .should('be.visible')
      .should('have.attr', 'type', 'submit')
      .should('have.text', 'Log in');

    // test visibility of modal alert text
    cy.get('button[class*="green-btn mt-2"]')
       .click()
    cy.get('#modal_alert_text')
      .should('be.visible')
      .should('have.text', 'Invalid username/password. No account?')


  })
})