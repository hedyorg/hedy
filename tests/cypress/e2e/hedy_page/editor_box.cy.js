const YAML = require('js-yaml')

describe('Is able to type in the editor box', () => {
  const LANGUAGES_TO_TEST = ['en', 'nl', 'fr'];

  // Do something for every language
  for (const language of LANGUAGES_TO_TEST) {

    it(`in ${language}`, () => {
      cy.visit(`${Cypress.env('hedy_page')}?language=${language}`);

      // click on textaread to get focus
      cy.get('#editor > .ace_scroller > .ace_content').click();
      // empty textarea
      cy.focused().clear()
      cy.get('#editor').type('print Hello world');
      cy.get('#editor > .ace_scroller > .ace_content').should('contain.text', 'print Hello world');
      cy.get('#runit').click();
      cy.get('#output').should('contain.text', 'Hello world');
    });
  }
});