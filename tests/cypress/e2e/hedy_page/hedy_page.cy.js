import {goToHedyLevel2Page, goToHedyPage} from "../tools/navigation/nav";

describe('Tests for Hedy level page', () => {
  beforeEach(() => {
    goToHedyPage();
  })
  
  describe('when the user tries to use the Go Back to level x', () => {
    beforeEach(()=> {
      goToHedyLevel2Page();
    })
    
    it('goes back to the previous level if the code is unchaged', () => {      
      cy.get('#prev_level_button').click();
      // Should go back to previous URL
      cy.url().should('eq', Cypress.config('baseUrl') + Cypress.env('hedy_page') + '#default');
    })

    it('shows the confirm modal if the code was changed', () => {
      cy.get('#editor').type('hello');
      cy.get('#prev_level_button').click();
      cy.getBySel('modal-yes-button').click();
      cy.url().should('eq', Cypress.config('baseUrl') + Cypress.env('hedy_page') + '#default');
    })
  })
    
  it('Is able to type in the editor box', () => {
    cy.get('#editor > .ace_scroller > .ace_content').type('\nask What is your name\necho hello');
    cy.get('#editor > .ace_scroller > .ace_content .ace_line').each((element, index) => {
      if(index == 0) {
        cy.get(element).should('have.text', 'print hello world!');
      }
      if(index == 1) {
        cy.get(element).should('have.text', 'ask What is your name');
      }
      if(index == 2) {
        cy.get(element).should('have.text', 'echo hello');
      }
    })
  })

  describe('when the user changes their language to Arabic', () => {
    beforeEach(() => {
      cy.getBySel('language-dropdown').click();
      cy.getBySel('switch-lang-ar').click();
    });
  
    it('initially has keywords in Arabic', () => {
      cy.contains('.ace_keyword', 'قول').should('be.visible');
      cy.contains('.ace_keyword', 'print').should('not.exist');
    });
  
    it('the keyword language switcher at the top can switch keywords to English', () => {
      cy.getBySel('kwlang-switch-btn').click();
      cy.getBySel('kwlang-switch-toggle').click();
  
      cy.contains('.ace_keyword', 'قول').should('not.exist');
      cy.contains('.ace_keyword', 'print').should('be.visible');
    });
  })

  it('Is able to switch programmers mode on and of', () => {    
    cy.get('#toggle_circle').click(); // Programmers mode is switched on
    cy.get('#adventures-tab').should('not.be.visible');
  
    cy.get('#toggle_circle').click(); // Programmers mode is switched off
    cy.get('#adventures-tab').should('be.visible');
  })
  
  describe("When running code", () => {
    it("if the code is correct the code is executed", () => {
      cy.get('#editor > .ace_scroller > .ace_content')
        .type('\nprint Hello world!');
      
      cy.get('#runit').click();
      cy.get('#okbox').should('be.visible');

      cy.get('#output')
        .should('contain', 'Hello world!');    
    })
    
    it('incorrect code shouldnt run and should output error message', () => {      
      cy.get('#editor').type('\np');
      cy.get('#runit').click();
      cy.get('#errorbox').should('be.visible');
      cy.get('#output').should('be.empty');
    })
  })
  
  it('Is able to go to different sublevels', () => {
    cy.get('#adventure1').should('have.class', 'tab-selected');
    cy.get('#adventure2').click();
    cy.get('#adventure2').should('have.class', 'tab-selected');
    cy.get('#adventure1').should('not.have.class', 'tab-selected');
  })

  it('when clicking the yellow button code should be pasted into', () => {
    
    cy.get('#editor > .ace_scroller > .ace_content > .ace_layer > .ace_line > span')
      .then(($original_lines) => {
        cy.get('[data-cy=example-code-section] pre .yellow-btn')
          .filter(':visible')
          .first()
          .click();

        cy.get('#editor > .ace_scroller > .ace_content > .ace_layer > .ace_line > span')
          .should(($new_lines) => {
            expect($new_lines.text()).not.to.eq($original_lines.text());
          })
      })
  })
})
