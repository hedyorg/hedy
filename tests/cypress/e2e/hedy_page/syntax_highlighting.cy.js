import { loginForUser } from "../tools/login/login";
import { goToHedyPage, goToAdventurePage } from "../tools/navigation/nav";
import chaiColors from 'chai-colors'

// to know if the keywords do have the appropiate color
// cant check css classes in CodeMirror since it generates them automatically and have random names
chai.use(chaiColors)
context('chai-colors', () => {
  describe('The Hedy level 1 print adventure page', () => {
    beforeEach(() => {
      goToAdventurePage();
    });
  
    it('has the word print highlighted in examples', () => {
      cy.get('#adventures_tab pre .cm-editor')
        .eq(0)
        .contains('print')
        .should('be.visible')
        .should('have.css', 'color')
        .and('be.colored', '#ff6188')
  
    })

    it('highlights answer as a variable after ask in level 1', () => {
      cy.visit('/hedy/1?keyword_language=en');
      cy.get('#editor .cm-content').click();
      cy.focused().clear();
      cy.focused().type('ask what is your name{enter}print answer');

      cy.contains('#editor .cm-content .cm-highlight-var', 'answer')
        .should('be.visible')
        .should('have.css', 'color')
        .and('be.colored', '#c2e3ff')
    })

    it('highlights translated answer keyword after ask in level 1', () => {
      cy.visit('/hedy/1?language=es&keyword_language=es');
      cy.get('#editor .cm-content').click();
      cy.focused().clear();
      cy.focused().type('preguntar como te llamas{enter}imprimir respuesta');

      cy.contains('#editor .cm-content .cm-highlight-var', 'respuesta')
        .should('be.visible')
        .should('have.css', 'color')
        .and('be.colored', '#c2e3ff')
    })
  });
})
describe('The view program page', () => {
  let programName;
  beforeEach(async () => {
    loginForUser();
    goToHedyPage();
    programName = Math.random().toString(36);
    cy.get('#program_name').clear().type(programName);
    cy.get('#share_program_button').click();
    cy.get('#share_public').click();
    cy.get('button[data-action="copy_to_clipboard"]').click();

    const urlFromClipboard = await new Promise((ok) =>
      cy.window().then((win) =>
        win.navigator.clipboard.readText().then(ok)));

    cy.visit(urlFromClipboard);
  });
})

describe('The raw program page', () => {
  beforeEach(() => {
    cy.visit('/adventure/story/1/raw');
  });
});
