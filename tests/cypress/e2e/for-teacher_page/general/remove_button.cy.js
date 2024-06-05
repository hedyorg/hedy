import { loginForTeacher } from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';
import { createClass, openClassView } from '../../tools/classes/class.js';

describe('Remove class test', () => {
  it('passes', () => {
    loginForTeacher();
    let className = createClass();
    goToTeachersPage();
    cy.reload();
    cy.wait(500);
    openClassView();
    cy.get("#remove_class").first().click()
  })
})
  