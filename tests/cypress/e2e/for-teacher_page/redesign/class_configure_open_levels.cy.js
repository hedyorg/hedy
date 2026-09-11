import { loginAndOpenClasses, createRedesignClass, openClassSubpage, uniqueName } from './helpers';
import { loginForTeacher } from '../../tools/login/login';

const SECOND_TEACHER = 'teacher2';

/**
 * Invite `username` as a second teacher and have them accept, without walking the whole UI.
 * Leaves the browser logged in as the second teacher.
 */
function addSecondTeacher(classId, username) {
  cy.request({
    method: 'POST',
    url: `/for-teachers/class/${classId}/configure/invite`,
    form: true,
    body: { usernames: username },
  }).its('status').should('eq', 200);

  loginForTeacher(username);
  // Accepting an invite decrements the unread-message counter, which the profile page seeds.
  cy.request('/my-profile').its('status').should('eq', 200);
  cy.request({
    method: 'POST',
    url: `/class/join/${classId}`,
    failOnStatusCode: false,
  }).its('status').should('be.oneOf', [200, 302]);
}

function levelToggle(level) {
  return cy.get(`#enable_level_${level}`);
}

/** Flip a level switch on the configure page and wait for the save to land. */
function toggleLevel(level) {
  cy.get(`#enable_level_${level}`).parent('.switch').find('.slider').click();
  return cy.wait('@saveLevels').its('response.statusCode').should('eq', 200);
}

/** Read the levels the server currently has stored for this class. */
function storedLevels(classId) {
  return cy
    .request(`/for-teachers/class/${classId}/configure`)
    .then(({ body }) => {
      const open = [];
      const pattern = /id="enable_level_(\d+)"([\s\S]{0,240}?)>/g;
      let match;
      while ((match = pattern.exec(body)) !== null) {
        if (match[2].includes('checked')) {
          open.push(Number(match[1]));
        }
      }
      return open;
    });
}

describe('Opening and closing levels on the configure class page', () => {
  beforeEach(() => {
    loginAndOpenClasses();
    createRedesignClass({ className: uniqueName('open-levels') }).then(({ classId }) => {
      cy.wrap(classId).as('classId');
    });
  });

  it('saves only the level that was toggled', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'configure');
      cy.intercept('POST', `/for-teachers/customize-levels/${classId}`).as('saveLevels');

      levelToggle(4).should('be.checked');
      toggleLevel(4);

      // The request must describe one level, not the state of every checkbox on the page.
      cy.get('@saveLevels').its('request.body').should((body) => {
        expect(body).to.deep.equal({ level: 4, enabled: false });
        expect(body).to.not.have.property('levels');
      });

      levelToggle(4).should('not.be.checked');
      cy.reload();
      levelToggle(4).should('not.be.checked');
      levelToggle(3).should('be.checked');
      levelToggle(5).should('be.checked');
    });
  });

  it('keeps a level a second teacher opened while the first teacher has the page open', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'configure');
      cy.intercept('POST', `/for-teachers/customize-levels/${classId}`).as('saveLevels');

      // The first teacher closes levels 4 and 5, then leaves the page sitting open.
      toggleLevel(4);
      toggleLevel(5);
      levelToggle(4).should('not.be.checked');
      levelToggle(5).should('not.be.checked');

      // Meanwhile the second teacher opens level 4 from their own session.
      addSecondTeacher(classId, SECOND_TEACHER);
      cy.request({
        method: 'POST',
        url: `/for-teachers/customize-levels/${classId}`,
        body: { level: 4, enabled: true },
      }).its('status').should('eq', 200);

      storedLevels(classId).should('include', 4);

      // Back on the first teacher's stale page, which still shows level 4 as closed,
      // they open level 5. That must not drag level 4 back down with it.
      loginForTeacher();
      openClassSubpage(classId, 'configure');
      cy.intercept('POST', `/for-teachers/customize-levels/${classId}`).as('saveLevels');
      levelToggle(4).should('be.checked');

      cy.window().then((win) => {
        // Put the page back into the stale state the first teacher was looking at
        win.document.getElementById('enable_level_4').checked = false;
      });
      toggleLevel(5);

      storedLevels(classId).should((levels) => {
        expect(levels, 'level opened by the second teacher').to.include(4);
        expect(levels, 'level opened by the first teacher').to.include(5);
      });
    });
  });

  it('lets a second teacher open a level and makes it stick', () => {
    cy.get('@classId').then((classId) => {
      openClassSubpage(classId, 'configure');
      cy.intercept('POST', `/for-teachers/customize-levels/${classId}`).as('saveLevels');
      toggleLevel(6);
      levelToggle(6).should('not.be.checked');

      addSecondTeacher(classId, SECOND_TEACHER);

      openClassSubpage(classId, 'configure');
      cy.intercept('POST', `/for-teachers/customize-levels/${classId}`).as('saveLevels');
      levelToggle(6).should('not.be.checked');
      toggleLevel(6);
      levelToggle(6).should('be.checked');

      cy.reload();
      levelToggle(6).should('be.checked');

      // and it is still open when the first teacher looks again
      loginForTeacher();
      openClassSubpage(classId, 'configure');
      levelToggle(6).should('be.checked');
    });
  });

  it('opens a level that was scheduled for a date in the future', () => {
    cy.get('@classId').then((classId) => {
      // The legacy customize page is the only place an opening date can be set. Schedule
      // level 4 far ahead and close it, the way a class from before the redesign looks.
      const levels = Array.from({ length: 16 }, (_, i) => String(i + 1)).filter((l) => l !== '4');
      cy.request({
        method: 'POST',
        url: `/for-teachers/customize-class/${classId}`,
        body: { levels, opening_dates: { 4: '2099-01-01' }, other_settings: [], level_thresholds: {} },
      }).its('status').should('eq', 200);

      // Open it again from the customize-level page, which has no opening-date UI either.
      cy.visit(`/for-teachers/class/${classId}/customize-level/4`);
      cy.intercept('POST', `/for-teachers/class/${classId}/customize-level/4/availability`).as('availability');
      cy.get('#level_availability_panel input[type="checkbox"]').should('not.be.checked');
      cy.get('#level_availability_panel .switch .slider').click();
      cy.wait('@availability').its('response.statusCode').should('eq', 200);
      cy.get('#level_availability_status').should('not.contain.text', 'currently unavailable');

      openClassSubpage(classId, 'configure');
      levelToggle(4).should('be.checked');

      // The page says level 4 is open, so previewing the class must actually land on level 4.
      // A level that is still closed silently serves the first open level instead.
      cy.visit(`/for-teachers/class/${classId}/preview?level=4`);
      cy.getDataCy('preview_class_banner').should('be.visible');
      cy.window().its('hedyApp.theLevel').should('eq', 4);
      cy.visit('/for-teachers/clear-preview-class');
    });
  });

  it('shows levels as open on a class that was never customized', () => {
    // Classes created before the redesign have no customizations record at all.
    cy.request({
      method: 'POST',
      url: '/class',
      body: { name: uniqueName('never-customized') },
    }).then(({ body }) => {
      const classId = body.id;

      openClassSubpage(classId, 'configure');
      cy.get('[id^="enable_level_"]').should('have.length', 16);
      cy.get('[id^="enable_level_"]:checked').should('have.length', 16);

      cy.intercept('POST', `/for-teachers/customize-levels/${classId}`).as('saveLevels');
      toggleLevel(2);
      levelToggle(2).should('not.be.checked');

      cy.reload();
      levelToggle(2).should('not.be.checked');
      levelToggle(1).should('be.checked');
    });
  });
});
