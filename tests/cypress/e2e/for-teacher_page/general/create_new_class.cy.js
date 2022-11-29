import { createClass } from '../../tools/classes/class.js';
import {loginForTeacher} from '../../tools/login/login.js'
import { goToPage, goToTeachersPage } from '../../tools/navigation/nav.js';

describe('Is able to create new class', () => {
  it('Passes', () => {
    loginForTeacher();
    createClass();
    goToTeachersPage();

    // Assert that there is a class that's called: test class
    //
    cy.get('tbody > :nth-child(1) > .px-4').should("contain.text", "test class");
});
});