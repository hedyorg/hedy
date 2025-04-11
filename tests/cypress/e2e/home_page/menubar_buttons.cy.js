import { loginForStudent, loginForTeacher, loginForUser } from "../tools/login/login";
import { goToHome, navigateHomeButton } from "../tools/navigation/nav";

describe('Navigation buttons', () => {
  it('When not logged in: Is able to click all menubar buttons', () => {
    navigateHomeButton('hedy_button', Cypress.env('hedy_page'))
  })

  it('As a teacher: Is able to click all menubar buttons', () => {
    loginForTeacher();
    navigateHomeButton('hedy_button', Cypress.env('hedy_page'))
    navigateHomeButton('for_teacher_button', Cypress.env('teachers_page'))
    navigateHomeButton('manual_button', Cypress.env('manual_page'))
    navigateHomeButton('programs_button', Cypress.env('programs_page'))
  })

  it('As a student: Is able to click all menubar buttons', () => {
    loginForStudent();
    navigateHomeButton('hedy_button', Cypress.env('hedy_page'))
    notNavigateHomeButton('for_teacher_button')
    notNavigateHomeButton('manual_button')
    navigateHomeButton('programs_button', Cypress.env('programs_page'))
  })

  it('As a user: Is able to click all menubar buttons', () => {
    loginForUser();
    navigateHomeButton('hedy_button', Cypress.env('hedy_page'))
    notNavigateHomeButton('for_teacher_button')
    notNavigateHomeButton('manual_button')
    navigateHomeButton('programs_button', Cypress.env('programs_page'))
  })
})

function notNavigateHomeButton(button)
{
  goToHome();
  cy.getDataCy(button).should('not.exist');
}
