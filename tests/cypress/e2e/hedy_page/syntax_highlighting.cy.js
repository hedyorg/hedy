import { loginForUser } from "../tools/login/login";
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
});

describe('The view program page', () => {
  let programName;
  beforeEach(async () => {
    loginForUser();
    goToHedyPage();
    programName = Math.random().toString(36);
    cy.get('#program_name').clear().type(programName);
    cy.get('#share_program_button').click();
    cy.get('#modal-copy-button').click();

    const urlFromClipboard = await new Promise((ok) =>
      cy.window().then((win) =>
        win.navigator.clipboard.readText().then(ok)));

    cy.visit(urlFromClipboard);
  });

  it('has syntax highlighting', () => {
    cy.get('#editor')
      .contains('print')
      .should('be.visible')
      .and('have.class', 'ace_keyword');
  })
})
