import { goToTeachersPage } from "../navigation/nav";

export function createAdventure()
{
    goToTeachersPage();

    // Click 'Create new class' button
    cy.get('#create_adventure_button').click();

    // Type 'test class'
    cy.get('#modal-prompt-input').type("test adventure");

    // Click 'ok'
    cy.get('#modal-ok-button').click();

    cy.wait(500);
}

export default {createAdventure};
