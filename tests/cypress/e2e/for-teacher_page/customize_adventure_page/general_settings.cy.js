import { loginForTeacher } from '../../tools/login/login.js'
import { createAdventure, openAdventureView } from '../../tools/adventures/adventure.js'
import { createClass } from '../../tools/classes/class.js'

const teachers = ["teacher1", "teacher4"];
const className = 'test'
const advName = 'test'

teachers.forEach((teacher) => {
  it(`Is able to name adventure, select a class, select level, agree public checkbox, go back and delete adventure for ${teacher}`, () => {
    loginForTeacher(teacher);
    createClass(className);
    createAdventure();

    // select levels
    cy.getDataCy('level_select').click()
    cy.wait(500)
    cy.getDataCy('2').click()
    cy.wait(500)
    cy.getDataCy('level_select').click()
    cy.wait(500)

    // set adventure name
    cy.getDataCy('custom_adventure_name').clear().type(advName)

    // select class
    cy.getDataCy('classes_select').click()
    cy.wait(500)
    cy.getDataCy(`${className}`).click()
    cy.wait(500)
    cy.getDataCy('classes_select').click()
    cy.wait(500)

    // agree public 
    cy.getDataCy('agree_public')
      .should('be.visible')
      .should('not.be.disabled')
      .check()
      .should('be.checked')
      .uncheck()
      .should('not.be.checked');

    cy.get('#submit_adventure').click();
    cy.wait(500)

    // go back button
    cy.getDataCy('go_back_button')
      .should('be.visible')
      .should('not.be.disabled')
      .click();

    openAdventureView();
    cy.getDataCy(`edit_link_${advName}`).click();

    // delete adventure
    cy.getDataCy('remove_adventure_button').click();
    cy.getDataCy('modal_yes_button').click();

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
    openAdventureView();
    cy.getDataCy('adventures_table').should("not.contain.text", advName);
  })
})
