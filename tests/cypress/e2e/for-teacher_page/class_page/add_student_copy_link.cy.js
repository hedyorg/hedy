import {loginForTeacher, logout} from '../../tools/login/login.js'
describe('Is able to see copy link to add student to class', () => {
  it('Passes', () => {    
    loginForTeacher();
    cy.get(".view_class").first().click();
    cy.get('#add-student').click();
    cy.get('#copy-join-link').should('be.visible').should('be.enabled').click();

  })
})
