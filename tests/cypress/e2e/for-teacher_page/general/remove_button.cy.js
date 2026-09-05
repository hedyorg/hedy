import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';
import { createClass, openClassView } from '../../tools/classes/class.js';
import { createAdventure, deleteAdventure } from '../../tools/adventures/adventure.js';

it('Is able to remove a class', () => {
  const newClass = "NEWCLASS"
  loginForTeacher();
  createClass(newClass);
  goToTeachersPage();
  cy.reload();
  cy.wait(500);
  openClassView();
  cy.contains('tr', newClass).as('targetRow');
  cy.get('@targetRow').find('button.blue-btn-new').first().click({ force: true });
  cy.get('@targetRow').find('button[data-cy="remove_class"]').click({ force: true });
  cy.get('body').then(($body) => {
    if ($body.find('[data-cy="htmx_modal_yes_button"]:visible').length > 0) {
      cy.getDataCy('htmx_modal_yes_button').click();
    } else if ($body.find('[data-cy="redesign_confirm_yes_button"]:visible').length > 0) {
      cy.getDataCy('redesign_confirm_yes_button').click();
    } else {
      cy.getDataCy('modal_yes_button').click();
    }
  });
  cy.getDataCy('view_class_link').should("not.contain.text", newClass)
})

it('Is able to remove an adventure', () => {
  const newAdventure = `NEWADV_${Date.now()}`
  loginForTeacher();
  createAdventure(newAdventure);
  deleteAdventure(newAdventure);
  goToTeachersPage();
  cy.get('body').should('not.contain.text', newAdventure);
})