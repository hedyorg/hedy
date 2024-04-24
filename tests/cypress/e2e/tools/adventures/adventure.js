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
    cy.get("#adventures_table").then($viewAdventure => {
        if (!$viewAdventure.is(':visible')) {
            cy.get("#view_adventures").click();
        }
    });

    cy.get("#adventures_table tbody tr")
    .each(($tr, i) => {
        if ($tr.text().includes(name)) {
            cy.get(`tbody :nth-child(${i+1}) [data-cy="delete-adventure"]`).click();
        }
    })
    cy.get('[data-cy="modal_yes_button"]').should('be.enabled').click();
}

export default {createAdventure};
