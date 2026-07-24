import { goToTeachersPage } from "../navigation/nav";

export function createClass(classname=`test class ${Math.random()}`)
{
    cy.request({
        method: 'POST',
        url: '/class',
        body: {
            creation_type: 'standard',
            name: classname,
        },
        failOnStatusCode: true,
    }).its('status').should('be.oneOf', [200, 201]);

    cy.visit('/for-teachers/class/all');
    cy.url().should('include', '/for-teachers/class/all');

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
    const seed = Date.now();
    const students = Array.from({length:count}, (_, index) => `student_${index}_${seed}`)
    goToTeachersPage();
    cy.wait(500);

    openClassView(classname);
    cy.wait(500);

    cy.getDataCy('add_student').click();
    cy.getDataCy('create_accounts').click();

    cy.getDataCy('toggle_circle').click();
    const accounts = students.map(function (s) {
      return `${s};123456`;
    }).join('\n');
    cy.getDataCy('create_accounts_input').type(accounts);

    cy.getDataCy('create_accounts_button').click();
    cy.getDataCy('modal_yes_button').click();

    return students;
}

export function openClassView(classname=null){
    cy.visit('/for-teachers/class/all');
    cy.url().should('include', '/for-teachers/class/all');
    cy.getDataCy('view_class_link').should('exist');

    if (classname) {
        cy.getDataCy('view_class_link')
            .contains(classname)
            .invoke('attr', 'href')
            .then((href) => {
                const classId = href.split('/').pop();
                cy.visit(`/for-teachers/legacy/class/${classId}`);
            });
    }
}

export function openClass(classname) {
    cy.getDataCy('view_class_link')
        .contains(classname)
        .invoke('attr', 'href')
        .then((href) => {
            const classId = href.split('/').pop();
            cy.visit(`/for-teachers/legacy/class/${classId}`);
        });
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
}

export function createClassAndAddStudents(){
    const classname = createClass();
    const students = addStudents(classname, 4);
    return {classname, students};
}

export function navigateToClass(classname=null) {
    goToTeachersPage();
    cy.wait(500);
    openClassView(classname);
    if (!classname) {
        cy.getDataCy('view_class_link')
            .first()
            .invoke('attr', 'href')
            .then((href) => {
                const classId = href.split('/').pop();
                cy.visit(`/for-teachers/legacy/class/${classId}`);
            });
    }

    cy.wait(500);
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())
}

export function selectLevel(level) {
    cy.getDataCy('levels_dropdown').select(level);
  }

export default {createClassAndAddStudents};
