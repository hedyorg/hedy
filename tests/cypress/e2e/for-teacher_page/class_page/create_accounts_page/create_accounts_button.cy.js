import {loginForTeacher} from '../../../tools/login/login.js'
import {createClassAndAddStudents} from '../../../tools/classes/class.js'


describe('Is able to create new accounts for class', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    const {_, students} = createClassAndAddStudents();
    cy.get('#back_to_class_button').click();
    cy.get('.username_cell').should(($div) => {
      const text = $div.text()
      expect(text).include(students[0]);
    }) 
  })
})