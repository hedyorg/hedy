import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Levels Dropdown Select test', () => {
  const levels = ["3", "5"];
  for (const level of levels) {
    for (const teacher of ["teacher1", "teacher4"]) { 
      it(`${teacher} can select level ${level}`, () => {
        loginForTeacher(teacher);
        goToEditAdventure();

        // Tests level field interaction
        cy.get('#custom_adventure_levels_container')
          .should('be.visible')
          .should('not.be.disabled')
          .click()
        
        cy.wait(400)

        cy.get("div[data-te-select-dropdown-ref]")
          .should('be.visible')
        
        cy.get("div[role='option']")
          .contains(level)
          .click()
        
        cy.get("div[role='option']")
          .contains(level)
          .parent()
          .should("have.attr", "data-te-select-selected")
      })
    }
  }
})
