import { loginAndOpenClasses, createRedesignClass, createStudentsForClass, openClassSubpage, assertBreadcrumbLinks, uniqueName } from './helpers';
import { login } from '../../tools/login/login';

function getCreatedStudentCredentials() {
  return cy.getDataCy('create_accounts_output').find('tr').then(($rows) => {
    const credentials = [];

    Cypress.$($rows).each((index, row) => {
      if (index === 0) {
        return;
      }

      const cells = Cypress.$(row).find('td');
      if (cells.length < 3) {
        return;
      }

      credentials.push({
        username: Cypress.$(cells[1]).text().trim(),
        password: Cypress.$(cells[2]).text().trim(),
      });
    });

    return credentials;
  });
}

function createAndSubmitProgramForStudent(studentCredential, index) {
  const outputToken = `graph-output-${index}`;

  login(studentCredential.username, studentCredential.password);
  cy.visit('/hedy/1');

  cy.get('#editor .cm-content').click();
  cy.focused().type(`{selectall}{backspace}print ${outputToken}`);

  cy.getDataCy('runit').click();
  cy.getDataCy('output').should('contain.text', outputToken);

  cy.visit('/programs');
  cy.get('.program').first().invoke('attr', 'data-id').then((programId) => {
    cy.request('POST', '/programs/submit', { id: programId }).its('status').should('eq', 200);
  });
}

function seedSubmittedPrograms(studentCredentials) {
  cy.wrap(studentCredentials).each((studentCredential, index) => {
    createAndSubmitProgramForStudent(studentCredential, index + 1);
  });
}

function getGraphData() {
  return cy.get('#adventure_bubble').should('have.attr', 'data-graph').then((graphData) => {
    return JSON.parse(graphData);
  });
}

describe('Redesigned class performance graph page', () => {
  let classId;
  let students = [];

  before(() => {
    loginAndOpenClasses();
    createRedesignClass({ className: uniqueName('performance-graph') }).then((createdClass) => {
      classId = createdClass.classId;
      return createStudentsForClass(classId, 3);
    }).then(() => {
      return getCreatedStudentCredentials();
    }).then((studentCredentials) => {
      students = studentCredentials.map(({ username }) => username);
      return seedSubmittedPrograms(studentCredentials);
    }).then(() => {
      loginAndOpenClasses();
    });
  });

  beforeEach(() => {
    loginAndOpenClasses();
  });

  it('serializes seeded graph data for the default level', () => {
    openClassSubpage(classId, 'graph');
    assertBreadcrumbLinks(['/for-teachers/class/all', `/for-teachers/redesign/class/${classId}`]);
    cy.get('#programs_container').should('have.class', 'hidden');

    getGraphData().then((graphData) => {
      expect(graphData.level).to.eq(1);
      expect(graphData.graph_students).to.have.length(students.length);
      expect(graphData.graph_students.map((student) => student.username).sort()).to.deep.eq([...students].sort());

      graphData.graph_students.forEach((student) => {
        expect(student).to.have.keys([
          'username',
          'programs',
          'adventures_tried',
          'number_of_errors',
          'successful_runs',
        ]);
        expect(student.adventures_tried).to.be.greaterThan(0);
        expect(student.successful_runs).to.be.greaterThan(0);
        expect(student.number_of_errors).to.be.at.least(0);
      });
    });
  });

  it('changes level through the dropdown and updates the graph payload', () => {
    openClassSubpage(classId, 'graph');

    cy.get('#dropdown_level_button').click();
    cy.get('#level_button_2').should('have.attr', 'href', `/for-teachers/redesign/class/${classId}/graph?level=2`).click();

    cy.url().should('include', `/for-teachers/redesign/class/${classId}/graph?level=2`);
    cy.get('#dropdown_level_button').should('contain.text', '2');

    cy.get('#dropdown_level_button').click();
    cy.get('#level_button_2').should('have.attr', 'disabled');

    getGraphData().then((graphData) => {
      expect(graphData.level).to.eq(2);
      expect(graphData.graph_students).to.have.length(students.length);

      graphData.graph_students.forEach((student) => {
        expect(student.adventures_tried).to.eq(0);
        expect(student.successful_runs).to.eq(0);
        expect(student.number_of_errors).to.eq(0);
      });
    });
  });

  it('loads a selected student programs panel for the graph', () => {
    const selectedStudent = students[0];

    openClassSubpage(classId, 'graph');
    cy.intercept('GET', '/for-teachers/redesign/get_student_programs*').as('loadGraphPrograms');

    cy.window().then((win) => {
      win.hedyApp.loadPerformanceGraphPrograms([selectedStudent], 1, true);
    });

    cy.wait('@loadGraphPrograms').then(({ request, response }) => {
      expect(response.statusCode).to.eq(200);
      const url = new URL(request.url);
      expect(url.searchParams.getAll('usernames')).to.deep.eq([selectedStudent]);
      expect(url.searchParams.get('level')).to.eq('1');
    });

    cy.get('#programs_container').should('not.have.class', 'hidden');
    cy.get(`#${selectedStudent}_programs_container`).should('be.visible');
    cy.get(`#${selectedStudent}_programs_container .show-program-button`).should('have.length.greaterThan', 0);
  });

  it('loads multiple student program panels for overlapping graph points', () => {
    const selectedStudents = students.slice(0, 2);

    openClassSubpage(classId, 'graph');
    cy.intercept('GET', '/for-teachers/redesign/get_student_programs*').as('loadMultipleGraphPrograms');

    cy.window().then((win) => {
      win.hedyApp.loadPerformanceGraphPrograms(selectedStudents, 1, true);
    });

    cy.wait('@loadMultipleGraphPrograms').then(({ request, response }) => {
      expect(response.statusCode).to.eq(200);
      const url = new URL(request.url);
      expect(url.searchParams.getAll('usernames').sort()).to.deep.eq([...selectedStudents].sort());
      expect(url.searchParams.get('level')).to.eq('1');
    });

    selectedStudents.forEach((student) => {
      cy.get(`#${student}_programs_container`).should('be.visible');
    });
  });

  it('shows the no programs state for an unseeded level', () => {
    const selectedStudent = students[0];

    cy.visit(`/for-teachers/redesign/class/${classId}/graph?level=2`);
    cy.intercept('GET', '/for-teachers/redesign/get_student_programs*').as('loadEmptyGraphPrograms');

    cy.window().then((win) => {
      win.hedyApp.loadPerformanceGraphPrograms([selectedStudent], 2, true);
    });

    cy.wait('@loadEmptyGraphPrograms').its('response.statusCode').should('eq', 200);
    cy.get(`#${selectedStudent}_programs_container`).should('be.visible');
    cy.get(`#${selectedStudent}_programs_container`).find('[data-cy="no-programs"]').should('be.visible');
  });

  it('closes a loaded student programs panel', () => {
    const selectedStudent = students[0];

    openClassSubpage(classId, 'graph');
    cy.intercept('GET', '/for-teachers/redesign/get_student_programs*').as('loadClosableGraphPrograms');

    cy.window().then((win) => {
      win.hedyApp.loadPerformanceGraphPrograms([selectedStudent], 1, true);
    });

    cy.wait('@loadClosableGraphPrograms').its('response.statusCode').should('eq', 200);
    cy.get(`#${selectedStudent}_programs_container`).should('be.visible').within(() => {
      cy.getDataCy('hide').click();
    });
    cy.get(`#${selectedStudent}_programs_container`).should('not.exist');
  });

  it('returns 404 for a non-existing redesigned class graph id', () => {
    cy.request({
      url: '/for-teachers/redesign/class/non-existing-redesign-class-id/graph',
      failOnStatusCode: false,
    }).its('status').should('eq', 404);
  });
});