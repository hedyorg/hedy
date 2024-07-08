import { loginForTeacher } from '../../tools/login/login.js'
import { createAdventure } from '../../tools/adventures/adventure.js'
import { createClass } from '../../tools/classes/class.js'

const className = 'test'
const advName = 'test'

it('Is able to rename adventure, select a class, select levels', () => {
  loginForTeacher();
  createClass(className);
  createAdventure();
  
  cy.getDataCy('custom_adventure_name').clear().type(advName)
  cy.getDataCy('classes_select').click()
  cy.wait(500)
  cy.getDataCy(`${className}`).click()
  cy.getDataCy('classes_select').click()


  cy.getDataCy('level_select').click()
  cy.wait(500)
  cy.getDataCy('1').click()
  cy.getDataCy('level_select').click()

  cy.getDataCy('language_select').click()
  cy.wait(500)
  cy.getDataCy('English').click()
})
