const YAML = require('js-yaml')

describe('Is able to type in the editor box', () => {
  const LANGUAGES_TO_TEST = ['en', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de','el', 'eo', 'es', 'et', 'fa', 'fi', 'fr', 'fy', 'he', 'hi', 'hu', 'id', 'it', 'ja', 'kmr', 'ko', 'nb_NO', 'nl', 'pa_PK', 'pl', 'pt_BR', 'pt_PT', 'ro', 'ru', 'sq', 'sr', 'sv', 'sw', 'te', 'th']

  // Do something for every language
  for (const language of LANGUAGES_TO_TEST) {

    it(`Language ${language} should run`, () => {
      cy.visit(`${Cypress.env('hedy_page')}?language=${language}#default`);

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
