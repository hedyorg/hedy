const { loginForAdmin } = require("../tools/login/login");
const { goToExploreProgramsPage } = require("../tools/navigation/nav");

describe('Explore programs page', () => {
    beforeEach(() => {
        loginForAdmin();
        goToExploreProgramsPage();
    });

    it('When selecting a program as Hedys choice, it should be shown', ()=>{
        // Get the id of the first program in the db
        cy.get('#explore_page_programs')
          .children()
          .first()
          .invoke('attr', 'data-cy')
          .as('program_id');
        
        cy.get('@program_id').then(program_id => {
            // mark the program as Hedys choice
            cy.get(`#${program_id}`).click();
            cy.get('#modal-yes-button').click();
            // reload the page to see the changes
            cy.reload();
            cy.get(`#explore_favourite_programs > [data-cy=${program_id}]`).should('be.visible');
        });
    });
});