import { loginForTeacher } from "../login/login";
import { goToTeachersPage } from "../navigation/nav";

export function createClass()
{
    // Click 'Create new class' button
    cy.get('#teacher_classes > .green-btn').click();

    // Type 'test class'
    cy.get('#modal-prompt-input').type("test class");

    // Click 'ok'
    cy.get('#modal-ok-button').click();

    goToTeachersPage();
}

export default {createClass};