import {loginForTeacher} from '../../../tools/login/login.js'
import {createClass} from '../../../tools/classes/class.js'


describe('Is able to download login credentials', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(".view_class").first().click(); // Press view class button
    cy.get('#add-student').click();
    cy.get('#create-accounts').click(); 
    var levelarray = Array.from({length:4},(v, k)=>k+1) // length reflects how many rows to fill
    cy.wrap(levelarray).each((index) => {
      cy.get(':nth-child(' +(index + 1) + ') > #username').type("student" + '0' + index)
      cy.get(':nth-child(' +(index + 1) + ') > #password').type('123456')
    })
    cy.wait(1000);

    cy.get('#download_credentials_yes').check()

    cy.get('#create_accounts_button').click();
    cy.get('#modal-yes-button').click();

    cy.wait(1000);
    

    cy.readFile('cypress/downloads/accounts.csv')

    cy.get('#back_to_class_button').click();
    cy.get('.username_cell').should(($div) => {
      const text = $div.text()
    
      expect(text).include('student01');
    }) 
    
  })
})