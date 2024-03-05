import { createAdventure, deleteAdventure } from "../tools/adventures/adventure";
import { executeHelloWorldProgram, deleteProgram } from "../tools/programs/program";
import { loginForTeacher } from "../tools/login/login";
import { navigateToClass } from "../tools/classes/class";

describe("General tests for my programs page (with both custom teacher and built-in adventure)", () => {
    const programName = "myTestProgram";
    beforeEach(() => {
        loginForTeacher();
    }) 

    it("create adventure, run its code, and see it in my programs", () => {
        createAdventure(programName);
        navigateToClass("CLASS1");
        cy.getBySel("customize_class_button").click(); // Press customize class button
        cy.getBySel("available_adventures_current_level").select(`${programName}`);

        // Now preview it and run the program
        cy.get('[data-cy="preview_class_link"]')
            .click();
        executeHelloWorldProgram(programName)
        cy.get(".programs").should("contain.text", programName);

        deleteAdventure(programName)
    });

    it('can make program public', () => {
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get('#share_option_dropdown_1').click();
        cy.get('#share_button_1').click();
        cy.get('#share_option_dropdown_1').should('contain.text', 'Public');
        cy.get('#non_submitted_button_container_1 [data-cy="submit-btn"]').should('be.visible');
    });


    it("second-teachers can view each other's public programs", () => {
        loginForTeacher("teacher4");
        navigateToClass("CLASS1");
        cy.get("#second_teachers_container tbody tr")
            .each(($tr, i) => {
                if ($tr.text().includes("teacher1")) {
                    cy.get(`#second_teachers_container tbody :nth-child(${i+1}) [data-cy="programs"]`).click();
                    cy.get(".programs")
                        .should("contain.text", programName);
                    // but second teacher should is not permitted to see submit or delete btns.
                    cy.get('#non_submitted_button_container_1 [data-cy="submit-btn"]')
                        .should('not.be.visible');
                    cy.get(`#more_options_1`).click();
                    cy.get(`#program_options_dropdown_1`).should("be.visible");
                    cy.getBySel(`delete_non_submitted_program_1`).should("not.exist");
                }
            })

    });

    it('can make program private', () => {
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get('#share_option_dropdown_1').click();
        cy.get('#share_button_1').click();
        cy.get('#share_option_dropdown_1').should('contain.text', 'Private');
        cy.get('#non_submitted_button_container_1 [data-cy="submit-btn"]').should('not.be.visible');
    });

    it("second-teachers can NOT view each other's public programs", () => {
        loginForTeacher("teacher4");
        navigateToClass("CLASS1");
        cy.get("#second_teachers_container tbody tr")
            .each(($tr, i) => {
                if ($tr.text().includes("teacher1")) {
                    cy.get(`#second_teachers_container tbody :nth-child(${i+1}) [data-cy="programs"]`).click();
                    cy.getBySel("no-programs").should("be.visible");
                }
            })

    });

    it("delete created program", () => {
        deleteProgram(programName);
    });

});
