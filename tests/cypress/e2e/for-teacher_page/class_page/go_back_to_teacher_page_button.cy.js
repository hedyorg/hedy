import {loginForTeacher} from '../../tools/login/login.js'
import { openClassView } from "../../tools/classes/class";

it('Is able to go to logs page', () => {
  loginForTeacher();
  cy.wait(500);

  openClassView();
  cy.getDataCy('view_class_link').first().click(); // Press view class button
  cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())

  cy.getDataCy('go_back_button')
    .should('be.visible')
    .should('not.be.disabled')
    .click();   

  cy.url()
    .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
})