import { goToTeachersPage } from "../navigation/nav";

export function createAdventure(name)
{
    if (name) {
        cy.visit(`/for-teachers/customize-adventure?ui=legacy&name=${encodeURIComponent(name)}&level=1`);

        cy.intercept({
            method: 'POST',
            url: '/for-teachers/customize-adventure'
        }).as('customizeAdventure');

        cy.getDataCy('custom_adventure_name').should('be.visible').should('have.value', name);
        cy.get('#submit_adventure').click();
        cy.wait('@customizeAdventure').should('have.nested.property', 'response.statusCode', 200);
        return;
    }

    goToTeachersPage();

    // Click 'Create new class' button
    cy.getDataCy('create_adventure_button').click();

    cy.wait(1000);
}

export function deleteAdventure(name) {
    // Delete that adventure
    goToTeachersPage();
    cy.reload();
    cy.wait(500);
    openAdventureView();

    cy.getDataCy(`delete_adventure_${name}`).click();
    cy.getDataCy('modal_yes_button').click();
    cy.getDataCy('adventures_table').should("be.visible");
}

export function openAdventureView(){
    cy.get('body').then(($body) => {
        const $table = $body.find('[data-cy="adventures_table"]');
        const isVisible = $table.length > 0 && $table.is(':visible');

        if (!isVisible && $body.find('[data-cy="view_adventures"]').length > 0) {
            cy.getDataCy('view_adventures').click();
        }
    });
}

export default {createAdventure};
