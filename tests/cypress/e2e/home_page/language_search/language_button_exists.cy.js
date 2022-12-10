import { goToHome } from "../../tools/navigation/nav";

describe('Language choice button', () => {
  it('passes', () => {
    goToHome();
    cy.get('.dropdown > .menubar-text').should('be.visible').click();
  })
})
