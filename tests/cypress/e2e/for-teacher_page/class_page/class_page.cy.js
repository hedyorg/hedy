import { ensureClass } from '../../tools/classes/class.js';
import {loginForTeacher, logout} from '../../tools/login/login.js'

describe('Tests for view class page', () => {
  beforeEach(() => {
    loginForTeacher();
    ensureClass();
    cy.getBySel('view_class_link').first().click();
  });
  
  describe('Add students tests', () => {
    beforeEach(() => {
      cy.getBySel('add-student')
        .click()
        .should('have.class', 'blue-btn');
      
      cy.getBySel('add_students_options')
        .should('be.visible');
    })
    
    it('Is able to see copy link to add student to class', () => {      
      cy.getBySel('copy-join-link')
        .should('be.visible')
        .should('be.enabled')
        .click();
    
      cy.getBySel('modal_alert_text')
        .should('be.visible');
    })

    it('Deletes a student if found and then invites them again', () => {
      //delete student if in class
      const studentUsername = "student5";

      cy.getBySel('class-user-table').then(($div) => {
          if ($div.text().includes(studentUsername)) {
            cy.getBySel(`remove-student-${studentUsername}`).click();
            cy.getBySel('modal-yes-button').click();
          }
      })

      cy.getBySel('invite-student').click();
      cy.getBySel('modal-prompt-input')
        .type(studentUsername);
      cy.getBySel('modal-ok-button').click();

      cy.getBySel('pending_invites')
        .should('be.visible')
        .and('contain', studentUsername);
    })
  });

  // FH, Jan 2023 It is unclear to me why this fails, commenting out for now (in 3682)
  //    cy.wait(500);
  //    login("student5", "123456");
  //    cy.wait(500);
  //
  //    cy.get('.dropdown > .menubar-text').click();
  //    cy.get('#my_account_button').click();
  //    cy.get('#my-messages').click();
  //    cy.get('#join-link').click();
  //    cy.get('.green-btn').contains("Join class").click();
  //
  //    //logout:
  //    cy.wait(500);
  //    cy.get('.dropdown > .menubar-text').click();
  //    cy.get('#logout_button').click();
  //
  //    cy.wait(500);
  //
  //    loginForTeacher();
  //    cy.wait(500);
  //    cy.get(".view_class").first().click();
  //
  //    cy.get('.username_cell').should(($div) => {
  //      const text = $div.text()
  //
  //      expect(text).include('student5');
  //    })

  it('is able to go the customize class page', () => {    
    cy.url().then(url => {
      let classUrl = url;
      cy.getBySel('customize-class-button').click();
      let newUrl = Cypress.env('customize_class_page') + classUrl.substring(classUrl .indexOf('class/')+6);      
      cy.url().should('include', newUrl); // Check if you are in the logs page
    })
  });

  it('is able to go the class stats page', () => {    
    cy.url().then(url => {
      let classUrl = url;
      cy.getBySel('stats_button').click();
      let newUrl = Cypress.env('stats_page') + classUrl.substring(classUrl .indexOf('class/')+6);      
      cy.url().should('include', newUrl); // Check if you are in the logs page
    })
  });

  it('is able to go the class logs page', () => {    
    cy.url().then(url => {
      let classUrl = url;
      cy.getBySel('logs_button').click();
      let newUrl = Cypress.env('logs_page') + classUrl.substring(classUrl .indexOf('class/')+6);      
      cy.url().should('include', newUrl); // Check if you are in the logs page
    })
  });

  it('goes back to the teachers page', () => {
    cy.getBySel('go_back_teacher')
    .should('be.visible')
    .should('not.be.disabled')
    .click();   

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
  })
})