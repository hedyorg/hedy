import {loginForTeacher, loginForStudent, logout} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to add student by name', () => {
  it('Passes', () => {

    loginForTeacher();
    
    cy.wait(500);
   
    cy.get(".view_class").first().click();

    //delete student1 if in class
  
    cy.get('#class-user-table').then(($div) => {

        if ($div.text().includes('student1')){
          cy.get('#remove-student').click();
          cy.get('#modal-yes-button').click();
        }
    })

    cy.wait(500);

    cy.get('#add-student').click();

    cy.get('#invite-student').click();

    cy.get('#modal-prompt-input').type("student1");
    cy.get('#modal-ok-button').click();
 
    //logout:
    cy.wait(500);
    cy.get('.dropdown > .menubar-text').click();
    cy.get('#logout_button').click();

    cy.wait(500);
    loginForStudent();
    cy.wait(500);

    cy.get('.dropdown > .menubar-text').click();
    cy.get('#my_account_button').click();
    cy.get('#my-messages').click();
    cy.get('#join-link').click();
    cy.get('.green-btn').contains("Join class").click();
    
    //logout:
    cy.wait(500);
    cy.get('.dropdown > .menubar-text').click();
    cy.get('#logout_button').click();

    cy.wait(500);

    loginForTeacher();
    cy.wait(500);
    cy.get(".view_class").first().click();
    
    cy.get('.username_cell').should(($div) => {
      const text = $div.text()
    
      expect(text).include('student1');
    }) 


  })
})
