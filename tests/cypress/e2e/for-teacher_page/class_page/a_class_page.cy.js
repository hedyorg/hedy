import { ensureClass } from '../../tools/classes/class.js';
import {loginForTeacher, logout} from '../../tools/login/login.js'

describe('Tests for view class page', () => {
  beforeEach(() => {
    loginForTeacher();
    ensureClass();
    cy.getBySel('view_class_link').first().click();
  });
  
  it('Is able to see copy link to add student to class', () => {
    cy.getBySel('add-student')
      .click()
      .should('have.class', 'blue-button');   
    
    cy.getBySel('copy-join-link')
      .should('be.visible')
      .should('be.enabled')
      .click();
    
    cy.getBySel('modal_alert_text').should('be.visible');
  })

  it('Is able to invite a student by username', () => {
    //delete student if in class
    const studentUsername = "student5";

    cy.getBySel('class-user-table').then(($div) => {
        if ($div.text().includes(studentUsername)){
          cy.getBySel('remove-student').click();
          cy.getBySel('modal-yes-button').click();
        }
    })

    cy.getBySel('add-student').click();
    cy.getBySel('invite-student').click();
    cy.getBySel('modal-prompt-input')
      .type(studentUsername);
    cy.get('#modal-ok-button').click();
  })
})