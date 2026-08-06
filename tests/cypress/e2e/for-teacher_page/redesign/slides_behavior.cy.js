import { loginForTeacher } from '../../tools/login/login';

describe('Teacher slides behavior', () => {
  beforeEach(() => {
    loginForTeacher();
    cy.visit('/for-teachers');
  });

  it('teacher landing remains accessible and does not expose the legacy slides toggle UI', () => {
    cy.url().should('include', '/for-teachers');
    cy.get('#view_slides').should('not.exist');
    cy.get('#slides_table').should('not.exist');
  });

  it('opens a slides page with rendered sections', () => {
    cy.request('/slides/1').its('status').should('eq', 200);
    cy.visit('/slides/1');
    cy.get('.slides section').its('length').should('be.greaterThan', 0);
  });

  it('slides PDF endpoint is available for download', () => {
    cy.request('/slides/1').then((resp) => {
      expect(resp.status).to.eq(200);
      expect(resp.headers['content-type']).to.include('text/html');
    });
  });
});
