import { loginAndOpenClasses, createRedesignClass, openClassOverview, assertBreadcrumbLinks, uniqueName } from './helpers';

describe('Redesigned class overview navigation', () => {
  beforeEach(() => {
    loginAndOpenClasses();
    createRedesignClass({ className: uniqueName('overview') }).then(({ classId }) => {
      cy.wrap(classId).as('classId');
    });
  });

  it('shows links to all redesigned class subpages', () => {
    cy.get('@classId').then((classId) => {
      openClassOverview(classId);
      assertBreadcrumbLinks(['/for-teachers/class/all']);
      cy.get(`a[href="/for-teachers/redesign/class/${classId}/graph"]`).should('be.visible');
      cy.get(`a[href="/for-teachers/redesign/class/${classId}/grade"]`).should('be.visible');
      cy.get(`a[href="/for-teachers/redesign/class/${classId}/manage"]`).should('be.visible');
      cy.get(`a[href="/for-teachers/redesign/class/${classId}/configure"]`).should('be.visible');
    });
  });

  it('renders danger zone controls with delete endpoint', () => {
    cy.get('@classId').then((classId) => {
      openClassOverview(classId);
      cy.getDataCy('delete_class')
        .should('be.visible')
        .and('have.attr', 'hx-delete', `/for-teachers/class/${classId}`)
        .and('have.attr', 'data-confirm-modal', 'redesign');
    });
  });

  it('loads performance graph canvas and supports level links', () => {
    cy.get('@classId').then((classId) => {
      cy.visit(`/for-teachers/redesign/class/${classId}/graph`);
      assertBreadcrumbLinks(['/for-teachers/class/all', `/for-teachers/redesign/class/${classId}`]);
      cy.get('#adventure_bubble').should('be.visible').and('have.attr', 'data-graph');

      cy.get('#dropdown_level_button').click();
      cy.get(`#level_button_2`).should('have.attr', 'href', `/for-teachers/redesign/class/${classId}/graph?level=2`);
    });
  });

  it('opens classes table context menu and follows grading/configure actions', () => {
    cy.get('@classId').then((classId) => {
      cy.visit('/for-teachers/class/all');
      cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).closest('tr').as('targetRow');

      cy.get('@targetRow').find('button.blue-btn-new').first().click();
      cy.get('@targetRow').find('div[id^="menu-"]').should('be.visible').and('not.have.class', 'hidden');
      cy.get('@targetRow').find('a[href*="/grade"]').should('be.visible').click();
      cy.url().should('include', `/for-teachers/redesign/class/${classId}/grade`);

      cy.visit('/for-teachers/class/all');
      cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).closest('tr').as('targetRow');
      cy.get('@targetRow').find('button.blue-btn-new').first().click();
      cy.get('@targetRow').find('div[id^="menu-"]').should('be.visible').and('not.have.class', 'hidden');
      cy.get('@targetRow').find('a[href*="/configure"]').should('be.visible').click();
      cy.url().should('include', `/for-teachers/redesign/class/${classId}/configure`);
    });
  });

  it('opens classes table delete confirmation and cancel keeps class', () => {
    cy.get('@classId').then((classId) => {
      cy.visit('/for-teachers/class/all');
      cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).closest('tr').as('targetRow');

      cy.get('@targetRow').find('button.blue-btn-new').first().click();
      cy.get('@targetRow').find('div[id^="menu-"]').should('be.visible').and('not.have.class', 'hidden');
      cy.get('@targetRow').find('button[data-cy="remove_class"]').should('be.visible').click();

      cy.getDataCy('redesign_confirm_modal').should('be.visible');
      cy.getDataCy('redesign_confirm_no_button').should('be.visible').click();
      cy.getDataCy('redesign_confirm_modal').should('not.be.visible');
      cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).should('exist');
    });
  });

  it('renames a class from the configure page', () => {
    cy.get('@classId').then((classId) => {
      const renamedClass = uniqueName('renamed-overview');

      cy.visit(`/for-teachers/redesign/class/${classId}/configure`);
      cy.intercept('PUT', `/class/${classId}`).as('renameClass');

      cy.get('h1 i.fa-pencil').should('be.visible').click();
      cy.getDataCy('redesign_prompt_modal').should('be.visible');
      cy.getDataCy('redesign_prompt_input').should('be.visible').clear().type(renamedClass);
      cy.getDataCy('redesign_prompt_ok_button').click();

      cy.wait('@renameClass').its('response.statusCode').should('eq', 200);
      cy.get('h1').should('contain.text', renamedClass);
      assertBreadcrumbLinks(['/for-teachers/class/all', `/for-teachers/redesign/class/${classId}`]);

      cy.visit('/for-teachers/class/all');
      cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).should('contain.text', renamedClass);
    });
  });

  it('returns 404 for non-existing redesigned class id', () => {
    cy.request({
      url: '/for-teachers/redesign/class/non-existing-redesign-class-id',
      failOnStatusCode: false,
    }).its('status').should('eq', 404);
  });

  it('deletes a class from overview and ensures it is gone', () => {
    cy.get('@classId').then((classId) => {
      // Go to the overview page
      openClassOverview(classId);
      // Click the delete button (danger zone)
      cy.getDataCy('delete_class').click();
      // Confirm the modal appears
      cy.getDataCy('redesign_confirm_modal').should('be.visible');
      // Confirm deletion
      cy.getDataCy('redesign_confirm_yes_button').click();
      // Modal should disappear
      cy.getDataCy('redesign_confirm_modal').should('not.be.visible');
      // Should be redirected to the classes list
      cy.url().should('include', '/for-teachers/class/all');
      // The class should no longer be in the list
      cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).should('not.exist');
      // Direct navigation should 404
      cy.request({
        url: `/for-teachers/redesign/class/${classId}`,
        failOnStatusCode: false,
      }).its('status').should('eq', 404);
    });
  });
});
