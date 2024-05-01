const { loginForAdmin } = require("../tools/login/login");
const { goToExploreProgramsPage } = require("../tools/navigation/nav");

it('When selecting a program as Hedys choice, it should be shown', ()=>{
    loginForAdmin();
    goToExploreProgramsPage();
    // Get the id of the first program in the db
    cy.get('[data-cy="explore_page_programs"]')
        .children()
        .first()
        .invoke('attr', 'data-cy')
        .as('program_id');
    
    cy.get('@program_id').then(program_id => {
        // mark the program as Hedys choice
        cy.get(`#${program_id}`).click();
        cy.get('[data-cy="modal_yes_button"]').click();
        // reload the page to see the changes
        cy.reload();
        cy.get(`[data-cy="explore_favourite_programs"] > [data-cy=${program_id}]`).should('be.visible');
    });
});