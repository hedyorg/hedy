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
    const submitLoginForm = () => {
        cy.intercept('POST', '/auth/login').as('loginUi')
        goToLogin();
        cy.getDataCy('username', { timeout: 15000 }).clear().type(username);
        cy.getDataCy('password', { timeout: 15000 }).clear().type(password, { parseSpecialCharSequences: false });
        cy.getDataCy('login_button').click();

        return cy.wait('@loginUi').then(({ response }) => response?.statusCode);
    };

    cy.clearCookies();
    cy.clearAllLocalStorage()
    cy.clearAllSessionStorage();

    cy.request({
        method: 'POST',
        url: '/auth/login',
        failOnStatusCode: false,
        body: { username, password },
    }).then((response) => {
        if (response.status === 200) {
            return;
        }

        submitLoginForm().then((statusCode) => {
            expect(statusCode).to.eq(200);
        });
    });
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
