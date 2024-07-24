import { goToHedyPageAdventure, goToProgramsPage } from '../../tools/navigation/nav.js';

export function executeHelloWorldProgram(name) {
    goToHedyPageAdventure(name)
    // Execute program to save it
    cy.getDataCy('editor').click();
    cy.focused().clear()
    cy.focused().type('print Hello world');
    cy.getDataCy('editor').should('contain.text', 'print Hello world');
    cy.getDataCy('runit').click();
    cy.getDataCy('output').should('contain.text', 'Hello world');
    goToProgramsPage();
    cy.getDataCy('programs_list').should("contain.text", name)
    cy.get(`[data-name=${name}]`).should('contain.text', 'print Hello world');
}

export function deleteProgram(name) {
    goToProgramsPage();
    cy.get(".programs")
        .each(($program, i) => {
            if ($program.text().includes(name)) {
                cy.get(`[data-name=${name}]`)
                .first()
                .then($el => {
                    const programId = $el[0].getAttribute("data-id");
                    cy.get(`#more_options_${programId}`).click();
                    cy.get(`#more_options_${programId}`).should("be.visible");
                    cy.getDataCy(`delete_non_submitted_program_${programId}`).click();
                    cy.getDataCy('modal_yes_button').click();
                    cy.wait(500);
            })
            }
        })
}