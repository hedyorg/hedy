import { loginForStudent, loginForTeacher, loginForUser } from "../tools/login/login";
import { goToHome, navigateHomeButton } from "../tools/navigation/nav";

describe('Navigation buttons', () => {
  it('When not logged in: Is able to click all menubar buttons', () => {
    navigateHomeButton('hedy_button', Cypress.expose('hedy_page'))
  })

  it('As a teacher: Is able to click all menubar buttons', () => {
    loginForTeacher();
    navigateHomeButton('hedy_button', Cypress.expose('hedy_page'))
    navigateHomeButton('for_teacher_button', Cypress.expose('teachers_page'))
    navigateHomeButton('manual_button', Cypress.expose('manual_page'))
    goToHome();
    cy.getDataCy('user_dropdown').find('a.menubar-text').first().click();
    cy.getDataCy('programs_button').click();
    cy.url().should('include', Cypress.expose('programs_page'))
  })

  it('As a student: Is able to click all menubar buttons', () => {
    loginForStudent();
    navigateHomeButton('hedy_button', Cypress.expose('hedy_page'))
    notNavigateHomeButton('for_teacher_button')
    notNavigateHomeButton('manual_button')
    goToHome();
    cy.getDataCy('user_dropdown').find('a.menubar-text').first().click();
    cy.getDataCy('programs_button').click();
    cy.url().should('include', Cypress.expose('programs_page'))
  })

  it('As a user: Is able to click all menubar buttons', () => {
    loginForUser();
    navigateHomeButton('hedy_button', Cypress.expose('hedy_page'))
    notNavigateHomeButton('for_teacher_button')
    notNavigateHomeButton('manual_button')
    goToHome();
    cy.getDataCy('user_dropdown').find('a.menubar-text').first().click();
    cy.getDataCy('programs_button').click();
    cy.url().should('include', Cypress.expose('programs_page'))
  })
})

function notNavigateHomeButton(button) {
  goToHome();
  cy.getDataCy(button).should('not.exist');
}
