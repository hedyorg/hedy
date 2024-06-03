import { goToHome } from "../../tools/navigation/nav";

describe('Language choice button', () => {
  it('passes', () => {
    goToHome();
    cy.get('.dropdown > .menubar-text').click();

    cy.get('.language').each(($el) => {
      cy.wrap($el).should('be.visible').should('be.not.empty').should('be.not.disabled');
    })  
  })
});
