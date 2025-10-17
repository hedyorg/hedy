import { createAdventure, openAdventureView } from "../tools/adventures/adventure";
import { createClass, openClassView } from "../tools/classes/class";
import { navigateHomeButton, goToTeachersPage } from "../tools/navigation/nav";
import { makeProfilePublic } from "../tools/profile/profile";

it('Is able to create a class adventure, public profile, in teacher preview mode. After exiting, class and adventure are deleted.', () => {
  navigateHomeButton('start_teaching_button', Cypress.env('teachers_page'))
  cy.getDataCy('teacher_mode_banner').should("be.visible");

  // can create classes
  const newClass = "test_class";
  createClass(newClass);
  openClassView();
  cy.getDataCy('view_class_link').should("contain.text", newClass)

  // can create adventures
  const adv = "test_adv";
  createAdventure(adv);
  goToTeachersPage();
  openAdventureView();
  cy.getDataCy('adventures_table').should("contain.text", adv);

  // can create public profile
  makeProfilePublic();
  cy.getDataCy('username-menu').invoke('text').then((username) => {
    const lowercaseUsername = username.toLowerCase();
    cy.getDataCy('exit_teacher_mode_banner').click();

    navigateHomeButton('start_teaching_button', Cypress.env('teachers_page'))
    cy.getDataCy('teacher_mode_banner').should("be.visible");

    // all created adventures/classes/public profile should be removed now.
    goToTeachersPage();
    cy.get("view_class_link").should("not.exist");
    cy.get("view_adventures").should("not.exist");
    cy.visit(`localhost:8080/user/${lowercaseUsername}`, { failOnStatusCode: false });
    cy.getDataCy('general_info').should("not.exist");
    cy.getDataCy('exit_teacher_mode_banner').click();
  });
})
