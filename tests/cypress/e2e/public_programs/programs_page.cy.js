import { loginForUser } from "../tools/login/login";

describe('Is able to share and unshare programs', () => {
    beforeEach(() => {
        loginForUser();
        cy.visit(`${Cypress.env('programs_page')}`);
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
        cy.get('#editor > .ace_scroller > .ace_content').click();
        // empty textarea
        cy.focused().clear()
        cy.get('#editor').type('print Hello world');
        cy.get('#editor > .ace_scroller > .ace_content').should('contain.text', 'print Hello world');
        cy.get('#runit').click();
        cy.get('#output').should('contain.text', 'Hello world');
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get('#program_1').should('contain.text', 'print Hello world');    
    });

    afterEach(() => {
        cy.getBySel('delete_non_submitted_program_1').click();
        cy.getBySel('modal_yes_button').click();
    });

    it('Clicking the share program button shows the confirm modal and the unshare button, and vice versa', () => {
        cy.get('#non_public_button_container_1 > button').click();
        cy.get('#modal-confirm').should('be.visible');
        cy.getBySel('modal_yes_button').click();
        cy.get('#modal_alert_text').should('be.visible');
        cy.get('#non_public_button_container_1').should('not.be.visible');
        cy.get('#public_button_container_1').should('be.visible');
        
        // Wait until the achievement is gone
        cy.get('#achievement_pop-up', {timeout: 8_000}).should('not.be.visible');
        
        // Make the program private again
        cy.getBySel('unshare_program_1').click();
        cy.get('#modal-confirm').should('be.visible');
        cy.getBySel('modal_yes_button').click();
        cy.get('#modal_alert_text').should('be.visible');
        cy.get('#non_public_button_container_1').should('be.visible');
        cy.get('#public_button_container_1').should('not.be.visible');
    });
});