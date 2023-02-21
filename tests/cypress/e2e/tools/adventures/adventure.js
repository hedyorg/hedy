import { goToTeachersPage } from "../navigation/nav";

export function createAdventure()
{
    goToTeachersPage();

    // Click 'Create new class' button
    cy.getBySel('create_adventure_button').click();

    // Type 'test class'
    cy.getBySel('modal-prompt-input').type("test adventure");

    // Click 'ok'
    cy.getBySel('modal-ok-button').click();

    }

export default {createAdventure};
