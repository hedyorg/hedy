import { loginForUser } from "../tools/login/login";

describe('Is able to share and unshare programs', () => {
    beforeEach(() => {
        loginForUser();
        cy.visit(`${Cypress.env('programs_page')}`);
        // Delete the program in case it's already there
        cy.get("body").then($body => {
            if ($body.find("[data-cy='delete_non_submitted_program_1']").length > 0) {
                cy.getBySel('delete_non_submitted_program_1').then(($btn) => {
                    if ($btn.is(':visible')) {
                        $btn.click();
                        cy.getBySel('modal_yes_button').click();
                    }
                });
            }
        });
        cy.visit(`${Cypress.env('hedy_page')}#default`);
        // Execute program to save it
        cy.get('#editor .cm-content').click();
        // empty textarea
        cy.focused().clear()
        cy.focused().type('print Hello world');
        cy.get('#editor .cm-content').should('contain.text', 'print Hello world');
        cy.get('#runit').click();
        cy.get('#output').should('contain.text', 'Hello world');
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get('#program_1').should('contain.text', 'print Hello world');
    });

    afterEach(() => {
        cy.get('#more_options_1').click();
        cy.getBySel('delete_non_submitted_program_1').click();
        cy.getBySel('modal_yes_button').click();
    });

    it('Clicking the share program button shows the confirm modal and the unshare button, and vice versa', () => {
        cy.get('#share_option_dropdown_1').click();
        cy.get('#share_button_1').click();
        cy.get('#favourite_program_container_1').should('not.be.visible');

        // Make the program private again
        cy.get('#share_option_dropdown_1').click();
        cy.get('#share_button_1').click();
        cy.get('#share_option_dropdown_1').should('be.visible');
    });
});