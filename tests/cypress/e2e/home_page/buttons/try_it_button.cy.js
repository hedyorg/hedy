

import { goToHome } from "../../tools/navigation/nav";

describe('Try it button', () => {
  it('passes', () => {
    goToHome();
    cy.get('#tryitbutton').should("be.not.disabled").should("be.visible");
  })
})
