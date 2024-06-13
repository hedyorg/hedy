import { createClass, openClassView, selectLevel } from '../../tools/classes/class.js';
import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

// Do we also want this to be tested for a second_teacher?
it('Is able to preview class', () => {
    loginForTeacher();
    // go to main hedy page in "normal mode"
    cy.getDataCy('hedybutton').click();
    cy.getDataCy('print_command').should("be.visible");
    cy.getDataCy('ask_command').should("be.visible");
    // assert that no preview_class_banner is shown right now
    cy.getDataCy('preview_class_banner').should("not.exist");

    // create a custom class
    let className = createClass();
    goToTeachersPage();
    openClassView(className);
    cy.getDataCy('customize_class_button').click();

    cy.getDataCy('hide_adv_print_command').click();
    cy.getDataCy('preview_class_link').click();
    cy.getDataCy('preview_class_banner').should("be.visible");
    cy.getDataCy('ask_command').should("be.visible");
    // check that the print_command is absent
    cy.getDataCy('print_command').should("not.exist");
    cy.getDataCy('exit_preview_class_banner').click();

    // we now expect the normal situation to be restored
    cy.getDataCy('hedybutton').click();
    cy.getDataCy('print_command');
    cy.getDataCy('preview_class_banner').should("not.exist");
})
