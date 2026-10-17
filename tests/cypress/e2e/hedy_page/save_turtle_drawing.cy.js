import { goToHedyPage } from "../tools/navigation/nav";
import { codeEditorContent } from "../tools/programs/program";

describe('Save turtle drawing button', () => {
  beforeEach(() => {
    goToHedyPage();
    codeEditorContent().clear();
    codeEditorContent().type('color red\nforward 100\nturn right\nforward 50');
    cy.get('#runit').click();
    cy.get('#turtlecanvas').should('be.visible');
  });

  it('Downloads the machine files of a turtle program', () => {
    cy.intercept('POST', '/generate_machine_files').as('generate');

    cy.get('#saveFiles').should('be.visible').click();

    cy.wait('@generate').its('response.statusCode').should('eq', 200);
    cy.readFile(`${Cypress.config('downloadsFolder')}/hedy_drawing.zip`, 'binary', { timeout: 15000 })
      .should('have.length.greaterThan', 0);
  });

  it('Shows an error when the drawing can not be generated', () => {
    cy.intercept('POST', '/generate_machine_files', {
      statusCode: 400,
      body: { error: 'There was an error, please try again.' },
    }).as('generate');

    cy.get('#saveFiles').should('be.visible').click();

    cy.wait('@generate');
    cy.getDataCy('modal_alert_text')
      .should('be.visible')
      .should('contain.text', 'There was an error, please try again.');
  });
});
