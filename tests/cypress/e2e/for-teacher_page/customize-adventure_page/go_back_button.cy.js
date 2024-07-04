import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

const teachers = ["teacher1", "teacher4"];

teachers.forEach((teacher) => {
  it(`Preview button test for ${teacher}`, () => {
    loginForTeacher(teacher);
    goToEditAdventure();

    cy.getDataCy('go_back_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
    })
})