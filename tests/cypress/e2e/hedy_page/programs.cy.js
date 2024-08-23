import {goToHedyLevel, goToHedyPage} from "../tools/navigation/nav";
import {codeEditorContent} from "../tools/programs/program";

describe('Test commands', () => {
  it('The input of ask is converted to a number in level 12', () => {
    cy.intercept('/parse').as('parse')

    goToHedyLevel(12);

    codeEditorContent().click();
    codeEditorContent().type('a is ask "number"\nprint a * 2'); //

    cy.get('#runit').click();
    cy.wait('@parse');

    cy.get('#ask_modal').should('be.visible');
    cy.get('#ask_modal > form > div > input[type="text"]').type('42');
    cy.get('#ask_modal > form > div > input[type="submit"]').click();

    cy.get('#output').should('contain.text', '84');
  });

  it('The input of ask is converted to a boolean in level 15', () => {
    cy.intercept('/parse').as('parse')

    goToHedyLevel(15);

    codeEditorContent().click();
    codeEditorContent().type('a is true\nb is ask "T/F"\nif a == b\n  print "match"'); //

    cy.get('#runit').click();
    cy.wait('@parse');

    cy.get('#ask_modal').should('be.visible');
    cy.get('#ask_modal > form > div > input[type="text"]').type('True');
    cy.get('#ask_modal > form > div > input[type="submit"]').click();

    cy.get('#output').should('contain.text', 'match');
  });
})
