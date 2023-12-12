import { goToTeachersPage } from "../navigation/nav";

export function createAdventure()
{
    goToTeachersPage();

    // Click 'Create new class' button
    cy.get('#create_adventure_button').click();

    // Click 'Go back to teachers page' button
    cy.get('#go_back_button').click();

    cy.wait(500);
}

export default {createAdventure};
