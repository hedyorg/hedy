import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Level Field test', () => {
  for (const teacher of ["teacher1", "teacher4"]) { 
    it(`passes: ${teacher}`, () => {
      loginForTeacher(teacher);
      goToEditAdventure();

      // Tests level field interaction
      cy.get('#custom_adventure_level')
        .should('be.visible')
        .should('not.be.disabled')
        .select('1')
        .should('have.value', '1');
    })
  }
})
