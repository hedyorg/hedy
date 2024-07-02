import { loginForStudent, loginForTeacher, loginForUser } from "../tools/login/login";
import { goToHome, navigate_home_button } from "../tools/navigation/nav";

describe('Start buttons', () => {
  it('When not logged in: Should be able to click on start buttons', () => {
    navigate_home_button('start_learning_button', '/hedy')
    goToHome();
    cy.getDataCy('start_teaching_button').click();
    cy.url().should('include', 'signup?teacher=true');
  })

  it('As a teacher: Should be able to click on start buttons', () => {
    loginForTeacher();
    navigate_home_button('start_learning_button', '/hedy')
    navigate_home_button('start_teaching_button', '/for-teachers')
  })

  it('As a student: Should be able to click on start buttons', () => {
    loginForStudent();
    navigate_home_button('start_learning_button', '/hedy')
    navigate_home_button('start_teaching_button', '/my-profile')
  })

  it('As a user: Should be able to click on start buttons', () => {
    loginForUser();
    navigate_home_button('start_learning_button', '/hedy')
    navigate_home_button('start_teaching_button', '/my-profile')
  })
})