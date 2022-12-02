
import { goToHome } from "../../tools/navigation/nav";

describe('Hedy nav works', () => {
  it('passes', () => {
    goToHome();
    cy.get('#hedybutton').should('be.visible').should('be.not.disabled').click();
    cy.wait(500);
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/hedy");
    })
   


  })
})
