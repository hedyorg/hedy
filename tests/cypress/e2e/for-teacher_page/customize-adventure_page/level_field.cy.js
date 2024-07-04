import { loginForTeacher } from '../../tools/login/login.js'
import { goToEditAdventure } from '../../tools/navigation/nav.js'

const levels = ["3", "5"];
const teachers = ["teacher1", "teacher4"];

levels.forEach((level) => {
  teachers.forEach((teacher) => {
    it(`${teacher} can select level ${level}`, () => {
      loginForTeacher(teacher);
      goToEditAdventure();

      // Tests level field interaction
      cy.getDataCy('level_select')
        .should('be.visible')
        .should('not.be.disabled')
        .click()
      
      cy.get(`#levels_dropdown > div.option[data-value="${level}"]`)
        .click()
      
      cy.get(`#levels_dropdown > div.option[data-value="${level}"]`)
        .should('have.class', 'selected')
    })
  })
})
