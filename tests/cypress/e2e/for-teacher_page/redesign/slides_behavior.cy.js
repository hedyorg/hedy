import { loginForTeacher } from '../../tools/login/login';

describe('Teacher slides behavior', () => {
  beforeEach(() => {
    loginForTeacher();
    cy.visit('/for-teachers');
  });

  it('toggles slides table and persists visibility in localStorage', () => {
    cy.window().then((win) => {
      win.localStorage.removeItem('slides_table');
    });

    cy.reload();
    cy.get('#slides_table').should('have.class', 'hidden');

    cy.get('#view_slides').click();
    cy.get('#slides_table').should('not.have.class', 'hidden');
    cy.window().its('localStorage.slides_table').should('eq', 'true');
    cy.get('#slides_table_hide').should('not.have.class', 'hidden');

    cy.reload();
    cy.get('#slides_table').should('not.have.class', 'hidden');

    cy.get('#view_slides').click();
    cy.get('#slides_table').should('have.class', 'hidden');
    cy.window().its('localStorage.slides_table').should('eq', 'false');
  });

  it('has valid slides links and opens slides page with rendered sections', () => {
    cy.get('#view_slides').click();
    cy.get('#slides_table a[href^="/slides/"]').first().should('have.attr', 'href').then((href) => {
      cy.request(href).its('status').should('eq', 200);
      cy.visit(href);
      cy.get('.slides section').its('length').should('be.greaterThan', 0);
    });
  });

  it('download slides button triggers iframe source update for chosen level', () => {
    cy.get('#view_slides').click();
    cy.get('button[id^="download_slides_"]').first().invoke('attr', 'id').then((buttonId) => {
      const level = buttonId.replace('download_slides_', '');
      cy.get(`#level_${level}_slides`).should('have.attr', 'src', 'about:blank');

      cy.get(`#download_slides_${level}`).click({ force: true });
      cy.get(`#level_${level}_slides`).should('have.attr', 'src').and('include', `/slides/${level}`);
    });
  });
});
