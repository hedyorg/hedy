import { goToTeachersPage } from "../navigation/nav";

export function createAdventure(name="")
{
    goToTeachersPage();

    // Click 'Create new class' button
    cy.get('#create_adventure_button').click();

    if (name) {
        cy.get("#custom_adventure_name").clear().type(name);
        cy.get("#save_adventure_button").click();
    }

    cy.wait(500);
}

export function deleteAdventure(name) {
    // Delete that adventure
    goToTeachersPage();
    if (!cy.get("#adventures_table")){
        cy.get("#view_adventures").click();
    }
    cy.get("#adventures_table tbody tr")
    .each(($tr, i) => {
        if ($tr.text().includes(name)) {
            cy.get(`tbody :nth-child(${i+1}) [data-cy="delete-adventure"]`).click();
            cy.get('#modal-yes-button').should('be.enabled').click();
        }
    })
}

export default {createAdventure};
