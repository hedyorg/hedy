import { loginForTeacher } from '../../tools/login/login';

export function loginAndOpenClasses(username = 'teacher1') {
  loginForTeacher(username);
  cy.visit('/for-teachers/class/all');
  cy.url().should('include', '/for-teachers/class/all');
}

export function uniqueName(prefix) {
  const random = Math.random().toString(36).slice(2, 10);
  return `${prefix}-${Date.now()}-${random}`;
}

export function createRedesignClass(options = {}) {
  const creationType = options.creationType || 'standard';
  const sourceClassId = options.sourceClassId;
  const className = options.className || uniqueName('redesign-e2e-class');

  cy.visit('/for-teachers/class/new');
  cy.get('#class_name').should('be.visible').clear().type(className);

  if (creationType === 'copy') {
    cy.intercept('POST', '/duplicate_class').as('duplicateClass');
    cy.get('input[name="creation_type"][value="copy"]').check({ force: true });
    if (sourceClassId) {
      cy.get('#class_to_copy').select(sourceClassId);
    }
    cy.get('#create_class_form button.green-btn-new').click();
    return cy.wait('@duplicateClass').then(({ response }) => {
      expect(response.statusCode).to.be.oneOf([200, 201]);
      const classId = response.body.id;
      cy.url().should('include', `/for-teachers/redesign/class/${classId}`);
      return cy.wrap({ classId, className });
    });
  }

  cy.intercept('POST', '/class').as('createClass');
  cy.get(`input[name="creation_type"][value="${creationType}"]`).check({ force: true });
  cy.get('#create_class_form button.green-btn-new').click();

  return cy.wait('@createClass').then(({ response }) => {
    expect(response.statusCode).to.be.oneOf([200, 201]);
    const classId = response.body.id;
    cy.url().should('include', `/for-teachers/redesign/class/${classId}`);
    return cy.wrap({ classId, className });
  });
}

export function createStudentsForClass(classId, count = 2) {
  const students = Array.from({ length: count }, (_, idx) => uniqueName(`student-${idx}`));

  cy.visit(`/for-teachers/create-accounts/${classId}`);
  cy.getDataCy('create_accounts_input').clear().type(students.join('\n'));

  cy.intercept('POST', '/for-teachers/create-accounts').as('createAccounts');
  cy.getDataCy('create_accounts_button').click();
  cy.getDataCy('modal_yes_button').click();
  cy.wait('@createAccounts').its('response.statusCode').should('eq', 200);
  cy.getDataCy('create_accounts_output').should('be.visible');

  return cy.wrap(students);
}

export function openClassOverview(classId) {
  cy.visit(`/for-teachers/redesign/class/${classId}`);
  cy.url().should('include', `/for-teachers/redesign/class/${classId}`);
}

export function openClassSubpage(classId, segment) {
  cy.visit(`/for-teachers/redesign/class/${classId}/${segment}`);
  cy.url().should('include', `/for-teachers/redesign/class/${classId}/${segment}`);
}

export function assertBreadcrumbLinks(expectedHrefs = []) {
  cy.get('div.mt-2, div.-mb-4').find('a[href="/for-teachers/redesign"]').should('exist');
  expectedHrefs.forEach((href) => {
    cy.get('a').filter(`[href="${href}"]`).should('exist');
  });
}
