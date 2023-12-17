import { createClass } from '../../tools/classes/class.js';
import {loginForTeacher} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

describe('Is able to preview class', () => {
  it('Passes', () => {
    loginForTeacher();
    // go to main hedy page in "normal mode"
    cy.get("#hedybutton").click();
    // we expect a "print_command" tab
    cy.get("#dropdown_level_button").click()
    cy.get("#level_button_1").click()
    cy.get("#adventures-buttons [data-tab='print_command']")
    // assert that no preview_class_banner is shown right now
    cy.get("[data-cy='preview_class_banner']").should("not.exist");

    // now we create a custom class
    let className = createClass();
    goToTeachersPage();
    // we navigate to our custom class
    // if this ever fails, it might be due to pagination
    cy.get("a.view_class").contains(className).click();
    cy.get("button#customize-class-button").click();
    cy.get("#levels-dropdown").select("1");
    // we remove the print command from our custom class
    cy.get("div[data-cy='print_command'] span").click();
    // we preview the class without the print command
    cy.get("a[data-cy='preview_class_link']").click()
    // check the banner is there
    cy.get("[data-cy='preview_class_banner']")
    // check the is_command is there
    cy.get("#adventures-buttons [data-tab='is_command']")
    // check that the print_command is absent
    cy.get("#adventures-buttons [data-tab='print_command']").should("not.exist")

    // exit preview mode
    cy.get("[data-cy='preview_class_banner'] a").click()

    // we now expect the normal situation to be restored
    cy.get("#hedybutton").click();
    cy.get("#dropdown_level_button").click()
    cy.get("#level_button_1").click()
    cy.get("#adventures-buttons [data-tab='print_command']")
    cy.get("[data-cy='preview_class_banner']").should("not.exist");
  })
})
