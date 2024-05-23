import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Agree public checkbox test', () => {
  for (const teacher of ["teacher1", "teacher4"]) { 
    it(`passes: ${teacher}`, () => {
      loginForTeacher(teacher);
      goToEditAdventure();

      // navigate to the editor's view
      cy.getBySel("adventure").click();

      cy.get('#agree_public')
        .should('be.visible')
        .should('not.be.disabled')
        .check()
        .should('be.checked')
        .uncheck()
        .should('not.be.checked');
    })
  }
})
