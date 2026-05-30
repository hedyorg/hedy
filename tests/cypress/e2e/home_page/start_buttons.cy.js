import { loginForStudent, loginForTeacher, loginForUser } from "../tools/login/login";
import { navigateHomeButton } from "../tools/navigation/nav";

describe('Start buttons', () => {
  it('When not logged in: start_learning goes to hedy, start_teaching goes to signup', () => {
    navigateHomeButton('start_learning_button', Cypress.env('hedy_page'))
    navigateHomeButton('start_teaching_button', Cypress.env('signup_page'))
  })

  it('As a teacher: start_learning goes to hedy, start_teaching goes to teachers page', () => {
    loginForTeacher();
    navigateHomeButton('start_learning_button', Cypress.env('hedy_page'))
    navigateHomeButton('start_teaching_button', Cypress.env('teachers_page'))
  })

  it('As a student: start_learning goes to hedy, start_teaching goes to profile', () => {
    loginForStudent();
    navigateHomeButton('start_learning_button', Cypress.env('hedy_page'))
    // Already logged in, so /signup redirects to the profile page
    navigateHomeButton('start_teaching_button', Cypress.env('profile_page'))
  })

  it('As a user: start_learning goes to hedy, start_teaching goes to profile', () => {
    loginForUser();
    navigateHomeButton('start_learning_button', Cypress.env('hedy_page'))
    // Already logged in, so /signup redirects to the profile page
    navigateHomeButton('start_teaching_button', Cypress.env('profile_page'))
  })
})
