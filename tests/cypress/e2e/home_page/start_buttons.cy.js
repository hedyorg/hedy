import { loginForStudent, loginForTeacher, loginForUser } from "../tools/login/login";
import { goToHome, navigate_home_button } from "../tools/navigation/nav";

describe('Start buttons', () => {
  it('When not logged in: Should be able to click on start buttons', () => {
    navigate_home_button('start_learning_button', Cypress.env('hedy_page'))
    goToHome();
    cy.getDataCy('start_teaching_button').click();
    cy.url().should('include', 'signup?teacher=true');
  })

  it('As a teacher: Should be able to click on start buttons', () => {
    loginForTeacher();
    navigate_home_button('start_learning_button', Cypress.env('hedy_page'))
    navigate_home_button('start_teaching_button', Cypress.env('teachers_page'))
  })

  it('As a student: Should be able to click on start buttons', () => {
    loginForStudent();
    navigate_home_button('start_learning_button', Cypress.env('hedy_page'))
    navigate_home_button('start_teaching_button', Cypress.env('profile_page'))
  })

  it('As a user: Should be able to click on start buttons', () => {
    loginForUser();
    navigate_home_button('start_learning_button', Cypress.env('hedy_page'))
    navigate_home_button('start_teaching_button', Cypress.env('profile_page'))
  })
})