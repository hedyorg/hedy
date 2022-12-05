import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to use try pre formatted code', () => {
    it('Passes', () => {
      goToHedyPage();

      cy.get('#dropdown_cheatsheet_button').click();
      cy.get('#cheatsheet_dropdown').should('be.visible');

      cy.get('#try_button2').click();

      cy.get('#editor > .ace_scroller > .ace_content .ace_line').each((element, index) => {
        if(index == 0) {
          cy.get(element).should('contain', 'ask');
        }
      })
    })
  })