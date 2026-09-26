
export function codeEditorContent() {
    return cy.get('#editor > .cm-editor > .cm-scroller > .cm-content');
}

function clickRunButtonWhenUncovered() {
    cy.get('body').then(($body) => {
        if ($body.find('#dropdown-level:visible').length > 0) {
            cy.getDataCy('dropdown_open_button').click();
        }
    });

    cy.get('#dropdown-level').should('not.be.visible');

    const originalScrollBehavior = Cypress.config('scrollBehavior');
    Cypress.config('scrollBehavior', { block: 'center' });
    cy.getDataCy('runit')
        .scrollIntoView()
        .should('be.visible')
        .should('not.be.disabled')
        .click();
    Cypress.config('scrollBehavior', originalScrollBehavior)
}

export function executeHelloWorldProgram(adventureName: string) {
    cy.visit(`${Cypress.env('hedy_page')}#${adventureName}`);
    // make sure to navigate to the wanted program tab.
    cy.getDataCy('dropdown_open_button').click();
    cy.getDataCy(`${adventureName}`).click();
    // close dropdown
    cy.getDataCy('dropdown_open_button').click();
    // Execute program to save it
    cy.get('#editor .cm-content').click();
    // empty textarea
    cy.focused().clear()
    cy.focused().type('print Hello world');
    cy.get('#editor .cm-content').should('contain.text', 'print Hello world');
    clickRunButtonWhenUncovered()
    cy.getDataCy('output').should('contain.text', 'Hello world');
    cy.visit(`${Cypress.env('programs_page')}`);
    cy.getDataCy('programs').should("contain.text", adventureName)
    // cy.get('#program_1').should('contain.text', 'print Hello world');
}

export function deleteProgram(programName: string) {
    cy.visit(`${Cypress.env('programs_page')}`);
    cy.getDataCy('programs')
        .each(($program, i) => {
            if ($program.text().includes(programName)) {
                cy.getDataCy(`${programName}`)
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
