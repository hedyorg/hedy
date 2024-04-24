import {goToHedyPage} from "../tools/navigation/nav";

describe('Is able to use try pre formatted code', () => {
    it('The cheatsheet code is added to the end of the editor', () => {
      goToHedyPage();
      cy.get('#editor > .cm-editor > .cm-scroller > .cm-content').clear()
      cy.get('#editor > .cm-editor > .cm-scroller > .cm-content').type('print hello world')
      
      cy.get('#dropdown_cheatsheet_button').click();
      cy.get('#cheatsheet_dropdown').should('be.visible');

      cy.get('#try_button2').click();

      cy.get('#editor .cm-line').each((element, index) => {
        // the code should've been added to the second line
        if (index == 0) {
          cy.get(element).should('contain', 'print hello world')
        } else if(index == 1) {
          cy.get(element).should('contain', 'ask');
        }
      })
    })
  })