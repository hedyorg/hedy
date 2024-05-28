import {loginForTeacher} from '../../tools/login/login.js'
import { goToTeachersPage } from '../../tools/navigation/nav.js';
import { createClass } from '../../tools/classes/class.js';

describe('Remove class test', () => {
  it('passes', () => {
    loginForTeacher();
    let className = createClass();
    goToTeachersPage();
    cy.reload();
    cy.wait(500);
    cy.getBySel('view_class_link').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.getBySel('view_classes').click();
      }
    });
    cy.get("#remove-class").first().click()
  })
})
  