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
    cy.intercept('/auth/login').as('login')
    cy.clearCookies();
    cy.clearAllLocalStorage()
    cy.clearAllSessionStorage();
    goToLogin();
    cy.getDataCy('username', { timeout: 15000 }).type(username);
    cy.getDataCy('password', { timeout: 15000 }).type(password, { parseSpecialCharSequences: false });
    cy.getDataCy('login_button').click();
    cy.wait('@login');
}

export function logout()
{
    cy.intercept('/auth/logout').as('logout')
    goToHome();            
    cy.getDataCy('user_dropdown').click()
    cy.getDataCy('logout_button').click()
    cy.wait('@logout')
}

export default {loginForUser};
