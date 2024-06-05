import { createClass, openClassView } from '../../tools/classes/class.js';
import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';

function goToLevel(targetLevel) {
  let button = cy.getDataCy('dropdown_level_button');
  button.invoke('text').then((buttonText) => {
    if (!buttonText.includes(`Level ${targetLevel}`)) {
      cy.getDataCy('dropdown_level_button').click();
      cy.getDataCy(`level_button_${targetLevel}`).click();
    }
  })
}

it('Is able to preview class', () => {
    loginForTeacher();
    // go to main hedy page in "normal mode"
    cy.getDataCy('hedybutton').click();

    goToLevel(1);
    // we expect a "print_command" and an "ask_command" tab
    cy.get("#adventures_buttons [data-tab='print_command']");
    cy.get("#adventures_buttons [data-tab='ask_command']");
    // assert that no preview_class_banner is shown right now
    cy.getDataCy('preview_class_banner').should("not.exist");

    // now we create a custom class
    let className = createClass();
    goToTeachersPage();
    // we navigate to our custom class
    // if this ever fails, it might be due to pagination
    openClassView();
    cy.get("a.view_class").contains(className).click();
    cy.getDataCy('customize_class_button').click();
    cy.getDataCy('levels_dropdown').select("1");
    // we remove the print command from our custom class
    cy.get("div[data-cy='print_command'] span").click();
    // we preview the class without the print command
    cy.getDataCy("preview_class_link").click();
    // check the banner is there
    cy.getDataCy('preview_class_banner');
    // check the is_command is there
    cy.get("#adventures_buttons [data-tab='ask_command']");
    // check that the print_command is absent
    cy.get("#adventures_buttons [data-tab='print_command']").should("not.exist");

    // exit preview mode
    cy.get('[data-cy="preview_class_banner"] a').click();

    // we now expect the normal situation to be restored
    cy.getDataCy('hedybutton').click();
    goToLevel(1);
    cy.get("#adventures_buttons [data-tab='print_command']");
    cy.getDataCy('preview_class_banner').should("not.exist");
})
