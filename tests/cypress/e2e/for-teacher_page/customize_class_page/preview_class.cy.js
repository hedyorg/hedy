import { createClass, openClassView } from '../../tools/classes/class.js';
import { loginForTeacher } from '../../tools/login/login.js'
import { goToHedyPage, goToTeachersPage, clickAdventureIndexButton } from '../../tools/navigation/nav.js';

const teachers = ["teacher1", "teacher4"];

teachers.forEach((teacher) => {
    it(`${teacher } is able to preview class`, () => {
        loginForTeacher(teacher);
        // go to main hedy page in "normal mode"
        goToHedyPage();
        clickAdventureIndexButton();
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
        clickAdventureIndexButton();
        cy.getDataCy('ask_command').should("be.visible");
        // check that the print_command is absent
        cy.getDataCy('print_command').should("not.be.visible");
        cy.getDataCy('exit_preview_class_banner').click();

        // we now expect the normal situation to be restored
        goToHedyPage();
        cy.getDataCy('preview_class_banner').should("not.exist");
        clickAdventureIndexButton();
        cy.getDataCy('print_command');
    })
});
