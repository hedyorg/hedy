import { goToHedyPage } from "../tools/navigation/nav";
import { codeEditorContent } from "../tools/programs/program";

function runTurtleProgram(code) {
  codeEditorContent().clear();
  codeEditorContent().type(code);
  cy.get('#runit').click();
  cy.get('#saveFiles').should('be.visible');
}

describe('Save turtle drawing button', () => {
  beforeEach(() => {
    goToHedyPage();
    runTurtleProgram('color red\nforward 100\nturn right\nforward 50');
  });

  it('Downloads the machine files of a turtle program', () => {
    cy.intercept('POST', '/generate_machine_files').as('generate');

    cy.get('#saveFiles').click();

    cy.wait('@generate').its('response.statusCode').should('eq', 200);
    cy.readFile(`${Cypress.config('downloadsFolder')}/hedy_drawing.zip`, 'binary', { timeout: 15000 })
      .should('have.length.greaterThan', 0);
  });

  it('Sends the drawing of the last program that ran', () => {
    cy.intercept('POST', '/generate_machine_files').as('generate');

    cy.get('#saveFiles').click();
    cy.wait('@generate').its('request.body.points').then((firstDrawing) => {
      runTurtleProgram('forward 20\nturn left\nforward 30');
      cy.get('#saveFiles').click();
      cy.wait('@generate').its('request.body.points').should('not.deep.equal', firstDrawing);
    });
  });

  it('Shows an error when the drawing can not be generated', () => {
    cy.intercept('POST', '/generate_machine_files', {
      statusCode: 400,
      body: { error: 'There was an error, please try again.' },
    }).as('generate');

    cy.get('#saveFiles').click();

    cy.wait('@generate');
    cy.getDataCy('modal_alert_text')
      .should('be.visible')
      .should('contain.text', 'There was an error, please try again.');
  });
});
