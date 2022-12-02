import { goToHome } from "../../tools/navigation/nav";

describe('Explore nav button', () => {
  it('passes', () => {
    goToHome();
    cy.get('#explorebutton').should('be.visible').should('be.not.disabled').click();
    cy.wait(500);
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/login");
    })
   


  })
})
