import { loginForTeacher } from '../../tools/login/login.js'
import { createAdventure, openAdventureView } from '../../tools/adventures/adventure.js'
import { createClass } from '../../tools/classes/class.js'

const teachers = ["teacher1", "teacher4"];
const className = 'test'
const advName = `test_${Date.now()}`

teachers.forEach((teacher) => {
  it(`Is able to name adventure, select a class, select level, agree public checkbox, go back and delete adventure for ${teacher}`, () => {
    loginForTeacher(teacher);
    createClass(className);
    createAdventure(advName);

    cy.get('body').then(($body) => {
      if ($body.find('[data-cy="level_select"]').length > 0) {
        cy.getDataCy('level_select').click();
        cy.getDataCy('2').click();
        cy.getDataCy('level_select').click();

        cy.getDataCy('classes_select').click();
        cy.getDataCy(`${className}`).click();
        cy.getDataCy('classes_select').click();

        cy.getDataCy('agree_public')
          .should('be.visible')
          .check()
          .should('be.checked')
          .uncheck()
          .should('not.be.checked');

        cy.get('#submit_adventure').click();
        cy.getDataCy('remove_adventure_button').click();
      } else {
        cy.getDataCy('solution_example').click();
        cy.get('input[name="adventure_levels"]').first().check({ force: true });
        cy.get('input[name="adventure_public"]').check({ force: true }).uncheck({ force: true });
        cy.getDataCy('delete_adventure').click();
      }
    });

    cy.get('body').then(($body) => {
      if ($body.find('[data-cy="htmx_modal_yes_button"]:visible').length > 0) {
        cy.getDataCy('htmx_modal_yes_button').click();
      } else if ($body.find('[data-cy="redesign_confirm_yes_button"]:visible').length > 0) {
        cy.getDataCy('redesign_confirm_yes_button').click();
      } else {
        cy.getDataCy('modal_yes_button').click();
      }
    });

    cy.visit('/for-teachers/adventures/manage');
    cy.get('body').should('not.contain', advName);
  })
})
