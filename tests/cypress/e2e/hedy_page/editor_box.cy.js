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

describe('Test editor box functionality', () => {
  beforeEach(() => {
    cy.visit(`${Cypress.env('hedy_page')}#default`);
    // click on textaread to get focus
    cy.get('#editor > .ace_scroller > .ace_content').click();
    // empty textarea
    cy.focused().clear();
  });
  
  it('Ask modal should hold input and the answer should be shown in output', () => {
    cy.get('#editor').type('print Hello world\nask Hello!\necho');
    cy.get('#editor > .ace_scroller > .ace_content').should('contain.text', 'print Hello worldask Hello!echo');
    cy.get('#runit').click();
    cy.get('#output').should('contain.text', 'Hello world');
    cy.get('#ask-modal').should('be.visible');
    cy.get('#ask-modal > form > div > input[type="text"]').type('Hedy!');      
    cy.get('#ask-modal > form > div > input[type="submit"]').click();
    cy.get('#output').should('contain.text', 'Hedy!');
  });

  it('Ask modal shpuld be shown even when editing the program after clicking run and not answering the modal', () => {
    // First we write and run the program and leave the ask modal unanswered
    cy.get('#editor').type('print Hello world\nask Hello!');
    // the \n is not shown as a charecter when you get the text
    cy.get('#editor > .ace_scroller > .ace_content').should('contain.text', 'print Hello worldask Hello!');
    cy.get('#runit').click();
    cy.get('#output').should('contain.text', 'Hello world');
    cy.get('#ask-modal').should('be.visible');

    // Now we edit the program and the ask modal should be hidden
    cy.get('#editor > .ace_scroller > .ace_content').click();
    cy.focused().clear();
    cy.get('#editor').type('print Hello world\nask Hello!');
    cy.get('#ask-modal').should('not.be.visible');

    // Running program again and it should show the modal
    cy.get('#runit').click();
    cy.get('#output').should('contain.text', 'Hello world');
    cy.get('#ask-modal').should('be.visible');
  });
});