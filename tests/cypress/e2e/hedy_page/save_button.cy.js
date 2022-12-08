import {goToHedyPage, goToHome} from "../tools/navigation/nav";
import {loginForStudent} from "../tools/login/login";

describe('Checks if save button works', () => {
    it('Passes', () => {
      loginForStudent();
      cy.get('#start_programming_button').click();

      // clear and type in editor 'print test'
      cy.get('textarea').clear({force: true})
      cy.get('#editor').type('print test');
      
      cy.get('#runit').click();
      cy.wait(3000);

      // the save button:
      cy.get('#save_program_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();
      
      // this is for if you already have saved your level once:
      if (cy.get('#modal-confirm')){
        cy.get('#modal-yes-button').click();
      }
      
      goToHome();
      goToHedyPage();

      // checks if it is correctly saved:
      cy.get('#editor > .ace_scroller > .ace_content .ace_line').each((element, index) => {
        if(index == 0) {
          cy.get(element).should('have.text', 'print test');
        }
      })
      
    })
  })