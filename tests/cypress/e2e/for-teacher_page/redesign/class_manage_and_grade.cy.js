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
  const outputToken = `hello-1-${index}`;

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

function getManageTableUsernames() {
  return cy.get('#manage-students-table-body tr').then(($rows) => {
    return Cypress.$($rows).map((_, row) => {
      return Cypress.$(row).find('td').first().text().trim();
    }).get();
  });
}

function openManageStudentActions(username) {
  cy.getDataCy(`manage_student_row_${username}`).within(() => {
    cy.getDataCy(`manage_student_actions_${username}`).should('be.visible').click();
  });

  cy.getDataCy(`manage_student_menu_${username}`).should('be.visible').and('not.have.class', 'hidden');
}

function signUpStandaloneStudent() {
  const username = uniqueName('invite-student');
  const password = 'InviteStudent123!';

  cy.clearCookies();
  cy.clearAllLocalStorage();
  cy.clearAllSessionStorage();
  cy.visit('/signup');

  cy.get('body').then(($body) => {
    if ($body.find('[data-cy="signup_student"]').length) {
      cy.getDataCy('signup_student').click();
    }
  });

  cy.intercept('POST', '/auth/signup').as('signupStudent');
  cy.getDataCy('username').type(username);
  cy.getDataCy('email').type(`${username}@test.biz`);
  cy.getDataCy('password').type(password);
  cy.getDataCy('password_repeat').type(password);
  cy.getDataCy('language').select('English');
  cy.getDataCy('birth_year').type('2000');
  cy.getDataCy('gender').select('Female');
  cy.getDataCy('country').select('Australia');
  cy.getDataCy('prog_experience_yes').check();
  cy.getDataCy('scratch').check();
  cy.getDataCy('python').check();
  cy.getDataCy('agree_terms').check();
  cy.getDataCy('submit_button').click();
  cy.wait('@signupStudent').its('response.statusCode').should('eq', 200);

  return cy.wrap({ username, password });
}

describe('Redesigned class grading and management pages', () => {
  beforeEach(() => {
    loginAndOpenClasses();
    createRedesignClass({ className: uniqueName('grade-manage') }).then(({ classId }) => {
      cy.wrap(classId).as('classId');
      createStudentsForClass(classId, 3).then(() => {
        getCreatedStudentCredentials().then((studentCredentials) => {
          cy.wrap(studentCredentials.map(({ username }) => username)).as('students');
          cy.wrap(studentCredentials).as('studentCredentials');
          seedSubmittedPrograms(studentCredentials);
        });
      });
    }).then(() => {
      loginAndOpenClasses();
    });
  });

  it('shows all students in the manage students table', () => {
    cy.get('@classId').then((classId) => {
      cy.get('@students').then((students) => {
        openClassSubpage(classId, 'manage');
        assertBreadcrumbLinks(['/for-teachers/class/all', `/for-teachers/redesign/class/${classId}`]);

        cy.get('#manage-students-table-body tr').should('have.length', students.length);
        students.forEach((student) => {
          cy.getDataCy(`manage_student_row_${student}`).should('be.visible').and('contain.text', student);
        });
      });
    });
  });

  it('sorts the manage students table by student name', () => {
    cy.get('@classId').then((classId) => {
      cy.get('@students').then((students) => {
        const ascStudents = [...students].sort((left, right) => left.localeCompare(right));
        const descStudents = [...ascStudents].reverse();

        openClassSubpage(classId, 'manage');
        cy.intercept('GET', `/for-teachers/redesign/class/${classId}/manage/filter_sort*`).as('manageFilterSort');

        cy.getDataCy('sort_student').click();
        cy.wait('@manageFilterSort').its('response.statusCode').should('eq', 200);
        cy.get('#student-sort-input').should('have.value', 'ascendent');
        getManageTableUsernames().should('deep.equal', ascStudents);

        cy.getDataCy('sort_student').click();
        cy.wait('@manageFilterSort').its('response.statusCode').should('eq', 200);
        cy.get('#student-sort-input').should('have.value', 'descendent');
        getManageTableUsernames().should('deep.equal', descStudents);
      });
    });
  });

  it('resets a student password from the manage students table', () => {
    cy.get('@classId').then((classId) => {
      cy.get('@students').then((students) => {
        const targetStudent = students[0];
        const newPassword = 'ResetStudent123!';

        openClassSubpage(classId, 'manage');
        cy.intercept('POST', '/auth/change_student_password').as('changeStudentPassword');

        openManageStudentActions(targetStudent);
        cy.getDataCy(`reset_student_password_${targetStudent}`).should('be.visible').click();

        cy.getDataCy('redesign_prompt_modal').should('be.visible');
        cy.getDataCy('redesign_prompt_input').should('be.visible').clear().type(newPassword);
        cy.getDataCy('redesign_prompt_ok_button').click();
        cy.getDataCy('redesign_prompt_modal').should('not.be.visible');

        cy.getDataCy('redesign_confirm_modal').should('be.visible');
        cy.getDataCy('redesign_confirm_yes_button').click();
        cy.wait('@changeStudentPassword').its('response.statusCode').should('eq', 200);
        cy.getDataCy('modal_alert_text').should('contain.text', 'successfully changed');
      });
    });
  });

  it('deletes a student from the manage students table', () => {
    cy.get('@classId').then((classId) => {
      cy.get('@students').then((students) => {
        const targetStudent = students[1];

        openClassSubpage(classId, 'manage');
        cy.intercept('POST', `/for-teachers/redesign/class/${classId}/manage/remove_student/${targetStudent}*`).as('removeStudent');

        openManageStudentActions(targetStudent);
        cy.getDataCy(`remove_student_${targetStudent}`).should('be.visible').click();

        cy.getDataCy('htmx_modal').should('be.visible');
        cy.getDataCy('htmx_modal_yes_button').click();
        cy.wait('@removeStudent').its('response.statusCode').should('eq', 200);
        cy.getDataCy(`manage_student_row_${targetStudent}`).should('not.exist');
        cy.get('#manage-students-table-body tr').should('have.length', students.length - 1);
      });
    });
  });

  it('invites a student from the manage students modal and shows the pending invite in the table', () => {
    cy.get('@classId').then((classId) => {
      signUpStandaloneStudent().then(({ username }) => {
        loginAndOpenClasses();
        openClassSubpage(classId, 'manage');

        cy.intercept('GET', '/search*').as('searchStudents');
        cy.intercept('POST', `/for-teachers/redesign/class/${classId}/manage/invite`).as('inviteStudent');

        cy.getDataCy('invite_student').should('be.visible').click();
        cy.getDataCy('redesign_search_modal').should('be.visible');
        cy.getDataCy('redesign_search_input').type(username);
        cy.wait('@searchStudents').its('response.statusCode').should('eq', 200);
        cy.getDataCy('invite-1').should('be.visible').click();
        cy.get('#redesign_users_to_invite').should('contain.text', username);

        cy.getDataCy('redesign_search_ok_button').click();
        cy.wait('@inviteStudent').its('response.statusCode').should('eq', 200);
        cy.getDataCy('redesign_search_modal').should('not.be.visible');
        cy.getDataCy(`manage_student_row_${username}`).should('be.visible').and('contain.text', username);
      });
    });
  });

  it('filters programs on grade page using selected student', () => {
    cy.get('@classId').then((classId) => {
      cy.get('@students').then((students) => {
        const selectedStudent = students[0];
        const otherStudent = students[1];

        openClassSubpage(classId, 'grade');
        assertBreadcrumbLinks(['/for-teachers/class/all', `/for-teachers/redesign/class/${classId}`]);
        cy.intercept('GET', `/for-teachers/redesign/class/${classId}/grade/filter_sort*`).as('gradeFilterSort');

        cy.get('#dropdown_student_button').click();
        cy.get('#student_dropdown').should('be.visible');
        cy.get(`#student_button_${selectedStudent}`).click();

        cy.get('button[type="submit"]').find('.fa-filter').first().parent('button').click();
        cy.wait('@gradeFilterSort').its('response.statusCode').should('eq', 200);

        cy.get('#grade-class-table-body [data-cy="teacher_cell"]').should('have.length.greaterThan', 0);
        cy.get('#grade-class-table-body').should('contain.text', selectedStudent);
        cy.get('#grade-class-table-body').should('not.contain.text', otherStudent);
      });
    });
  });

  it('grades and ungrades a student program from grade page', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'grade');
      cy.get('.student_adventure_checkbox').should('have.length.greaterThan', 0);
      cy.intercept('POST', `/for-teachers/redesign/program/${classId}/grade*`).as('tickProgram');

      cy.get('.student_adventure_checkbox').first().then(($checkbox) => {
        const wasTicked = $checkbox.hasClass('fa-check');

        cy.wrap($checkbox).click();
        cy.wait('@tickProgram').its('response.statusCode').should('eq', 200);
        cy.get('.student_adventure_checkbox').first().should(
          wasTicked ? 'not.have.class' : 'have.class',
          'fa-check'
        );

        cy.get('.student_adventure_checkbox').first().click();
        cy.wait('@tickProgram').its('response.statusCode').should('eq', 200);
        cy.get('.student_adventure_checkbox').first().should(
          wasTicked ? 'have.class' : 'not.have.class',
          'fa-check'
        );
      });
    });
  });

  it('views student program, toggles approval, and unsubmits program', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'grade');

      cy.get('#grade-class-table-body a[href*="/view/redesign"]').first().invoke('attr', 'href').then((href) => {
        cy.visit(href);
      });

      cy.intercept('POST', '/for-teachers/check_adventure*').as('checkAdventure');
      cy.get('#adventure_checkbox').should('be.visible');
      cy.get('#adventure-button-text').invoke('text').then((initialText) => {
        cy.get('#adventure_checkbox').click();
        cy.wait('@checkAdventure').its('response.statusCode').should('eq', 200);
        cy.get('#adventure-button-text').should(
          'contain.text',
          initialText.includes('Solution Approved') ? 'Accept program' : 'Solution Approved'
        );

        cy.get('#adventure_checkbox').click();
        cy.wait('@checkAdventure').its('response.statusCode').should('eq', 200);
        cy.get('#adventure-button-text').should('contain.text', initialText.trim());
      });

      cy.intercept('POST', '/programs/unsubmit').as('unsubmitProgram');
      cy.get('#unsubmit-program-button').should('be.visible').click();
      cy.getDataCy('redesign_confirm_yes_button').click();
      cy.wait('@unsubmitProgram').its('response.statusCode').should('eq', 200);
      cy.get('#unsubmit-program-button').should('not.be.visible');
    });
  });

  it('navigates from view-program page using next adventure and next student buttons', () => {
    cy.get('@classId').then((classId) => {
      cy.get('@students').then((students) => {
        const selectedStudent = students[0];

        openClassSubpage(classId, 'grade');

        cy.get('#dropdown_level_button').click();
        cy.get('#level_button_1').click();

        cy.get('#dropdown_student_button').click();
        cy.get(`#student_button_${selectedStudent}`).click();
        cy.get('button[type="submit"]').find('.fa-filter').first().parent('button').click();

        cy.contains('#grade-class-table-body tr', selectedStudent)
          .find('a[href*="/view/redesign"]')
          .first()
          .invoke('attr', 'href')
          .then((viewHref) => {
            cy.visit(viewHref);

            cy.get('body').then(($body) => {
              const nextAdventureCount = $body.find('a.blue-btn-new i.fa-puzzle-piece').length;
              if (nextAdventureCount > 0) {
                cy.location('pathname').then((beforeAdventurePath) => {
                  cy.get('a.blue-btn-new').filter(':has(i.fa-puzzle-piece)').first().click();
                  cy.location('pathname').should('not.eq', beforeAdventurePath);
                });
              }
            });

            cy.visit(viewHref);

            cy.get('body').then(($body) => {
              const nextStudentCount = $body.find('a.blue-btn-new i.fa-child-reaching').length;
              if (nextStudentCount > 0) {
                cy.location('pathname').then((beforeStudentPath) => {
                  cy.get('a.blue-btn-new').filter(':has(i.fa-child-reaching)').first().click();
                  cy.location('pathname').should('not.eq', beforeStudentPath);
                });
              }
            });
          });
      });
    });
  });
});
