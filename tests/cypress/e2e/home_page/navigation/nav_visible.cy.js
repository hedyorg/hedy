import { goToHome } from "../../tools/navigation/nav";

describe('Language choice button', () => {
  it('passes', () => {
    goToHome();
    cy.get('#hedybutton').should('be.visible').should('be.not.disabled');
    cy.get('#explorebutton').should('be.visible').should('be.not.disabled');
    cy.get('#learnmorebutton').should('be.visible').should('be.not.disabled');
    


  })
})
