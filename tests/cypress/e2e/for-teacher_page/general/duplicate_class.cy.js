import { createClass } from '../../tools/classes/class.js';
import {loginForTeacher} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

describe('Is able to click on duplicate class', () => {
  it('Passes', () => {
    loginForTeacher();
    createClass();
    goToTeachersPage();

    // Click on duplicate icon
    cy.get('.no-underline > .fas').first().click();

    // Checks for input field
    cy.get('#modal-prompt-input').type('test class 2');
    cy.get('#modal-ok-button').click();

    goToTeachersPage();
  })

  it("Second teacher can duplicate main teacher's class", () => {
    loginForTeacher("teacher4");
    goToTeachersPage();

    // Take actions only when teacher2 is a second teacher; i.e., having teacher1 as a teacher.
    cy.get("#teacher_classes tbody tr")
      .each(($tr, i) => {
        if ($tr.text().includes("teacher1")) {
          // Click on duplicate icon
          cy.get(`tbody :nth-child(${i+1}) .no-underline > .fas`).click();
          
          // Checks for input field
          cy.get('#modal-prompt-input').type(' teacher4');
          cy.get('#modal-ok-button').click(); 
        }
      })
    
    goToTeachersPage();
  })
})
