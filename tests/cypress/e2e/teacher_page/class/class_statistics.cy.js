import {loginForTeacher} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);

    createClass();

    
    
    cy.get(':nth-child(3) > .no-underline').click();

    cy.get('.green-btn').contains('Class statistics').click();
  })
})
