import { goToHedyPage } from "../tools/navigation/nav";

describe('the hedy page', () => {
  beforeEach(() => {
    goToHedyPage();
  });

  it('has a dropdown to pick speech language', () => {
    cy.getDataCy('read_outloud').should('be.visible');
  });
});