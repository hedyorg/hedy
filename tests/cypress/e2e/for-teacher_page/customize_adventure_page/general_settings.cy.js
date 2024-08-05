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
    
    // select class
    cy.getDataCy('custom_adventure_name').clear().type(advName)
    cy.getDataCy('classes_select').click()
    cy.wait(1000)
    cy.getDataCy(`${className}`).click()
    cy.getDataCy('classes_select').click()

    // select levels
    cy.getDataCy('level_select').click()
    cy.wait(500)
    cy.getDataCy('1').click()
    cy.getDataCy('2').click()
    cy.getDataCy('level_select').click()

    // agree public 
    cy.getDataCy('agree_public')
      .should('be.visible')
      .should('not.be.disabled')
      .check()
      .should('be.checked')
      .uncheck()
      .should('not.be.checked');

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