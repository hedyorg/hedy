import { loginAndOpenClasses, createRedesignClass, openClassOverview, assertBreadcrumbLinks, uniqueName } from './helpers';

function openClassesContextMenuForClass(classId) {
  cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).closest('tr').as('targetRow');
  cy.get('@targetRow').find('button.blue-btn-new').first().click();
  cy.get('@targetRow').find('div[id^="menu-"]').as('contextMenu');
  cy.get('@contextMenu').should('be.visible').and('not.have.class', 'hidden').and('have.class', 'menu-content-open');
}

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

  it('toggles classes table context menu open/close with animation classes', () => {
    cy.get('@classId').then((classId) => {
      cy.visit('/for-teachers/class/all');
      openClassesContextMenuForClass(classId);

      cy.get('@contextMenu')
        .should('have.class', 'transition-opacity')
        .and('have.class', 'transition-transform')
        .and('have.class', 'duration-150')
        .and('have.class', 'menu-content-open')
        .and('not.have.class', 'menu-content-closed');

      cy.get('@targetRow').find('button.blue-btn-new').first().click();
      cy.get('@contextMenu').should('have.class', 'menu-content-closed').and('not.have.class', 'menu-content-open');
      cy.wait(220);
      cy.get('@contextMenu').should('have.class', 'hidden');

      cy.get('@targetRow').find('button.blue-btn-new').first().click();
      cy.get('@contextMenu').should('be.visible').and('have.class', 'menu-content-open').and('not.have.class', 'hidden');
    });
  });

  it('hides classes table context menu when delete modal opens', () => {
    cy.get('@classId').then((classId) => {
      cy.visit('/for-teachers/class/all');
      openClassesContextMenuForClass(classId);

      cy.get('@targetRow').find('button[data-cy="remove_class"]').should('be.visible').click();
      cy.getDataCy('redesign_confirm_modal').should('be.visible');

      cy.wait(220);
      cy.get('@contextMenu')
        .should('have.class', 'hidden')
        .and('have.class', 'menu-content-closed')
        .and('not.have.class', 'menu-content-open');

      cy.getDataCy('redesign_confirm_no_button').click();
      cy.getDataCy('redesign_confirm_modal').should('not.be.visible');
    });
  });

  it('keeps context menu functional after archiving one class and allows archiving another', () => {
    cy.get('@classId').then((firstClassId) => {
      createRedesignClass({ className: uniqueName('overview-archive-second') }).then(({ classId: secondClassId }) => {
        cy.intercept('POST', '/for-teachers/class/*/archive').as('archiveClass');
        cy.visit('/for-teachers/class/all');

        openClassesContextMenuForClass(firstClassId);
        cy.get('@targetRow').find('button[data-cy="archive_class"]').should('be.visible').click();
        cy.getDataCy('redesign_confirm_modal').should('be.visible');
        cy.getDataCy('redesign_confirm_yes_button').click();
        cy.wait('@archiveClass').its('response.statusCode').should('eq', 200);
        cy.getDataCy('redesign_confirm_modal').should('not.be.visible');

        // Regression assertion: context menu should still open for another class
        openClassesContextMenuForClass(secondClassId);
        cy.get('@contextMenu').should('be.visible').and('not.have.class', 'hidden').and('have.class', 'menu-content-open');

        cy.get('@targetRow').find('button[data-cy="archive_class"]').should('be.visible').click();
        cy.getDataCy('redesign_confirm_modal').should('be.visible');
        cy.getDataCy('redesign_confirm_yes_button').click();
        cy.wait('@archiveClass').its('response.statusCode').should('eq', 200);
      });
    });
  });

  it('shows unarchive action in archived classes table and moves class back to active', () => {
    cy.get('@classId').then((classId) => {
      cy.intercept('POST', '/for-teachers/class/*/archive').as('archiveClass');
      cy.intercept('POST', '/for-teachers/class/*/unarchive').as('unarchiveClass');

      cy.visit('/for-teachers/class/all');
      openClassesContextMenuForClass(classId);
      cy.get('@targetRow').find('button[data-cy="archive_class"]').should('be.visible').click();
      cy.getDataCy('redesign_confirm_yes_button').click();
      cy.wait('@archiveClass').its('response.statusCode').should('eq', 200);

      cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).closest('tr').as('archivedRow');
      cy.get('@archivedRow').find('button.blue-btn-new').first().click();
      cy.get('@archivedRow').find('div[id^="menu-"]').should('be.visible').and('not.have.class', 'hidden');
      cy.get('@archivedRow').find('button[data-cy="unarchive_class"]').should('be.visible').click();
      cy.getDataCy('redesign_confirm_yes_button').click();
      cy.wait('@unarchiveClass').its('response.statusCode').should('eq', 200);

      cy.get(`a[href="/for-teachers/redesign/class/${classId}"]`).closest('tr').as('activeRow');
      cy.get('@activeRow').find('button.blue-btn-new').first().click();
      cy.get('@activeRow').find('button[data-cy="archive_class"]').should('be.visible');
    });
  });

  it('toggles archive/unarchive button and archived badge on class overview page', () => {
    cy.get('@classId').then((classId) => {
      cy.intercept('POST', '/for-teachers/class/*/archive').as('archiveClass');
      cy.intercept('POST', '/for-teachers/class/*/unarchive').as('unarchiveClass');

      openClassOverview(classId);
      cy.getDataCy('archive_class').should('be.visible').click();
      cy.getDataCy('redesign_confirm_yes_button').click();
      cy.wait('@archiveClass').its('response.statusCode').should('eq', 200);

      cy.contains('span', 'Archived').should('be.visible');
      cy.getDataCy('archive_class').should('not.exist');
      cy.getDataCy('unarchive_class').should('be.visible').click();
      cy.getDataCy('redesign_confirm_yes_button').click();
      cy.wait('@unarchiveClass').its('response.statusCode').should('eq', 200);

      cy.contains('span', 'Archived').should('not.exist');
      cy.getDataCy('archive_class').should('be.visible');
      cy.getDataCy('unarchive_class').should('not.exist');
    });
  });

  it('positions classes table context menu within viewport on mobile/tablet/desktop', () => {
    cy.get('@classId').then((classId) => {
      const viewports = ['iphone-6', 'ipad-2', [1280, 800]];

      cy.wrap(viewports).each((viewport) => {
        if (Array.isArray(viewport)) {
          cy.viewport(viewport[0], viewport[1]);
        } else {
          cy.viewport(viewport);
        }

        cy.visit('/for-teachers/class/all');
        openClassesContextMenuForClass(classId);

        cy.window().then((win) => {
          cy.get('@contextMenu').then(($menu) => {
            const rect = $menu[0].getBoundingClientRect();
            expect(rect.top).to.be.at.least(0);
            expect(rect.left).to.be.at.least(0);
            expect(rect.right).to.be.at.most(win.innerWidth);
            expect(rect.bottom).to.be.at.most(win.innerHeight);
          });
        });
      });
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
