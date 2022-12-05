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
})
