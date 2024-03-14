

import { goToHome } from "../../tools/navigation/nav";

describe('Try it button', () => {
  it('passes', () => {
    goToHome();
    cy.get('#try_learning_button').should("be.not.disabled").should("be.visible");
    cy.get('#try_teaching_button').should("be.not.disabled").should("be.visible");
  })
})
