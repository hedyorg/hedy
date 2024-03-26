import { goToTeachersPage } from "../navigation/nav";

export function createAdventure(name="")
{
    goToTeachersPage();

    // Click 'Create new class' button
    cy.get('#create_adventure_button').click();

    if (name) {
        cy.intercept('/for-teachers/customize-adventure').as('customizeAdventure');      
        cy.get("#custom_adventure_name").clear().type(name);
        cy.wait('@customizeAdventure').should('have.nested.property', 'response.statusCode', 200);
    }

    cy.wait(500);
}

export function deleteAdventure(name) {
    // Delete that adventure
    goToTeachersPage();
    cy.get("#teacher_adventures tbody tr")
    .each(($tr, i) => {
        if ($tr.text().includes(name)) {
            cy.get(`tbody :nth-child(${i+1}) > :nth-child(7) > [data-cy="delete-adventure"]`).click();
            cy.get('#modal-yes-button').should('be.enabled').click();
        }
    })
}

export default {createAdventure};
