import {loginForTeacher} from '../../../tools/login/login.js'
import {addStudents, navigateToClass} from '../../../tools/classes/class.js'

let classname = "CLASS1";
let students;


beforeEach(() => {
  loginForTeacher("teacher4");
})

before(() => {
  loginForTeacher("teacher4");
  students = addStudents(classname, 4);
})

describe('Testing second teacher accounts', () => {
  it('Is able to create new accounts for class', () => {
    navigateToClass(classname);
    cy.getDataCy(`student_${students[0]}`).should('include.text', students[0])
  })

  it('Is able to download login credentials', () => {
    cy.readFile('cypress/downloads/accounts.csv');
  })

  it('Is able to generate passwords', () => {
    navigateToClass(classname);
    cy.getDataCy('add_student').click();
    cy.getDataCy('create_accounts').click();
    cy.getDataCy('toggle_circle').click(); //switches the toggle on so that passwords are generated
    cy.wait(1000);
    cy.get(':nth-child(2) > [data-cy="password"]').should('have.length.greaterThan', 0);
  })

  it('Is able to go to logs page', () => {
    var currentUrl = '';
    navigateToClass(classname);
    cy.url().then(url => {
      currentUrl = url;
      cy.getDataCy('add_student').click();
      cy.getDataCy('create_accounts').click();
      cy.getDataCy('go_back_button').click();
      cy.wait(1000);
      let statsUrl = Cypress.env('class_page') + currentUrl.substring(currentUrl.indexOf('class/')+6);
      cy.url().should('include', statsUrl); 
    })    
  })

  it('Is able to remove row', () => {
    navigateToClass(classname);
    cy.getDataCy('add_student').click();
    cy.getDataCy('create_accounts').click();
    //fills in first row
    cy.get(':nth-child(2) > [data-cy="username"]').type("student10");
    cy.get(':nth-child(2) > [data-cy="password"]').type("123456");
    cy.wait(1000);
    //checks if the first row is filled
    cy.get(':nth-child(2) > [data-cy="username"]').should('have.value', 'student10');
    //deletes the first row
    cy.get(':nth-child(2) > .fill-current > path').click();
    cy.wait(1000);
    //check if the first row is now empty
    cy.get(':nth-child(2) > [data-cy="username"]').should('have.value', '');
  })

  it('Is able to use the reset button', () => {
    navigateToClass(classname);
    cy.getDataCy('add_student').click();
    cy.getDataCy('create_accounts').click();
    cy.get(':nth-child(2) > [data-cy="username"]').type("student10");
    cy.get(':nth-child(2) > [data-cy="password"]').type("123456");
    cy.wait(1000);
    cy.get(':nth-child(2) > [data-cy="username"]').should('have.value', 'student10');
    cy.getDataCy('reset_button').click();
    cy.wait(1000);
    cy.get(':nth-child(2) > [data-cy="username"]').should('have.value', '');
  })
})