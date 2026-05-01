import { loginAndOpenClasses, createRedesignClass, assertBreadcrumbLinks, uniqueName } from './helpers';

describe('For Teachers redesign landing and classes pages', () => {
  beforeEach(() => {
    loginAndOpenClasses();
  });

  it('loads redesign landing page with key CTA links', () => {
    cy.visit('/for-teachers/redesign');
    cy.url().should('include', '/for-teachers/redesign');

    cy.getDataCy('create_class_button')
      .should('be.visible')
      .and('have.attr', 'href', '/for-teachers/class/new');

    cy.getDataCy('create_adventure_button').should('be.visible').click();
    cy.url().should('include', '/for-teachers/customize-adventure');
  });

  it('shows class list and links to redesigned class overview', () => {
    createRedesignClass({ className: uniqueName('classes-list') });
    cy.visit('/for-teachers/class/all');
    assertBreadcrumbLinks([]);

    cy.get('#classes_table').should('be.visible');
    cy.get('a[data-cy="view_class_link"]').should('have.length.at.least', 1);
    cy.get('a[data-cy="view_class_link"]').first().should('have.attr', 'href').and('include', '/for-teachers/redesign/class/');
  });

  it('new class form enforces required fields and supports standard creation', () => {
    cy.visit('/for-teachers/class/new');
    assertBreadcrumbLinks(['/for-teachers/class/all']);

    cy.intercept('POST', '/class').as('createClass');

    cy.get('#create_class_form button.green-btn-new').click();
    cy.wait(300);
    cy.get('@createClass.all').should('have.length', 0);

    const className = `redesign-standard-${Date.now()}`;
    cy.get('#class_name').type(className);
    cy.get('input[name="creation_type"][value="standard"]').check({ force: true });

    cy.get('#create_class_form button.green-btn-new').click();
    cy.wait('@createClass').its('response.statusCode').should('be.oneOf', [200, 201]);
    cy.url().should('include', '/for-teachers/redesign/class/');
  });

  it('new class form supports copy mode and submits duplicate endpoint', () => {
    createRedesignClass({ className: uniqueName('copy-source') }).then(({ classId }) => {
      cy.visit('/for-teachers/class/new');

      cy.intercept('POST', '/duplicate_class').as('duplicateClass');

      const className = uniqueName('redesign-copy');
      cy.get('#class_name').type(className);
      cy.get('input[name="creation_type"][value="copy"]').check({ force: true });

      cy.get('#class_to_copy').should('exist').select(classId);
      cy.get('#create_class_form button.green-btn-new').click();

      cy.wait('@duplicateClass').its('response.statusCode').should('be.oneOf', [200, 201]);
      cy.url().should('include', '/for-teachers/redesign/class/');
    });
  });
});
