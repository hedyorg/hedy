import { goToTeachersPage } from "../navigation/nav";

function clickVisibleConfirmButton() {
    cy.get('body').then(($modalBody) => {
        if ($modalBody.find('[data-cy="htmx_modal_yes_button"]:visible').length > 0) {
            cy.getDataCy('htmx_modal_yes_button').click();
        } else if ($modalBody.find('[data-cy="redesign_confirm_yes_button"]:visible').length > 0) {
            cy.getDataCy('redesign_confirm_yes_button').click();
        } else {
            cy.getDataCy('modal_yes_button').should('be.visible').click();
        }
    });
}

export function createAdventure(name)
{
    if (name) {
        cy.visit(`/for-teachers/customize-adventure?name=${encodeURIComponent(name)}&level=1`);
        cy.url().should('include', '/for-teachers/customize-adventure/');

        cy.location('pathname').then((pathname) => {
            const adventureIdMatch = pathname.match(/customize-adventure\/([^/]+)/);
            expect(adventureIdMatch, 'adventure redirect pathname').to.not.be.null;
            const adventureId = adventureIdMatch[1];

            cy.visit(`/for-teachers/legacy/customize-adventure/${adventureId}?new_adventure=1`);
            cy.intercept({
                method: 'POST',
                url: '/for-teachers/customize-adventure'
            }).as('customizeAdventure');

            cy.getDataCy('custom_adventure_name').should('be.visible').clear().type(name);
            cy.get('#submit_adventure').click();
            cy.wait('@customizeAdventure').should('have.nested.property', 'response.statusCode', 200);
        });
        return;
    }

    goToTeachersPage();

    // Click create adventure and normalize to the legacy page used by legacy specs.
    cy.getDataCy('create_adventure_button').click();
    cy.location('pathname').then((pathname) => {
        const adventureIdMatch = pathname.match(/customize-adventure\/([^/]+)/);
        if (adventureIdMatch && adventureIdMatch[1]) {
            cy.visit(`/for-teachers/legacy/customize-adventure/${adventureIdMatch[1]}?new_adventure=1`);
        }
    });
}

export function deleteAdventure(name) {
    // Delete that adventure
    goToTeachersPage();
    cy.reload();
    cy.wait(500);
    openAdventureView();

    cy.get('body').then(($body) => {
        if ($body.find('[data-cy="adventures_table"]').length > 0) {
            cy.contains('tr', name).within(() => {
                cy.get('[data-cy^="delete_adventure_"]').first().click();
            });
            clickVisibleConfirmButton();
            cy.getDataCy('adventures_table').should('be.visible');
            return;
        }

        cy.visit('/for-teachers/adventures/manage');
        cy.contains('tr', name).within(() => {
            cy.get('[data-cy^="manage_adventure_actions_"]').first().click();
            cy.get('[data-cy^="remove_adventure_"]').first().click();
        });
        clickVisibleConfirmButton();
        cy.contains('tr', name).should('not.exist');
    });
}

export function openAdventureView(){
    goToTeachersPage();

    cy.get('body').then(($body) => {
        const $table = $body.find('[data-cy="adventures_table"]');
        const isVisible = $table.length > 0 && $table.is(':visible');

        if (!isVisible && $body.find('[data-cy="view_adventures"]').length > 0) {
            cy.getDataCy('view_adventures').click();
        }
    });

    cy.get('body').then(($body) => {
        const hasLegacyLinks = $body.find('[data-cy^="edit_link_"]').length > 0;
        if (!hasLegacyLinks) {
            cy.visit('/for-teachers/adventures/manage');
            cy.get('#my-adventures-table').should('exist');
        }
    });
}

export default {createAdventure};
