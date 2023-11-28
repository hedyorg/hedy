import { loginForStudent, loginForTeacher } from "../tools/login/login";
import {goToHedyLevel2Page} from "../tools/navigation/nav";

describe('Go to level dropdown', () => {
  it('Is able to use the level dropdown to go to level 1', () => {
    loginForStudent('student5')
    goToHedyLevel2Page();

    cy.get('#dropdown_level_button').click();
    cy.get('#level_button_1').click();
    cy.url().should('include', Cypress.env('hedy_page'));
  })

  it('Is not able to go to disabled level 5', () => {
    loginForTeacher();
    cy.wait(500);

    cy.getBySel('view_class_link').first().click();
    cy.get('body').then($b => $b.find("#survey")).then($s => $s.length && $s.hide())
    cy.getBySel('customize_class_button').click();
    cy.get('#enable_level_5').parent('.switch').click();
    cy.getBySel('save_customizations').click();


    loginForStudent('student5')
    goToHedyLevel2Page();
    cy.get('#dropdown_level_button').click();
    cy.get('#level_button_1').click();
    cy.url().should('include', Cypress.env('hedy_page'));

    cy.get('#dropdown_level_button').click();
    cy.get('#level_button_5').should('be.disabled');
  })
})