import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Preview button test', () => {
  for (const teacher of ["teacher1", "teacher2"]) { 
    it(`passes: ${teacher}`, () => {
      loginForTeacher(teacher);
      goToEditAdventure();

      cy.get('#go_back_button')
        .should('be.visible')
        .should('not.be.disabled')
        .click();

      cy.url()
        .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
    })
  }
})
