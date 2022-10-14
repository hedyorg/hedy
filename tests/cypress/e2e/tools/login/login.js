export function loginForAdmin() {
    cy.visit(Cypress.env('base_url'));
    cy.get(':nth-child(6) > .menubar-text').click();

    cy.get('#username').type("admin_user");
    cy.get("#password").type("useruser");
    cy.get('#login > .green-btn').click();
    cy.wait(1000);
    cy.location().then((loc) => {
        console.log(loc);
        if(loc.pathname != "/admin")
        {
            cy.visit(Cypress.env('base_url'));
            cy.get(':nth-child(6) > .menubar-text').click();
            cy.get('.flex-row.gap-2 > .green-btn').click();
            cy.get('#username').type("admin_user");
            cy.get('#email').type("user@user.com");
            cy.get('#password').type("useruser");
            cy.get('#password_repeat').type("useruser");
            cy.get('#language').select("English");
            cy.get('#birth_year').type(2001);
            cy.get('#gender').select("Male");
            cy.get('#country').select("Nederland");
            cy.get('#agree_terms').click();
            cy.get(':nth-child(16) > .green-btn').click();
        }
    });
}

export function loginForTeacher() {
    cy.visit(Cypress.env('base_url'));
    
    cy.get(':nth-child(6) > .menubar-text').click();
    cy.get('#username').type("teacher_user");
    cy.get("#password").type("useruser");
    cy.get('#login > .green-btn').click();

    cy.wait(500);
    cy.location().then((loc) => {
        var location_was = loc.pathname;
        if(loc.pathname != "/for-teachers")
        {
            
            logout();
            if(location_was != "/landing-page")
            {
                goToRegister();

                cy.get('#username').type("teacher_user");
                cy.get('#email').type("teacher_user@user.com");
                cy.get('#password').type("useruser");
                cy.get('#password_repeat').type("useruser");
                cy.get('#language').select("English");
                cy.get('#birth_year').type(2001);
                cy.get('#gender').select("Male");
                cy.get('#country').select("Nederland");
                cy.get('#agree_terms').click();
                cy.get(':nth-child(16) > .green-btn').click();
            }
            
            

            loginForAdmin();
            cy.get('[onclick="window.open(\'/admin/users\', \'_self\')"]').click();
            
            cy.get('.teacher_cell > input:checkbox:not(:checked)').each((el) => {
                cy.wrap(el).click();
                cy.get('#modal-yes-button').click();
            });

            logout();
            loginForTeacher();
        }
    });
}

export function logout()
{
    cy.visit(Cypress.env('base_url'));
            
    cy.get("body").then($body => {
        if ($body.find(".menubar-text:contains('Log In')").length == 0) {   
            
            cy.get('.dropdown > .menubar-text').click();
            cy.get(':nth-child(4) > .dropdown-item').click();
            cy.wait(500);
            
        } 
    });

}

export function goToRegister()
{
    cy.visit(Cypress.env('base_url') + "/signup");
}



export default {loginForAdmin, loginForTeacher};