import {loginForTeacher} from '../../tools/login/login.js'
import {createClass} from '../../tools/classes/class.js'


describe('Is able to go to logs page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);

    cy.get('[data-cy="view_class_link"]').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get('[data-cy="view_classes"]').click();
      }
    });
    cy.get('[data-cy="view_class_link"]').first().click(); // Press view class button
   cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide()).then($s => $s.length && $s.hide())

    cy.get('[data-cy="go_back_button"]')
      .should('be.visible')
      .should('not.be.disabled')
      .click();   

    cy.url()
      .should('eq', Cypress.config('baseUrl') + Cypress.env('teachers_page'));
  })
})