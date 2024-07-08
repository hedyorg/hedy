import { createAdventure, openAdventureView } from "../tools/adventures/adventure";
import { createClass, openClassView } from "../tools/classes/class";
import { goToHome, goToTeachersPage } from "../tools/navigation/nav";

describe('Test for teacher mode', () => {
  it('click try teaching, start teacher mode', () => {
    goToHome();
    cy.get('#try_teaching_button')
      .click();
    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));

    cy.getDataCy('teacher_mode_banner').should("be.visible");

    // can create classes
    const newClass = "math";
    createClass(newClass);
    // goToTeachersPage();
    openClassView();
    // this assumes the first class is the one we just added 
    cy.getDataCy('view_class_link').should("contain.text", newClass)

    // can create adventures
    const adv = "arithmetic";
    createAdventure(adv);
    goToTeachersPage();
    openAdventureView();
    cy.getDataCy('edit_link_adventure').should("contain.text", adv);
  
    cy.getDataCy('exit_teacher_mode_banner')
      .click();
  })

  it('a new login should not include previously created classes/adventures', () => {
    goToHome();
    cy.get('#try_teaching_button')
      .click();
    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));

    cy.getDataCy('teacher_mode_banner').should("be.visible");

    // all created adventures/classes should be removed now.
    goToTeachersPage();
    cy.get("view_class_link").should("not.exist");
    cy.get("view_adventures").should("not.exist");

  });
})
