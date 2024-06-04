const { loginForAdmin } = require("../tools/login/login");
const { goToExploreProgramsPage } = require("../tools/navigation/nav");

it('When selecting a program as Hedys choice, it should be shown', ()=>{
    loginForAdmin();
    goToExploreProgramsPage();
    // Get the id of the first program in the db
    cy.getDataCy('explore_page_programs')
        .children()
        .first()
        .invoke('attr', 'data-cy')
        .as('program_id');
    
    cy.get('@program_id').then(program_id => {
        // mark the program as Hedys choice
        cy.get(`#${program_id}`).click();
        cy.getDataCy('modal_yes_button').click();
        // reload the page to see the changes
        cy.reload();
        cy.getDataCy('explore_favourite_programs')
        .should('be.visible')  // Optionally, ensure the parent is visible
        // Then, within that element, get the child with data-cy=program_id
        .within(() => {
            cy.getDataCy(`${program_id}`)
            .should('be.visible');
        });
    });
});