import { loginForStudent } from "../tools/login/login";
import {goToHedyLevel2Page} from "../tools/navigation/nav";

describe('Go to levels buttons', () => {
  it('Is able to use "Go back to level x" button', () => {
    loginForStudent('student5')
    // Test when code is unchanged
    goToHedyLevel2Page();
    cy.get('#prev_level_button').click();
    cy.url().should('include', Cypress.env('hedy_page'));

    // Test when code is changed
    goToHedyLevel2Page();
    cy.get('#editor').type('hello');
    cy.get('#prev_level_button').click();
    cy.url().should('include', Cypress.env('hedy_page'));
  })

  it('Is able to use "Go to level x" button', () => {
    // TODO: add go to next when there's no quiz and parsons.
    // but if go back passes, this should also pass, so no rush!
  })
})