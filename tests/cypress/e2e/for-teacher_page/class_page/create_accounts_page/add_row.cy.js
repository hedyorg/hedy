import {loginForTeacher} from '../../../tools/login/login.js'
import {createClassAndAddStudents} from '../../../tools/classes/class.js'


describe('Is able to add rows to create more accounts', () => {
  it('Passes', () => {
    loginForTeacher();
    createClassAndAddStudents();
    cy.get('#add_multiple_rows').click();
    cy.get(':nth-child(6) > #username').should('have.value', '')
  })
})