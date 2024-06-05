import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';
import { createClass, openClassView } from '../../tools/classes/class.js';

it('Remove class test', () => {
  loginForTeacher();
  createClass();
  goToTeachersPage();
  cy.reload();
  cy.wait(500);
  openClassView();
  cy.getDataCy('remove_class').first().click()
})
  