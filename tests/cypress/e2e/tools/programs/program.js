
export function executeHelloWorldProgram(name) {
    cy.visit(`${Cypress.env('hedy_page')}#${name}`);
    // make sure to navigate to the wanted program tab.
    cy.get(`[data-cy="${name}"]`)
        .click();
    // Execute program to save it
    cy.get('#editor .cm-content').click();
    // empty textarea
    cy.focused().clear()
    cy.focused().type('print Hello world');
    cy.get('#editor .cm-content').should('contain.text', 'print Hello world');
    cy.get('#runit').click();
    cy.get('#output').should('contain.text', 'Hello world');
    cy.visit(`${Cypress.env('programs_page')}`);
    cy.get(".programs").should("contain.text", name)
    // cy.get('#program_1').should('contain.text', 'print Hello world');
}

export function deleteProgram(name) {
    cy.visit(`${Cypress.env('programs_page')}`);
    cy.get(".programs")
        .each(($program, i) => {
            if ($program.text().includes(name)) {
                cy.get(`[data-name=${name}]`)
                .first()
                .then($el => {
                    const programId = $el[0].getAttribute("data-id");
                    cy.get(`#more_options_${programId}`).click();
                    cy.get(`#more_options_${programId}`).should("be.visible");
                    cy.getBySel(`delete_non_submitted_program_${programId}`).click();
                    cy.getBySel('modal_yes_button').click();
            })
            }
        })
}