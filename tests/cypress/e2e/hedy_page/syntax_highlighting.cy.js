import { goToHedyPage } from "../tools/navigation/nav";

describe('The Hedy level 1 page', () => {
  beforeEach(() => {
    goToHedyPage();
  });

  it('has the word print highlighted in examples', () => {
    cy.get('#adventures-tab pre')
      .contains('print')
      .should('be.visible')
      .and('have.class', 'ace_keyword');
  })

  it('has the word print highlighted in the editor', () => {
    cy.get('#editor')
      .contains('print')
      .should('be.visible')
      .and('have.class', 'ace_keyword');
  })
})
