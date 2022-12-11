import {loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to go to logs page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button
    cy.get('#add-student').click();
    cy.get('#create-accounts').click(); 
    cy.get(':nth-child(2) > #username').type("student14");
    cy.get(':nth-child(2) > #password').type("123456");
    cy.get(':nth-child(3) > #username').type("student15");
    cy.get(':nth-child(3) > #password').type("123456");
    cy.get(':nth-child(4) > #username').type("student16");
    cy.get(':nth-child(4) > #password').type("123456");
    cy.get(':nth-child(5) > #username').type("student17");
    cy.get(':nth-child(5) > #password').type("123456");
    cy.wait(1000);

    cy.get('#create_accounts_button').click();
    cy.get('#modal-yes-button').click();

    cy.wait(1000);
    

    cy.readFile('cypress/downloads/accounts.csv')

    cy.get('#back_to_class_button').click();
    cy.get('.username_cell').should(($div) => {
      const text = $div.text()
    
      expect(text).include('student13');
    }) 
    
  })
})