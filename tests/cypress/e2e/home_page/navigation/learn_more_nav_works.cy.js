
import { goToHome } from "../../tools/navigation/nav";

describe('Learn more nav button', () => {
  it('passes', () => {
    goToHome();
    cy.get('#learnmorebutton').click();
    cy.wait(500);
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/learn-more");
    })
   


  })
})
