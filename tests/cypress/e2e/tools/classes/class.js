import { goToTeachersPage } from "../navigation/nav";

export function createClass()
{
    const classname = `test class ${Math.random()}`;

    goToTeachersPage();
    cy.wait(500);

    cy.get('#create_class_button').click();
    cy.get('#modal-prompt-input').type(classname);
    cy.get('#modal-ok-button').click();

    goToTeachersPage();
    cy.wait(500);

    return classname;
}

/**
 * Make sure that at least one class exists
 *
 * Create a class if one doesn't exist already.
 *
 * Use as follows:
 *
 *      const className = await ensureClass();
 *
 * In an `async` function.
 */
export function ensureClass()
{
    let classname = `test class ${Math.random()}`;
    goToTeachersPage();

    cy.getBySel('view_class_link').then(viewClassLink => {
        if (viewClassLink.length === 0) {
            createClass();
        } else {
            classname = viewClassLink.text();
        }
    });

    return classname
}

export function addStudents(classname, count) {
    const students = Array.from({length:count}, (_, index) => `student_${index}_${Math.random()}`)

    goToTeachersPage();
    cy.wait(500);

    cy.get(".view_class").then($viewClass => {
        if (!$viewClass.is(':visible')) {
            cy.get("#view_classes").click();
        }
    });
    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
    cy.wait(500);

    cy.get('body').then($b => $b.find("#survey")).then($s => $s.length && $s.hide())
    cy.get('#add-student').click();
    cy.get('#create-accounts').click();
    cy.wrap(students).each((student, index) => {
      cy.get(`:nth-child(${(index + 2)}) > #username`).type(student);
      cy.get(`:nth-child(${(index + 2)}) > #password`).type('123456');
    })
    cy.get('#create_accounts_button').click();
    cy.get('[data-cy="modal_yes_button"]').click();

    return students;
}

export function addCustomizations(classname){
    cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');      
    goToTeachersPage();

    cy.get(".view_class").then($viewClass => {
        if (!$viewClass.is(':visible')) {
            cy.get("#view_classes").click();
        }
    });
    cy.get(".view_class").contains(classname).click();
    cy.get('#customize-class-button').click();
    cy.get("#opening_date_container").should("not.be.visible")
    cy.get("#opening_date_label").click();
    cy.get("#opening_date_container").should("be.visible")
    cy.get('#enable_level_7').parent('.switch').click();

    cy.wait(1000)
    cy.wait('@updateCustomizations').should('have.nested.property', 'response.statusCode', 200);

    cy.get("#back_to_class").click();
}

export function createClassAndAddStudents(){
    const classname = createClass();
    const students = addStudents(classname, 4);
    return {classname, students};
}

export function navigateToClass(classname) {
    goToTeachersPage();
    cy.wait(500);
    cy.get(".view_class").then($viewClass => {
        if (!$viewClass.is(':visible')) {
            cy.get("#view_classes").click();
        }
    });
    cy.get(".view_class").contains(new RegExp(`^${classname}$`)).click();
    cy.wait(500);
    cy.get('body').then($b => $b.find("#survey")).then($s => $s.length && $s.hide())
}

export default {createClassAndAddStudents};