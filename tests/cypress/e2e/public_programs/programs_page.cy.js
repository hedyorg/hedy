import { createAdventure, deleteAdventure } from "../tools/adventures/adventure";
import { executeHelloWorldProgram, deleteProgram } from "../tools/programs/program";
import { loginForTeacher } from "../tools/login/login";
import { navigateToClass } from "../tools/classes/class";
import { makeProfilePublic } from "../tools/profile/profile";

describe("General tests for my programs page (with both custom teacher and built-in adventure)", () => {
    const programName = "myTestProgram";
    const adventure = 'story'
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

    it("should not be added to my programs when running a program with copied code", () => {
        cy.visit(`${Cypress.env('hedy_page')}#${adventure}`);
        // make sure to navigate to the wanted program tab.
        cy.get(`[data-cy="${adventure}"]`)
            .click();
        // Paste example code 
        cy.get(`[data-cy="paste-example-code-${adventure}"]`).click();
        cy.get('#runit').click();
        cy.wait(500);
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get(".programs").should("not.contain.text", adventure);
    });

    it("should be added to my programs when running a program with modified code", () => {
        cy.visit(`${Cypress.env('hedy_page')}#${adventure}`);
        // make sure to navigate to the wanted program tab.
        cy.get(`[data-cy="${adventure}"]`)
            .click();
        // Paste example code and modify code
        cy.get(`[data-cy="paste-example-code-${adventure}"`).click();
        cy.get('#editor .cm-content').click();
        cy.focused().type('print Hello world\nask Hello world?');
        cy.get('#runit').click();
        cy.wait(500);
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get(".programs").should("contain.text", adventure);
    });

    it('can make program public', () => {
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get(`[data-name=${programName}]`)
            .first()
            .then($el => {
                const programId = $el[0].getAttribute("data-id");
                cy.get(`#share_option_dropdown_${programId}`).click();
                cy.get(`#share_button_${programId}`).click();
                cy.get(`#share_option_dropdown_${programId}`).should('contain.text', 'Public');
                cy.get(`#non_submitted_button_container_${programId} [data-cy="submit-btn"]`).should('be.visible');
            })
    });

    it('can favourite and unfavourite a public program', () => {
        cy.intercept({
            url: '/auth/public_profile',
            method: "POST"
        }).as('public_profile')
        makeProfilePublic();
        cy.wait('@public_profile')
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.get(`[data-name=${programName}]`)
            .first()
            .then($el => {
                const programId = $el[0].getAttribute("data-id");
                //favourite a program:
                cy.get(`#favourite_program_container_${programId}`).click();
                cy.get(`#modal-confirm-text`).should('contain.text', 'favourite');
                cy.get('[data-cy="modal_yes_button"]').should('be.enabled').click();
                //unfavourite a program:
                cy.wait(500);
                cy.get(`#favourite_program_container_${programId}`).click();
                cy.get(`#modal-confirm-text`).should('contain.text', 'unfavourite');
                cy.get('[data-cy="modal_yes_button"]').should('be.enabled').click();
            })
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
                    cy.get(`[data-name=${programName}]`)
                    .first()
                    .then($el => {
                        const programId = $el[0].getAttribute("data-id");
                        cy.get(`#non_submitted_button_container_${programId} [data-cy="submit-btn"]`)
                            .should('not.be.visible');
                        cy.get(`#more_options_${programId}`).click();
                        cy.get(`#program_options_dropdown_${programId}`).should("be.visible");
                        cy.getBySel(`delete_non_submitted_program_${programId}`).should("not.exist");
                    })
                }
            })

    });

    it('can make program private', () => {
        cy.visit(`${Cypress.env('programs_page')}`);

        cy.get(`[data-name=${programName}]`)
                    .first()
                    .then($el => {
                        const programId = $el[0].getAttribute("data-id");
                        cy.get(`#share_option_dropdown_${programId}`).click();
                        cy.get(`#share_button_${programId}`).click();
                        cy.get(`#share_option_dropdown_${programId}`).should('contain.text', 'Private');
                        cy.get(`#non_submitted_button_container_${programId} [data-cy="submit-btn"]`).should('not.be.visible');
                    })
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
