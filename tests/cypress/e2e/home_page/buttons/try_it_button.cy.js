

import { goToHome } from "../../tools/navigation/nav";

describe('Try it button', () => {
  it('passes', () => {
    goToHome();
    cy.get('.py-8 > :nth-child(2) > .green-btn').should("be.not.disabled").should("be.visible");
  })
})
