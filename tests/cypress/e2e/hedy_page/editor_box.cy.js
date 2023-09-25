const YAML = require('js-yaml')

describe('Is able to type in the editor box', () => {
  const LANGUAGES_TO_TEST = ['en', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de','el', 'eo', 'es', 'et', 'fa', 'fi', 'fr', 'fy', 'he', 'hi', 'hu', 'id', 'it', 'ja', 'kmr', 'ko', 'nb_NO', 'nl', 'pa_PK', 'pl', 'pt_BR', 'pt_PT', 'ro', 'ru', 'sq', 'sr', 'sv', 'sw', 'te', 'th']

  // Do something for every language
  for (const language of LANGUAGES_TO_TEST) {

    it(`Language ${language} should run`, () => {
      cy.visit(`${Cypress.env('hedy_page')}?language=${language}#default`);

      // click on textaread to get focus, then clear it
      aceContent().click();
      clearViaBackspace();

      cy.focused().type('print Hello world');
      aceContent().should('have.text', 'print Hello world');
      cy.get('#runit').click();
      cy.get('#output').should('contain.text', 'Hello world');
    });
  }
});

describe('Test editor box functionality', () => {
  beforeEach(() => {
    cy.visit(`${Cypress.env('hedy_page')}#default`);

    aceContent().click();
    clearViaBackspace();
  });

  it('Ask modal should hold input and the answer should be shown in output', () => {
    cy.focused().type('print Hello world\nask Hello!\necho');
    aceContent().should('have.text', 'print Hello worldask Hello!echo');
    cy.get('#runit').click();
    cy.get('#output').should('contain.text', 'Hello world');
    cy.get('#ask-modal').should('be.visible');
    cy.get('#ask-modal > form > div > input[type="text"]').type('Hedy!');
    cy.get('#ask-modal > form > div > input[type="submit"]').click();
    cy.get('#output').should('contain.text', 'Hedy!');
  });

  it('Ask modal shpuld be shown even when editing the program after clicking run and not answering the modal', () => {
    // First we write and run the program and leave the ask modal unanswered
    cy.focused().type('print Hello world\nask Hello!');
    // the \n is not shown as a charecter when you get the text
    aceContent().should('have.text', 'print Hello worldask Hello!');
    cy.get('#runit').click();
    cy.get('#output').should('contain.text', 'Hello world');
    cy.get('#ask-modal').should('be.visible');

    // Now we edit the program and the ask modal should be hidden
    aceContent().click();
    // TODO: replace this wait. The editor takes a while to be focused
    cy.wait(500)

    clearViaBackspace();
    cy.focused().type('print Hello world\nask Hello!');
    aceContent().should('have.text', 'print Hello worldask Hello!');
    cy.get('#ask-modal').should('not.be.visible');

    // Running program again and it should show the modal
    cy.get('#runit').click();
    cy.get('#output').should('contain.text', 'Hello world');
    cy.get('#ask-modal').should('be.visible');
  });

  it ('When making an error the error modal should be shown', () => {
    cy.focused().type('echo');
    aceContent().should('have.text', 'echo');
    cy.get('#runit').click();

    cy.get('#errorbox').should('be.visible');
    // The error should be about the lonely echo
    cy.getBySel('error_details').should('contain.text', 'echo');
  });

  it ('When making an error the keywords must be highligted', () => {
    cy.focused().type('prin Hello world');
    aceContent().should('have.text', 'prin Hello world');
    cy.get('#runit').click();

    cy.get('#errorbox').should('be.visible');
    // The error should be about the lonely echo
    cy.getBySel('error_details').should('contain.text', 'prin');
    cy.get('[data-cy="error_details"] span').should('have.class', 'command-highlighted');

  });
});

/**
 * Clear the input via sending a whole bunch of {backspace} keystrokes
 *
 * We tried all kinds of `.clear()` invocations, all of them worked on our
 * desktops and never on GitHub Actions. The current invocation does
 * seem to work consistently on GHA, and we collectively have no idea
 * why ¯\_(ツ)_/¯.
 */
function clearViaBackspace() {
  cy.focused().type('{moveToEnd}' + '{backspace}'.repeat(40));
  aceContent().should('have.text', '');
}

function aceContent() {
  return cy.get('#editor > .ace_scroller > .ace_content');
}