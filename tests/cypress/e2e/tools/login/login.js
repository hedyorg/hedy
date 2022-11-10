import { goToHome, goToLogin } from "../navigation/nav";

export function loginForUser() {
    login("user1", "123456");
}

export function loginForTeacher() {
    login("teacher1", "user1");
}

export function loginForStudent() {
    login("student1", "123456");
}

export function login(username, password) {
    goToLogin();
    cy.get('#username').type(username);
    cy.get("#password").type(password);
    cy.get('#login > .green-btn').click();
}

export function logout()
{
    goToHome();            
    cy.get("body").then($body => {
        if ($body.find(".menubar-text:contains('Log in')").length == 0) {   
            
            cy.get('.dropdown > .menubar-text').click();
            cy.get(':nth-child(4) > .dropdown-item').click();
            cy.wait(500);
            
        } 
    });
}

export default {loginForUser};
