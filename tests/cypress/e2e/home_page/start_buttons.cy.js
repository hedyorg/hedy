import { loginForStudent, loginForTeacher, loginForUser } from "../tools/login/login";
import { goToHome, navigateHomeButton } from "../tools/navigation/nav";

describe('Start buttons', () => {
  it('When not logged in: Should be able to click on start buttons', () => {
    navigateHomeButton('start_learning_button', Cypress.env('hedy_page'))
    goToHome();
    cy.getDataCy('start_teaching_button').click();
    cy.url().should('include', 'signup?teacher=true');
  })

  it('As a teacher: Should be able to click on start buttons', () => {
    loginForTeacher();
    navigateHomeButton('start_learning_button', Cypress.env('hedy_page'))
    navigateHomeButton('start_teaching_button', Cypress.env('teachers_page'))
  })

  it('As a student: Should be able to click on start buttons', () => {
    loginForStudent();
    navigateHomeButton('start_learning_button', Cypress.env('hedy_page'))
    navigateHomeButton('start_teaching_button', Cypress.env('profile_page'))
  })

  it('As a user: Should be able to click on start buttons', () => {
    loginForUser();
    navigateHomeButton('start_learning_button', Cypress.env('hedy_page'))
    navigateHomeButton('start_teaching_button', Cypress.env('profile_page'))
  })
})