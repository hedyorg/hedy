import { goToHome, goToLogin } from "../navigation/nav";

export function loginForUser() {
    login("user1", "123456");
    cy.wait(500);
}

export function loginForTeacher(username="teacher1") {
    login(username, "123456");
    cy.wait(500);
}

export function loginForStudent(student="student1") {
    login(student, "123456");
    cy.wait(500);
}

export function loginForAdmin() {
    login("admin", "123456");
    cy.wait(500);
}

export function login(username, password) {
    cy.clearCookies();
    cy.clearAllLocalStorage()
    cy.clearAllSessionStorage();
    cy.intercept('GET', 'http://localhost:8080/login')
    cy.visit('http://localhost:8080/login');
    // goToLogin();
    cy.get('#username').type(username);
    cy.get('#password').type(password);
    cy.get('#login_button').click();
    cy.wait(500);
}

export function logout()
{
    goToHome();            
    cy.get('body').then($body => {
        if ($body.find(".menubar-text:contains('Log in')").length == 0) {
            
            cy.get('.dropdown > .menubar-text').click();
            cy.get('#logout_button').click();
            cy.wait(500);
            
        } 
    });
}

export default {loginForUser};
