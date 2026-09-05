import {loginForTeacher, logout, login} from '../../../tools/login/login.js'
import { createClass } from "../../../tools/classes/class.js";
import { goToProfilePage } from "../../../tools/navigation/nav.js";

const teachers = ["teacher1", "teacher4"];

function signUpStandaloneStudent() {
  const username = `invite-student-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
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

teachers.forEach((teacher) => {
  it(`Is able to add student by name for ${teacher}`, () => {
    signUpStandaloneStudent().then(({ username, password }) => {
      loginForTeacher(teacher);
      const className = createClass();
      cy.visit('/for-teachers/class/all');
      cy.getDataCy('view_class_link')
        .contains(className)
        .invoke('attr', 'href')
        .then((href) => {
          const classId = href.split('/').pop();
          cy.wrap(classId).as('classId');
          cy.visit(`/for-teachers/legacy/class/${classId}`);
        });

      cy.getDataCy('add_student').click();
      cy.get('#add_students_options').should('be.visible');

      cy.get('#add_students_options').then(($options) => {
        const inviteButton = $options.find('[data-cy="invite_student"]').first();

        if (inviteButton.length) {
          cy.window().then((win) => {
            win.eval(inviteButton.attr('onclick'));
          });
        }
      });

      cy.getDataCy('modal_search_input').type(username);
      cy.wait(500);
      cy.getDataCy('invite-1').click()
      cy.get('#users_to_invite').should('contain.text', username)
      cy.getDataCy('modal_ok_search_button').click()
      cy.getDataCy('invites_block').should('contain.text', username)

      cy.wait(500);
      login(username, password);

      goToProfilePage();
      cy.getDataCy('join_link').click();

      logout();
      loginForTeacher(teacher);
      cy.get('@classId').then((classId) => {
        cy.visit(`/for-teachers/legacy/class/${classId}`);
      });

      cy.getDataCy(`student_${username}`).should(($div) => {
        const text = $div.text()
        expect(text).include(username);
      })
    });
  })
})
