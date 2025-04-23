import { createAdventure, deleteAdventure } from "../tools/adventures/adventure";
import { executeHelloWorldProgram, deleteProgram } from "../tools/programs/program";
import { login, loginForTeacher } from "../tools/login/login";
import { navigateToClass } from "../tools/classes/class";
import { makeProfilePublic } from "../tools/profile/profile";
import { clickAdventureIndexButton } from "../tools/navigation/nav";

describe("General tests for my programs page (with both custom teacher and built-in adventure)", () => {
    const programName = "myTestProgram";
    const adventure = 'story'
    beforeEach(() => {
        loginForTeacher();
    })

    it("create adventure, run its code, and see it in my programs", () => {
        createAdventure(programName);
        navigateToClass("CLASS1");
        cy.getDataCy('customize_class_button').click(); // Press customize class button
        cy.getDataCy('available_adventures_current_level').select(`${programName}`);

        // Now preview it and run the program
        cy.getDataCy('preview_class_link').click();
        executeHelloWorldProgram(programName)
        cy.getDataCy('programs').should("contain.text", programName);

        deleteAdventure(programName)
    });

    it("should not be added to my programs when running a program with copied code", () => {
        cy.visit(`${Cypress.env('hedy_page')}#${adventure}`);
        // Paste example code
        cy.getDataCy(`paste_example_code_${adventure}`).click();
        cy.getDataCy('runit').click();
        cy.wait(500);
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.getDataCy('programs').should("not.contain.text", adventure);
    });

    it("should be added to my programs when running a program with modified code", () => {
        cy.visit(`${Cypress.env('hedy_page')}#${adventure}`);
        // Paste example code and modify code
        cy.getDataCy(`paste_example_code_${adventure}`).click();
        cy.get('#editor .cm-content').click();
        cy.focused().type('print Hello world\nask Hello world?');
        cy.getDataCy('runit').click();
        cy.wait(500);
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.getDataCy('programs').should("contain.text", adventure);
    });

    it('can make program public', () => {
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.getDataCy(`${programName}`)
            .first()
            .then($el => {
                const programId = $el[0].getAttribute("data-id");
                cy.getDataCy(`share_option_dropdown_${programId}`).click();
                cy.getDataCy(`share_button_${programId}`).click();
                cy.getDataCy(`share_option_dropdown_${programId}`).should('contain.text', 'Public');
                cy.getDataCy(`non_submitted_button_container_${programId}`).getDataCy(`submit_btn_${programId}`).should('be.visible');
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
        cy.getDataCy(`${programName}`)
            .first()
            .then($el => {
                const programId = $el[0].getAttribute("data-id");
                //favourite a program:
                cy.getDataCy(`favourite_program_container_${programId}`).click();
                cy.getDataCy('modal_confirm_text').should('contain.text', 'favourite');
                cy.getDataCy('modal_yes_button').click();
                //unfavourite a program:
                cy.wait(500);
                cy.getDataCy(`favourite_program_container_${programId}`).click();
                cy.getDataCy('modal_confirm_text').should('contain.text', 'unfavourite');
                cy.getDataCy('modal_yes_button').click();
            })
    });

    it("second-teachers can view each other's public programs", () => {
        loginForTeacher("teacher4");
        navigateToClass("CLASS1");
        cy.get("#second_teachers_container tbody tr")
            .each(($tr, i) => {
                if ($tr.text().includes("teacher1")) {
                    cy.get(`#second_teachers_container tbody :nth-child(${i+1}) [data-cy="programs"]`).click();
                    cy.getDataCy('programs')
                        .should("contain.text", programName);
                    // but second teacher should is not permitted to see submit or delete btns.
                    cy.getDataCy(`${programName}`)
                    .first()
                    .then($el => {
                        const programId = $el[0].getAttribute("data-id");
                        cy.getDataCy(`submit_btn_${programId}`)
                            .should('not.be.visible');
                        cy.getDataCy(`more_options_${programId}`).click();
                        cy.getDataCy(`program_options_dropdown_${programId}`).should("be.visible");
                        cy.getDataCy(`delete_non_submitted_program_${programId}`).should("not.exist");
                    })
                }
            })

    });

    it('can make program private', () => {
        cy.visit(`${Cypress.env('programs_page')}`);

        cy.getDataCy(`${programName}`)
        .first()
        .then($el => {
            const programId = $el[0].getAttribute("data-id");
            cy.getDataCy(`share_option_dropdown_${programId}`).click();
            cy.getDataCy(`share_button_${programId}`).click();
            cy.getDataCy(`share_option_dropdown_${programId}`).should('contain.text', 'Private');
            cy.getDataCy(`non_submitted_button_container_${programId}`).getDataCy(`submit_btn_${programId}`).should('not.be.visible');
        })
    });

    it("second-teachers can NOT view each other's public programs after making them private", () => {
        loginForTeacher("teacher4");
        navigateToClass("CLASS1");

        cy.getDataCy('second_teachers_container')
            .within(() => {
                cy.getDataCy('second_teacher_username_cell')
                    .each(($usernameCell, index) => {
                        if ($usernameCell.text().includes("teacher1")) {
                            cy.getDataCy('programs').eq(index).click();
                            cy.getDataCy('no-programs').should("not.exist");
                        }
                    });
            });
    });


    it("delete created program", () => {
        deleteProgram(programName);
    });

    describe('Test filters', () => {
        beforeEach(() => {
            cy.visit(`${Cypress.env('programs_page')}`);
        })
        it("The level filter should show the appropiate programs", ()=>{
            // After selecting level 2 only the programs from level 2 should ve visible
            cy.getDataCy('levels_dropdown').select('2')

            cy.get('#program_3e8926c0515d47a5aeb116164b1278c9').should('be.visible')
            cy.get('#program_195d94e733ff49b08079848409e664b6').should('be.visible')

            cy.get('#program_e1d94726655947c5b0309abb18cc17ca').should('not.exist')
            cy.get('#program_4c426ff4cd5a40d7bb65bfbb35907f8b').should('not.exist')

            // After selecting level 1 only the programs from level 1 should ve visible
            cy.getDataCy('levels_dropdown').select('1')

            cy.get('#program_3e8926c0515d47a5aeb116164b1278c9').should('not.exist')
            cy.get('#program_195d94e733ff49b08079848409e664b6').should('not.exist')

            cy.get('#program_e1d94726655947c5b0309abb18cc17ca').should('be.visible')
            cy.get('#program_4c426ff4cd5a40d7bb65bfbb35907f8b').should('be.visible')

            // Selecting the - Level - options should show every program
            cy.getDataCy('levels_dropdown').select(0);
            cy.get('#program_3e8926c0515d47a5aeb116164b1278c9').should('be.visible')
            cy.get('#program_195d94e733ff49b08079848409e664b6').should('be.visible')

            cy.get('#program_e1d94726655947c5b0309abb18cc17ca').should('be.visible')
            cy.get('#program_4c426ff4cd5a40d7bb65bfbb35907f8b').should('be.visible')
        })

        it('The adventure filter show the appropiate programs', () => {
            cy.getDataCy('adventure_select').select('ask')
            cy.get('#program_e1d94726655947c5b0309abb18cc17ca').should('be.visible');
            cy.wait(300)
            cy.getDataCy('adventure_select').select('print')
            cy.get('#program_4c426ff4cd5a40d7bb65bfbb35907f8b').should('be.visible');

            // Selecting the - Adventure - options should show every program
            cy.getDataCy('adventure_select').select(0);
            cy.get('#program_3e8926c0515d47a5aeb116164b1278c9').should('be.visible')
            cy.get('#program_195d94e733ff49b08079848409e664b6').should('be.visible')

            cy.get('#program_e1d94726655947c5b0309abb18cc17ca').should('be.visible')
            cy.get('#program_4c426ff4cd5a40d7bb65bfbb35907f8b').should('be.visible')
        })

        it('Introduction adventures should be visible', () => {
            login('user1', '123456')
            cy.visit(`${Cypress.env('programs_page')}`);
            cy.getDataCy('adventure_select').select('Introduction')
            cy.get('#program_fb23d0fa90ce48b5bf87c0632969fc28').should('be.visible')
        })
    })

});
