import { goToTeachersPage } from "../navigation/nav";

export function createAdventure(name)
{
    goToTeachersPage();

    // Click 'Create new class' button
    cy.getDataCy('create_adventure_button').click();

    if (name) {
        cy.intercept('/for-teachers/customize-adventure').as('customizeAdventure');      
        cy.getDataCy('custom_adventure_name').clear().type(name);
        cy.wait(500)
        cy.getDataCy('level_select').click();
        cy.wait(500)
        cy.getDataCy('1').click();
        cy.wait(500)
        cy.getDataCy('level_select').click()
        cy.wait(500)
        cy.wait('@customizeAdventure').should('have.nested.property', 'response.statusCode', 200);
    }

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
    cy.getDataCy('adventures_table').then($viewAdventure => {
        if (!$viewAdventure.is(':visible')) {
            cy.getDataCy('view_adventures').click();
        }
    });
}

export default {createAdventure};
