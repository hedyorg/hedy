import { loginForTeacher } from '../../tools/login/login.js'
import { goToEditAdventure } from '../../tools/navigation/nav.js'

describe('Levels Dropdown Select test', () => {
  const levels = ["3", "5"];
  for (const level of levels) {
    for (const teacher of ["teacher1", "teacher4"]) {
      it(`${teacher} can select level ${level}`, () => {
        loginForTeacher(teacher);
        goToEditAdventure();

        // Tests level field interaction
        cy.get("#levels_dropdown")
          .should('be.visible')
          .should('not.be.disabled')
          .click()
        
        cy.get(`#levels_dropdown > div > div > div.option[data-value="${level}"`)
          .click()
        
        cy.get(`#levels_dropdown > div > div > div.option[data-value="${level}"`)
          .should('have.class', 'selected')
      })
    }
  }
})
