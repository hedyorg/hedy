import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to go to different sublevels', () => {
    it('Passes', () => {
      goToHedyPage();

      cy.get('#adventure1').should('have.class', 'tab-selected');
      cy.get('#adventure2').click();
      cy.get('#adventure2').should('have.class', 'tab-selected');
      cy.get('#adventure1').should('not.have.class', 'tab-selected');
    })
  })