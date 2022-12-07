

  import { goToHome } from "../../tools/navigation/nav";

describe('Try it button', () => {
  it('passes', () => {
    goToHome();
    cy.get('#main_page_content > .mx-auto').should('be.not.disabled').should('be.visible');
  
  })});
