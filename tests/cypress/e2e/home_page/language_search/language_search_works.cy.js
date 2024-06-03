import { goToHome } from "../../tools/navigation/nav";

describe('Language search work', () => {
  it('passes', () => {
    goToHome();
    cy.get('.dropdown > .menubar-text').click();
    cy.get('#search_language').type('Deutsch');    
    cy.get('.language').contains('Deutsch');

    cy.get('#search_language').clear().type('Fran');    
    cy.get('.language').contains('Français');
  })
})
