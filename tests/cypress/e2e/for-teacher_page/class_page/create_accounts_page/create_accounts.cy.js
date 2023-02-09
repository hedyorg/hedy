import {loginForTeacher} from '../../../tools/login/login.js'
import {createClassAndAddStudents, navigateToClass} from '../../../tools/classes/class.js'

let classname;
let students;

beforeEach(() => {
    loginForTeacher();
    ({classname, students} = createClassAndAddStudents());
})

describe('Is able to add rows to create more accounts', () => {
  it('Passes', () => {
    cy.get('#add_multiple_rows').click();
    cy.get(':nth-child(6) > #username').should('have.value', '');
  })
})

describe('Is able to create new accounts for class', () => {
  it('Passes', () => {
    cy.get('#back_to_class_button').click();
    cy.get('.username_cell').should(($div) => {
      const text = $div.text();
      expect(text).include(students[0]);
    }) 
  })
})

describe('Is able to download login credentials', () => {
    it('Passes', () => {
      cy.readFile('cypress/downloads/accounts.csv');
    })
  })

describe('Is able to generate passwords', () => {
    it('Passes', () => {
        navigateToClass(classname);
        cy.get('#add-student').click();
        cy.get('#create-accounts').click(); 
        cy.get('#toggle_circle').click(); //switches the toggle on so that passwords are generated
        cy.wait(1000);
        cy.get(':nth-child(2) > #password').should('have.length.greaterThan', 0);
    })
})

describe('Is able to go to logs page', () => {
    it('Passes', () => {
      var currentUrl = '';
      navigateToClass(classname);
      cy.url().then(url => {
        currentUrl = url;
        cy.get('#add-student').click();
        cy.get('#create-accounts').click(); 
        cy.get('#back_to_class_button').click();
        cy.wait(1000);
        let statsUrl = Cypress.env('class_page') + currentUrl.substring(currentUrl.indexOf('class/')+6);
        cy.url().should('include', statsUrl); 
      })    
    })
  })

  describe('Is able to remove row', () => {
    it('Passes', () => {
        navigateToClass(classname);
        cy.get('#add-student').click();
        cy.get('#create-accounts').click(); 
        //fills in first row
        cy.get(':nth-child(2) > #username').type("student10");
        cy.get(':nth-child(2) > #password').type("123456");
        cy.wait(1000);
        //checks if the first row is filled
        cy.get(':nth-child(2) > #username').should('have.value', 'student10');
        //deletes the first row
        cy.get(':nth-child(2) > .fill-current > path').click();
        cy.wait(1000);
        //check if the first row is now empty
        cy.get(':nth-child(2) > #username').should('have.value', '');
    })
  })

  describe('Is able to use the reset button', () => {
    it('Passes', () => {
        navigateToClass(classname);
        cy.get('#add-student').click();
        cy.get('#create-accounts').click(); 
        cy.get(':nth-child(2) > #username').type("student10");
        cy.get(':nth-child(2) > #password').type("123456");
        cy.wait(1000);
        cy.get(':nth-child(2) > #username').should('have.value', 'student10');
        cy.get('#reset_button').click();
        cy.wait(1000);
        cy.get(':nth-child(2) > #username').should('have.value', '');
    })
  })