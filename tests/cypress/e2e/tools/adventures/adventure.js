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

export default {createAdventure};
