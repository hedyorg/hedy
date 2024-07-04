import { loginForStudent, loginForTeacher, loginForUser } from "../tools/login/login";
import { goToHome, navigate_home_button } from "../tools/navigation/nav";

describe('Navigation buttons', () => {
  it('When not logged in: Is able to click all menubar buttons', () => {
    navigate_home_button('hedy_button', Cypress.env('hedy_page'))
    navigate_home_button('explore_button', Cypress.env('login_page'))
  })

  it('As a teacher: Is able to click all menubar buttons', () => {
    loginForTeacher();
    navigate_home_button('hedy_button', Cypress.env('hedy_page'))
    navigate_home_button('explore_button', Cypress.env('explore_programs_page'))
    navigate_home_button('for_teacher_button', Cypress.env('teachers_page'))
    navigate_home_button('manual_button', Cypress.env('manual_page'))
    navigate_home_button('programs_button', Cypress.env('programs_page'))
  })

  it('As a student: Is able to click all menubar buttons', () => {
    loginForStudent();
    navigate_home_button('hedy_button', Cypress.env('hedy_page'))
    // explore button for a student is tested within the quiz parsons test
    not_navigate_home_button('for_teacher_button')
    not_navigate_home_button('manual_button')
    navigate_home_button('programs_button', Cypress.env('programs_page'))
  })

  it('As a user: Is able to click all menubar buttons', () => {
    loginForUser();
    navigate_home_button('hedy_button', Cypress.env('hedy_page'))
    navigate_home_button('explore_button', Cypress.env('explore_programs_page'))
    not_navigate_home_button('for_teacher_button')
    not_navigate_home_button('manual_button')
    navigate_home_button('programs_button', Cypress.env('programs_page'))
  })
})

function not_navigate_home_button(button)
{
  goToHome();
  cy.getDataCy(button).should('not.exist');
}