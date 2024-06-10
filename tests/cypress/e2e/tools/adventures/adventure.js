import { goToTeachersPage } from "../navigation/nav";
import { openAdventureView } from '../../tools/classes/class.js';

export function createAdventure(name)
{
    goToTeachersPage();

    // Click 'Create new class' button
    cy.get('#create_adventure_button').click();

    if (name) {
        cy.intercept('/for-teachers/customize-adventure').as('customizeAdventure');      
        cy.getDataCy('custom_adventure_name').clear().type(name);
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
    openAdventureView();

    cy.get("#adventures_table tbody tr")
    .each(($tr, i) => {
        if ($tr.text().includes(name)) {
            cy.get(`tbody :nth-child(${i+1}) [data-cy="delete_adventure"]`).click();
        }
    })
    cy.getDataCy('modal_yes_button').should('be.enabled').click();
    cy.getDataCy('adventures_table').should("be.visible");
}

export default {createAdventure};
