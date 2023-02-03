import {loginForTeacher} from '../../../tools/login/login.js'
import {createClassAndAddStudents} from '../../../tools/classes/class.js'


describe('Is able to download login credentials', () => {
  it('Passes', () => {
    loginForTeacher();
    createClassAndAddStudents();
    cy.readFile('cypress/downloads/accounts.csv')
  })
})