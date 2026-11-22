// Adventures with `show_output` hide their example program: students can only run it, and recreate it (#4007).
// The demo adventure is 'recreate_program' in level 6.
describe('Adventure with a hidden, runnable program', () => {
  it('shows the program runner instead of the example code', () => {
    cy.visit('/hedy/6#recreate_program');

    cy.get('[data-cy="adventure_output_frame_recreate_program"]')
      .should('be.visible')
      .and('have.attr', 'src', '/adventure-output/recreate_program/6');
    cy.get('#adv_recreate_program').should('not.contain.text', 'Do you like ice cream?');
    cy.get('[data-cy="paste_example_code_recreate_program"]').should('not.exist');
  });

  it('runs the hidden program interactively, showing only its output', () => {
    cy.visit('/adventure-output/recreate_program/6');

    cy.get('[data-cy="adventure_output_only"]').should('be.visible');
    cy.get('#editor').should('not.be.visible');

    runAndAnswer('Hedy', 'yes');
    cy.get('#output').should('contain.text', 'Hedy likes ice cream!');
    // No praise for running a program the student did not write
    cy.get('#okbox').should('not.exist');

    // It can be run again, with different answers
    runAndAnswer('Hedy', 'no');
    cy.get('#output').should('contain.text', 'Hedy does not like ice cream.');
  });
});

function runAndAnswer(name, answer) {
  cy.get('#runit').click();
  cy.get('#ask_modal').should('be.visible').and('contain.text', 'What is your name?');
  cy.get('#ask_modal input[type="text"]').type(name);
  cy.get('#ask_modal form').submit();

  cy.get('#ask_modal').should('be.visible').and('contain.text', 'Do you like ice cream? yes or no');
  cy.get('#ask_modal input[type="text"]').type(answer);
  cy.get('#ask_modal form').submit();
}
