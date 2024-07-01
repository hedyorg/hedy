import { loginForStudent, loginForTeacher } from "../tools/login/login";
import { goToHome } from "../tools/navigation/nav";

beforeEach(() => {
  goToHome();
})

describe('Start buttons', () => {
  it('Should be able to click on start learning button', () => {
    cy.getDataCy('start_learning_button').click();
    cy.url().should('include', 'hedy');
    })

  it('Should be able to click on start teaching button', () => {
    // teaching button first test not signed in
    cy.getDataCy('start_teaching_button').click();
    cy.url().should('include', 'signup?teacher=true');

    // then test signed in as teacher
    loginForTeacher();
    goToHome();
    cy.getDataCy('start_teaching_button').click();
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/for-teachers");
    })

    // then test signed in as student
    loginForStudent();
    goToHome();
    cy.getDataCy('start_teaching_button').click();
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/my-profile");
    })
  })
})