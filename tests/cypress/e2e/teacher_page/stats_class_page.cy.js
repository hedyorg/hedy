import {loginForAdmin, loginForTeacher} from '../tools/login/login.js'
import {createClass} from '../tools/classes/class.js'

describe('Is able to go back to teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(":nth-child(1) > :nth-child(3) > .no-underline").click();
    cy.get("cy.get(':nth-child(1) > .green-btn')").click();
     
    
  })
})