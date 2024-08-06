import { goToTeachersPage } from "../navigation/nav";

export function createClass(classname=`test class ${Math.random()}`)
{
    goToTeachersPage();
    cy.wait(500);

    cy.getDataCy('create_class_button').click();
    cy.getDataCy('modal_prompt_input').type(classname);
    cy.getDataCy('modal_ok_button').click();

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

    cy.getDataCy('view_class_link').then(viewClassLink => {
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

    openClassView(classname);
    cy.wait(500);

   cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())
    cy.getDataCy('add_student').click();
    cy.getDataCy('create_accounts').click();
    cy.wrap(students).each((student, index) => {
      cy.getDataCy(`username_${index + 1}`).type(student);
      cy.getDataCy(`password_${index + 1}`).type('123456');
    })
    cy.getDataCy('create_accounts_button').click();
    cy.getDataCy('modal_yes_button').click();

    return students;
}

export function openClassView(classname=null){
    cy.getDataCy('view_class_link').then($viewClass => {
        if (!$viewClass.is(':visible')) {
            cy.getDataCy('view_classes').click();
        }
      });
    if (classname) {
        openClass(classname)
    }
}

export function openClass(classname) {
    cy.getDataCy('view_class_link').contains(classname).click();
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide());
}

export function removeCustomizations(){
    cy.intercept('/for-teachers/restore-customizations*').as('restoreCustomizations');      
    cy.getDataCy('customize_class_button').click();
    cy.getDataCy('remove_customizations_button').click();
    cy.getDataCy('modal_yes_button').click();
    cy.wait('@restoreCustomizations');
}

export function addCustomizations(classname){
    cy.intercept('/for-teachers/customize-class/*').as('updateCustomizations');
    goToTeachersPage();

    cy.wait(500);
    openClassView(classname);
    cy.getDataCy('customize_class_button').click();
    cy.getDataCy('opening_date_container').should("not.be.visible")
    cy.getDataCy('opening_date_label').click();
    cy.getDataCy('opening_date_container').should("be.visible")
    cy.getDataCy('enable_level_7').parent('.switch').click();

    cy.wait(1000);
    cy.wait('@updateCustomizations');

    cy.getDataCy('back_to_class').click();
    cy.getDataCy('go_back_button').click();
}

export function createClassAndAddStudents(){
    const classname = createClass();
    const students = addStudents(classname, 4);
    return {classname, students};
}

export function navigateToClass(classname=null) {
    goToTeachersPage();
    cy.wait(500);
    openClassView();
    if (classname) {
        cy.getDataCy('view_class_link').contains(classname).click();
    } else {
        cy.getDataCy('view_class_link').first().click();
    }
    cy.wait(500);
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())
}

export function selectLevel(level) {
    cy.getDataCy("levels_dropdown").select(level);
}

export default {createClassAndAddStudents};