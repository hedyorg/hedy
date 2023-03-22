import { goToHedyPage } from "../tools/navigation/nav";

describe('the hedy page', () => {
  beforeEach(() => {
    goToHedyPage();
  });

  it('has a dropdown to pick speech language', () => {
    cy.get('#speak_dropdown').should('be.visible');
  });
});