import { createAdventure, deleteAdventure } from "../tools/adventures/adventure";
import { executeHelloWorldProgram, deleteProgram } from "../tools/programs/program";
import { loginForTeacher } from "../tools/login/login";
import { goToTeachersPage } from "../tools/navigation/nav";

describe("Program page works with cutoms teacher and built-in adventure", () => {
    const programName = "myTestProgram";
    beforeEach(() => {
        loginForTeacher();
    }) 

    it("create adventure and run its code", () => {
        createAdventure(programName);
        goToTeachersPage();
        cy.getBySel("view_class_link").first().click(); // Press on view class button
        cy.getBySel("customize_class_button").click(); // Press customize class button
        cy.getBySel("available_adventures_current_level").select(`${programName}`);

        // Now preview it and run the program
        cy.get('[data-cy="preview_class_link"]')
            .click();
        executeHelloWorldProgram(programName)
        cy.get(".programs").should("contain.text", programName);

        deleteAdventure(programName)
    });

    it('can (un)share the created program', () => {
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get('#share_option_dropdown_1').click();
        cy.get('#share_button_1').click();
        cy.get('#share_option_dropdown_1').should('contain.text', 'Public');
        cy.getBySel('submit-btn').should('be.visible');

        // Make the program private again
        cy.get('#share_option_dropdown_1').click();
        cy.get('#share_button_1').click();
        cy.get('#share_option_dropdown_1').should('contain.text', 'Private');
        cy.get('#non_submitted_button_container_1 [data-cy="submit-btn"]').should('not.be.visible');
    });

    it("delete created program", () => {
        deleteProgram(programName);
    })
});
