import { goToHome } from "../../tools/navigation/nav";

describe('Explore nav button', () => {
  it('passes', () => {
    goToHome();
    cy.get('#explorebutton').click();
    cy.wait(500);
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/login");
    })
   


  })
})
