import { createAdventure, deleteAdventure } from "../tools/adventures/adventure";
import { executeHelloWorldProgram, deleteProgram } from "../tools/programs/program";
import { loginForTeacher } from "../tools/login/login";
import { navigateToClass } from "../tools/classes/class";

describe("General tests for my programs page (with both custom teacher and built-in adventure)", () => {
    const uniqueName = (prefix) => `${prefix}${Date.now()}${Math.floor(Math.random() * 1000)}`;
    const programName = uniqueName("myTestProgram");
    const adventure = 'story'

    const configureAdventureForClass = (name) => {
        navigateToClass();
        cy.getDataCy('customize_class_button').click();
        cy.getDataCy('available_adventures_current_level').select(name);
    };

    const createProgramFixture = (name) => {
        createAdventure(name);
        configureAdventureForClass(name);
        cy.getDataCy('preview_class_link').click();
        executeHelloWorldProgram(name);
    };

    before(() => {
        loginForTeacher();
        createProgramFixture(programName);
    });

    beforeEach(() => {
        loginForTeacher();
    })

    it("create adventure, run its code, and see it in my programs", () => {
        const testProgramName = uniqueName('programFlow');

        createProgramFixture(testProgramName);
        cy.getDataCy('programs').should("contain.text", testProgramName);

        deleteProgram(testProgramName);
        deleteAdventure(testProgramName);
    });

    it("should not be added to my programs when running a program with copied code", () => {
        cy.visit(`${Cypress.env('hedy_page')}#${adventure}`);
        // Paste example code
        cy.get(`.adventure_content_${adventure}`).within(() => {
          cy.getDataCy(`paste_example_code_${adventure}`).click();
        });
        cy.getDataCy('runit').click();
        cy.wait(500);
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.getDataCy('programs').should("not.contain.text", 'Story 1');
    });

    it("should be added to my programs when running a program with modified code", () => {
        cy.visit(`${Cypress.env('hedy_page')}#${adventure}`);
        // Paste example code and modify code
        cy.get(`.adventure_content_${adventure}`).within(() => {
          cy.getDataCy(`paste_example_code_${adventure}`).click();
        });
        cy.get('#editor .cm-content').click();
        cy.focused().type('print Hello world\nask Hello world?');
        cy.getDataCy('runit').click();
        cy.wait(500);
        cy.visit(`${Cypress.env('programs_page')}`);
        cy.getDataCy('programs').should("contain.text", adventure);
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
    })

});
