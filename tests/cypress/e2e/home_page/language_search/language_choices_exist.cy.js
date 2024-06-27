import { goToHome } from "../../tools/navigation/nav";

describe('Language choice button', () => {
  it('passes', () => {
    goToHome();
    cy.get('.dropdown > .menubar-text').click();
    cy.get('#language_dropdown').should('be.visible');

    cy.get('.language').each(($el) => {
      cy.wrap($el).scrollIntoView({ easing: 'linear', duration: 100 })
      .should('be.visible')
      .should('be.not.empty')
      .should('be.not.disabled');
    })
  })
});