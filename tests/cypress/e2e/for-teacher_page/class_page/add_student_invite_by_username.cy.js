import {loginForTeacher, loginForStudent, logout} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to add student by name', () => {
  it('Passes', () => {

    loginForTeacher();
    
    cy.wait(500);
    
    cy.get(':nth-child(1) > #class_view_button').click();

    //delete student1 if in class
    cy.get('.username_cell').then(($div) => {

      if ($div.text().includes('student1')){
        cy.get('#remove-student').click();
        cy.get('#modal-yes-button').click();
      }
    })

    cy.wait(500);

    cy.get('#add-student').click();
    //cy.get('.green-btn').contains("Add students").click();
    cy.get('#invite-student').click();


    cy.get('#modal-prompt-input').type("student1");
    cy.get('#modal-ok-button').click();
 
    //logout:
    cy.wait(500);
    cy.get('.dropdown > .menubar-text > .fas').click();
    cy.get(':nth-child(6) > .dropdown-item').click();

    cy.wait(500);
    loginForStudent();
    cy.wait(500);

    cy.get('.dropdown > .menubar-text > .fas').click();
    cy.get(':nth-child(3) > .dropdown-item').click();
    cy.get('#my-messages').click();
    cy.get('#join-link').click();
    cy.get('.green-btn').contains("Join class").click();
    
    //logout:
    cy.wait(500);
    cy.get('.dropdown > .menubar-text > .fas').click();
    cy.get(':nth-child(4) > .dropdown-item').click();
    cy.wait(500);

    loginForTeacher();
    cy.wait(500);
    cy.get('#class_view_button').click();
    
    cy.get('.username_cell').should(($div) => {
      const text = $div.text()
    
      expect(text).include('student1');
    })

    //expect(cy.get('.username_cell')).to.eq('student1');
    


  })
})
