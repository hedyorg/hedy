import { createClass } from '../../tools/classes/class.js';
import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

it('Is able to create new class', () => {
    loginForTeacher();
    createClass();
    goToTeachersPage();

    // Assert that there is a class that's called: test class
    //
    cy.get('tbody > :nth-child(1) > .px-4').should("contain.text", "test class");
});