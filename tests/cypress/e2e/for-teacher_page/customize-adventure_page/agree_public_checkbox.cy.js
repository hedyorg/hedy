import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

const teachers = ["teacher1", "teacher4"];

teachers.forEach((teacher) => {
  it(`Agree public checkbox test for ${teacher}`, () => {
    loginForTeacher(teacher);
    goToEditAdventure();

    cy.get('#agree_public')
      .should('be.visible')
      .should('not.be.disabled')
      .check()
      .should('be.checked')
      .uncheck()
      .should('not.be.checked');
  })
})
