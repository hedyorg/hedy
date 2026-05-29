import { goToAdventurePage } from "../tools/navigation/nav";
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
  });
})
describe('The raw program page', () => {
  beforeEach(() => {
    cy.visit('/adventure/story/1/raw');
  });
});
