import {loginForTeacher} from '../../tools/login/login.js'

it('Is able to go to customize class page', () => {
  loginForTeacher();
  cy.wait(500);

  cy.get('[data-cy="view_class_link"]').then($viewClass => {
    if (!$viewClass.is(':visible')) {
        cy.get('[data-cy="view_classes"]').click();
    }
  });
  cy.get('[data-cy="view_class_link"]').first().click(); // Press view class button

  var currentUrl = '';
  cy.url().then(url => {
    currentUrl = url;
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())
    cy.get('[data-cy="customize_class_button"]').click(); // Press logs button

    let statsUrl = Cypress.env('customize_class_page') + currentUrl.substring(currentUrl.indexOf('class/')+6);
    cy.url().should('include', statsUrl); // Check if you are in the logs page
  })    
})