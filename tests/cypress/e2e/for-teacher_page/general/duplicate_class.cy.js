import { createClass, addCustomizations } from '../../tools/classes/class.js';
import { loginForTeacher, logout} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

describe('Duplicate class tests', () => {
  it('Is able to duplicate class without adding second teachers', () => {
    loginForTeacher();
    const classname = createClass();
    addCustomizations(classname);
    goToTeachersPage();
    const duplicate_class = `test class ${Math.random()}`;

    // Click on duplicate icon
    cy.get('.no-underline > .fas').first().click();

    //`Check for Second Teachers option
    cy.get('#modal-no-button').should('be.enabled').click();

    // Checks for input field
    cy.get('#modal-prompt-input').type(duplicate_class);
    cy.get('#modal-ok-button').click();

    cy.reload();

    cy.get(".view_class").contains(duplicate_class).click();
    cy.get("#customize-class-button").click();
    cy.get("#enable_level_7").should('be.enabled');
    logout();
  })

  it('Is able to duplicate class with adding second teachers', () => {
    loginForTeacher();
    const classname = createClass();
    addCustomizations(classname);
    goToTeachersPage();
    const duplicate_class = `test class ${Math.random()}`;

    cy.get('.no-underline > .fas').first().click();

    cy.get('#modal-yes-button').should('be.enabled').click();

    cy.get('#modal-prompt-input').type(duplicate_class);
    cy.get('#modal-ok-button').click();

    cy.reload();

    cy.get(".view_class").contains(duplicate_class).click();
    cy.get("#invites-block").should('be.visible');
    cy.get("#customize-class-button").click();
    cy.get("#enable_level_7").should('be.enabled');
  })
})
