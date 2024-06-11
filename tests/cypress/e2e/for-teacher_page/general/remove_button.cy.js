import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';
import { createClass, openClassView } from '../../tools/classes/class.js';
import { createAdventure, openAdventureView } from '../../tools/adventures/adventure.js';

it('Is able to remove a class', () => {
  const newClass = "NEWCLASS"
  loginForTeacher();
  createClass(newClass);
  goToTeachersPage();
  cy.reload();
  cy.wait(500);
  openClassView();
  cy.getDataCy('remove_class').first().click();
  cy.getDataCy('modal_yes_button').click();
  cy.getDataCy('view_class_link').should("not.contain.text", newClass)
})

it('Is able to remove an adventure', () => {
  const newAdventure = "NEWADV"
  loginForTeacher();
  createAdventure(newAdventure);
  goToTeachersPage();
  cy.reload();
  cy.wait(500);
  openAdventureView();
  cy.getDataCy(`delete_adventure_${newAdventure}`).click();
  cy.getDataCy('modal_yes_button').click();
  cy.getDataCy('edit_link_adventure').should("not.contain.text", newAdventure);
})