import { goToHome } from "../../tools/navigation/nav";

describe('Language search exists', () => {
  it('passes', () => {
    goToHome();
    cy.get('.dropdown > .menubar-text').click();
    cy.get('#search_language').should('be.enabled')
    .should('be.visible')    
  })
})
