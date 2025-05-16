
export function codeEditorContent() {
    return cy.get('#editor > .cm-editor > .cm-scroller > .cm-content');
}

export function executeHelloWorldProgram(name) {
    cy.visit(`${Cypress.env('hedy_page')}#${name}`);
    // make sure to navigate to the wanted program tab.
    cy.getDataCy('dropdown_open_button').click();
    cy.getDataCy(`${name}`).click();
    // Execute program to save it
    cy.get('#editor .cm-content').click();
    // empty textarea
    cy.focused().clear()
    cy.focused().type('print Hello world');
    cy.get('#editor .cm-content').should('contain.text', 'print Hello world');
    cy.getDataCy('runit').click();
    cy.getDataCy('output').should('contain.text', 'Hello world');
    cy.visit(`${Cypress.env('programs_page')}`);
    cy.getDataCy('programs').should("contain.text", name)
    // cy.get('#program_1').should('contain.text', 'print Hello world');
}

export function deleteProgram(name) {
    cy.visit(`${Cypress.env('programs_page')}`);
    cy.getDataCy('programs')
        .each(($program, i) => {
            if ($program.text().includes(name)) {
                cy.getDataCy(`${name}`)
                .first()
                .then($el => {
                    const programId = $el[0].getAttribute("data-id");
                    cy.getDataCy(`more_options_${programId}`).click();
                    cy.getDataCy(`more_options_${programId}`).should("be.visible");
                    cy.getDataCy(`delete_non_submitted_program_${programId}`).click();
                    cy.getDataCy('modal_yes_button').click();
                    cy.wait(500);
            })
            }
        })
}

export function codeMirrorContent() {
    return cy.get('#editor > .cm-editor > .cm-scroller > .cm-content');
}
