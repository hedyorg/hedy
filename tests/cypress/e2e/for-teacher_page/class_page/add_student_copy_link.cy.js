import {loginForTeacher, logout} from '../../tools/login/login.js'

it('Is able to see copy link to add student to class', () => {
    loginForTeacher();
    cy.wait(500);
    
    cy.get('[data-cy="view_class_link"]').then($viewClass => {
      if (!$viewClass.is(':visible')) {
          cy.get('[data-cy="view_classes"]').click();
      }
    });
    cy.get('[data-cy="view_class_link"]').first().click();
    cy.get('body').then($b => $b.find('[data-cy="survey"]')).then($s => $s.length && $s.hide())
    cy.get('[data-cy="add_student"]').click();
    cy.get('[data-cy="copy_join_link"]').should('be.visible').should('be.enabled').click();
})
