import { goToHome } from "../../tools/navigation/nav";

describe('Language choice button', () => {
  it('passes', () => {
    goToHome();
    cy.get('.dropdown > .menubar_text').should('be.visible').click();
  })
})
