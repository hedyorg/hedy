import { goToTeachersPage } from "../navigation/nav";

export function createAdventure(name)
{
    goToTeachersPage();

    // Click 'Create new class' button
    cy.get('#create_adventure_button').click();

    if (name) {
        cy.intercept('/for-teachers/customize-adventure').as('customizeAdventure');      
        cy.get("#custom_adventure_name").clear().type(name);
        cy.wait(500)
        cy.wait('@customizeAdventure').should('have.nested.property', 'response.statusCode', 200);
    }

    cy.wait(500);
}

export function deleteAdventure(name) {
    // Delete that adventure
    goToTeachersPage();
    cy.reload();
    cy.wait(500);
    cy.get("#adventures_table").then($viewClass => {
        if (!$viewClass.is(':visible')) {
            cy.get("#view_adventures").click();
        }
    });

    cy.get(`[data-cy='delete_${name}']`).click()
    cy.get('#modal-yes-button').should('be.enabled').click();
}

export default {createAdventure};
