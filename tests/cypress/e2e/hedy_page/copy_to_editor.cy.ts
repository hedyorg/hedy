import { goToHedyPage } from "../tools/navigation/nav";

describe('Copy code to editor button', () => {
  beforeEach(() => {
    goToHedyPage();
  });

  it('should exist for every show-copy-button editor.', () => {
    cy.get('.adventure_content_print_command.show-copy-button')
      .find('pre')
      .each(($editor, idx, $editors) => {
        const code = $editor.find('code').get(0).innerText;
        cy.wrap($editor).find('[data-cy="paste_example_code_print_command"]')
          .should('have.length', 1)
          .should('be.visible')
          .should('have.attr', 'aria-description').should('contain', code);
      })
  });

  it('should copy content to global editor when pressed.', () => {
    cy.get('[data-cy="paste_example_code_print_command"]').as('buttons');

    cy.get('@buttons').first().click();
    cy.focused().closest('#editor').should('exist').should('contain.text', 'print');

    // Replaces content after clicking the next button.
    cy.get('@buttons').eq(1).click();
    cy.focused().should('not.contain.text', 'print').should('contain.text', '_')
  });
});
