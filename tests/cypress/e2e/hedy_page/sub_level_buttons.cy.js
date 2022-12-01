import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to go to different sublevels', () => {
    it('Passes', () => {
      goToHedyPage();

      cy.get('.adventure1').click();
      cy.get('[data-tab="default"]').should('be.visible'); // The first tab shouldn't show tab-selected anymore
    })
  })