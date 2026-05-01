import { loginAndOpenClasses, createRedesignClass, openClassSubpage, assertBreadcrumbLinks, uniqueName } from './helpers';
import { login, loginForTeacher } from '../../tools/login/login';
import { goToProfilePage } from '../../tools/navigation/nav';

function createTeacherAccount(username, password) {
  cy.clearCookies();
  cy.clearAllLocalStorage();
  cy.clearAllSessionStorage();
  cy.visit('/signup?teacher=true');
  cy.get('body').then(($body) => {
    if ($body.find('[data-cy="signup_teacher"]').length) {
      cy.getDataCy('signup_teacher').click();
    }
  });
  cy.getDataCy('username').type(username);
  cy.getDataCy('email').type(`${username}@test.biz`);
  cy.getDataCy('password').type(password);
  cy.getDataCy('password_repeat').type(password);
  cy.getDataCy('language').select('English');
  cy.getDataCy('birth_year').type('2000');
  cy.getDataCy('gender').select('Female');
  cy.getDataCy('country').select('Australia');

  cy.getDataCy('from_another_teacher').check();
  cy.getDataCy('social_media').check();
  cy.getDataCy('from_video').check();
  cy.getDataCy('from_magazine_website').check();
  cy.getDataCy('other_source').check();
  cy.getDataCy('prog_experience_yes').check();
  cy.getDataCy('scratch').check();
  cy.getDataCy('python').check();
  cy.getDataCy('pair_with_teacher').check();
  cy.getDataCy('connect_guest_teacher').check();
  cy.getDataCy('phone').type('0612345678');
  cy.getDataCy('agree_terms').check();

  cy.intercept('POST', '/auth/signup').as('signupTeacher');
  cy.getDataCy('submit_button').click();
  cy.wait('@signupTeacher').its('response.statusCode').should('eq', 200);
  cy.url().should('include', '/for-teachers');
}

describe('Redesigned class configure and customize-level pages', () => {
  beforeEach(() => {
    loginAndOpenClasses();
    createRedesignClass({ className: uniqueName('configure') }).then(({ classId }) => {
      cy.wrap(classId).as('classId');
    });
  });

  it('renders configure controls and navigates to customize-level', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'configure');
      assertBreadcrumbLinks(['/for-teachers/class/all', `/for-teachers/redesign/class/${classId}`]);
      cy.get('[id^="enable_level_"]').should('have.length.at.least', 16);
      cy.get('#customize_level').select('2');

      cy.get(`button[onclick*="/for-teachers/redesign/class/${classId}/customize-level/"]`).click();
      cy.url().should('include', `/for-teachers/redesign/class/${classId}/customize-level/2`);
    });
  });

  it('toggles level availability and updates through HTMX', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'configure');
      cy.visit(`/for-teachers/redesign/class/${classId}/customize-level/1`);
      assertBreadcrumbLinks([
        '/for-teachers/class/all',
        `/for-teachers/redesign/class/${classId}`,
        `/for-teachers/redesign/class/${classId}/configure`,
      ]);

      cy.intercept('POST', `/for-teachers/redesign/class/${classId}/customize-level/1/availability`).as('availability');
      cy.get('#level_availability_panel input[type="checkbox"]').as('availabilityToggle');
      cy.get('#level_availability_panel .switch .slider').as('availabilitySlider');

      cy.get('@availabilityToggle').then(($toggle) => {
        if (!$toggle.is(':checked')) {
          cy.get('@availabilitySlider').click();
          cy.wait('@availability').its('response.statusCode').should('eq', 200);
        }
      });

      cy.get('@availabilityToggle').should('be.checked');
      cy.get('@availabilitySlider').click();
      cy.wait('@availability').its('response.statusCode').should('eq', 200);

      cy.get('@availabilityToggle').should('not.be.checked');
      cy.get('#level_availability_status').should('contain.text', 'currently unavailable for your students');

      cy.reload();
      cy.get('#level_availability_panel input[type="checkbox"]').should('not.be.checked');
      cy.get('#level_availability_status').should('contain.text', 'currently unavailable for your students');

      openClassSubpage(classId, 'configure');
      cy.get('#enable_level_1').should('not.be.checked');
    });
  });

  it('opens level dropdown and navigates to another level from customize-level page', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'configure');
      cy.visit(`/for-teachers/redesign/class/${classId}/customize-level/1`);

      cy.get('#level_button').should('be.visible');
      cy.get('#dropdown_level_button').click();
      cy.get('#level_dropdown').should('be.visible');

      cy.get('#level_dropdown a[id^="level_button_"]').should('have.length', 16);
      cy.get('#level_button_3').should('have.attr', 'href', `/for-teachers/redesign/class/${classId}/customize-level/3`);
      cy.get('#level_button_3').click();

      cy.url().should('include', `/for-teachers/redesign/class/${classId}/customize-level/3`);
      cy.get('#level_button_3').should('have.attr', 'disabled');
    });
  });

  it('opens and closes add-adventures modal, then restores default adventures', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'configure');
      cy.visit(`/for-teachers/redesign/class/${classId}/customize-level/1`);

      cy.get('#level_adventures_panel > div button.blue-btn-new').first().click();
      cy.get('#add_adventures_modal_level_1').should('be.visible');
      cy.get('#add_adventures_modal_level_1 button[aria-label]').first().click();
      cy.get('#add_adventures_modal_level_1').should('not.be.visible');

      cy.get('#level_1 input[name="adventure"]').then(($inputs) => {
        const originalAdventureIds = [...$inputs].map((input) => input.value);
        expect(originalAdventureIds.length).to.be.greaterThan(0);
        cy.wrap(originalAdventureIds).as('originalAdventureIds');
      });

      cy.intercept('POST', `/for-teachers/redesign/class/${classId}/customize-level/1/remove-adventure*`).as('removeAdventure');
      cy.get('#level_1 li button[aria-label]').first().click();
      cy.wait('@removeAdventure').its('response.statusCode').should('eq', 200);

      cy.get('@originalAdventureIds').then((originalAdventureIds) => {
        cy.get('#level_1 input[name="adventure"]').then(($inputsAfterRemove) => {
          const modifiedAdventureIds = [...$inputsAfterRemove].map((input) => input.value);
          expect(modifiedAdventureIds).to.not.deep.equal(originalAdventureIds);
        });
      });

      cy.intercept('POST', `/for-teachers/redesign/class/${classId}/customize-level/1/restore-default-adventures`).as('restoreDefault');
      cy.get('button[hx-post*="/restore-default-adventures"]').click();
      cy.getDataCy('redesign_confirm_modal').should('be.visible');
      cy.getDataCy('redesign_confirm_yes_button').click();
      cy.wait('@restoreDefault').its('response.statusCode').should('eq', 200);

      cy.get('@originalAdventureIds').then((originalAdventureIds) => {
        cy.get('#level_1 input[name="adventure"]').then(($inputsAfterRestore) => {
          const restoredAdventureIds = [...$inputsAfterRestore].map((input) => input.value);
          expect(restoredAdventureIds).to.deep.equal(originalAdventureIds);
        });
      });
    });
  });

  it('loads remove-all-adventures modal endpoint and handles invalid level URL', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'configure');
      cy.visit(`/for-teachers/redesign/class/${classId}/customize-level/1`);

      cy.get('#level_1 input[name="adventure"]').its('length').should('be.greaterThan', 0);

      cy.intercept('GET', `/for-teachers/redesign/class/${classId}/customize-level/1/remove-all-adventures-modal`).as('removeAllModal');
      cy.intercept('POST', `/for-teachers/redesign/class/${classId}/customize-level/1/sort-adventures`).as('removeAllAdventures');
      cy.get('button[hx-get*="/remove-all-adventures-modal"]').click();
      cy.wait('@removeAllModal').its('response.statusCode').should('eq', 200);
      cy.getDataCy('htmx_modal_yes_button').should('be.visible');
      cy.getDataCy('htmx_modal_yes_button').click();
      cy.wait('@removeAllAdventures').its('response.statusCode').should('eq', 200);

      cy.get('#level_1 li').should('have.length', 0);
      cy.get('#level_1 input[name="adventure"]').should('not.exist');

      cy.request({
        url: `/for-teachers/redesign/class/${classId}/customize-level/0`,
        failOnStatusCode: false,
      }).its('status').should('eq', 404);
    });
  });

  it('invites a newly created teacher, accepts invitation, and shows teacher in configure table', () => {
    cy.get('@classId').then((classId) => {
      const invitedTeacher = `teacher${Date.now()}${Math.random().toString(36).slice(2, 6)}`;
      const invitedTeacherPassword = '123456';

      createTeacherAccount(invitedTeacher, invitedTeacherPassword);

      loginForTeacher();
      openClassSubpage(classId, 'configure');

      cy.intercept('GET', '/search*').as('searchTeacher');
      cy.intercept('POST', `/for-teachers/redesign/class/${classId}/configure/invite`).as('inviteTeacher');

      cy.get(`button.green-btn-new[data-class-id="${classId}"]`).scrollIntoView().click();
      cy.getDataCy('redesign_search_modal').should('be.visible');
      cy.getDataCy('redesign_search_input').type(invitedTeacher);
      cy.wait('@searchTeacher').its('response.statusCode').should('eq', 200);
      cy.getDataCy('invite-1').click();
      cy.get('#redesign_users_to_invite').should('contain.text', invitedTeacher);
      cy.getDataCy('redesign_search_ok_button').click();
      cy.wait('@inviteTeacher').its('response.statusCode').should('eq', 200);
      cy.get('#configure-teachers-table-body').should('contain.text', invitedTeacher);

      login(invitedTeacher, invitedTeacherPassword);
      cy.getDataCy('user_dropdown').should('be.visible');
      goToProfilePage();
      cy.url().should('include', '/my-profile');
      cy.intercept('POST', `/class/join/${classId}`).as('joinClass');
      cy.getDataCy('join_link').click();
      cy.wait('@joinClass').its('response.statusCode').should((statusCode) => {
        expect([200, 302]).to.include(statusCode);
      });

      loginForTeacher();
      openClassSubpage(classId, 'configure');
      cy.contains('#configure-teachers-table-body tr td', invitedTeacher)
        .parents('tr')
        .within(() => {
          cy.contains('td', 'teacher').should('exist');
        });
    });
  });
});
