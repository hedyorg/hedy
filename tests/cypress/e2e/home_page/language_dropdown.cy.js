import { goToHome } from "../tools/navigation/nav";

it('Is able to search a language, see all languages and add a language', () => {
  goToHome();
  cy.getDataCy('language_dropdown_button').click();
  cy.getDataCy('language_dropdown').should('be.visible');

  // test if searching for a language works
  cy.getDataCy('search_language').type('Ger');
  cy.get('.language').contains('Deutsch');

  cy.getDataCy('search_language').clear().type('Fran');    
  cy.get('.language').contains('Français');
  cy.getDataCy('search_language').clear()

  // test if all buttons are present
  cy.get('.language').each(($el) => {
    cy.wrap($el).scrollIntoView({ easing: 'linear', duration: 100 })
    .should('be.visible')
    .should('be.not.empty')
    .should('be.not.disabled');
  })

  // test if adding a language button works
  cy.getDataCy('add_language_btn').should('be.visible');
  })