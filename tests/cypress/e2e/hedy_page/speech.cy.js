import { goToHedyPage } from "../tools/navigation/nav";

describe('the hedy page', () => {
  beforeEach(() => {
    goToHedyPage();
  });

  it('has a dropdown to pick speech language', () => {
    cy.get('#read_outloud').should('be.visible');
  });
});
