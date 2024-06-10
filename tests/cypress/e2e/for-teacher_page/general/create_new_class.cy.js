import { createClass, openClassView } from '../../tools/classes/class.js';
import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

it('Is able to create new class', () => {
    const classname = "TEST_CLASS"
    loginForTeacher();
    createClass(classname);
    goToTeachersPage();
    openClassView();

    // Assert that there is a class with the new classname
    cy.getDataCy('view_class_link').should("contain.text", classname);
});