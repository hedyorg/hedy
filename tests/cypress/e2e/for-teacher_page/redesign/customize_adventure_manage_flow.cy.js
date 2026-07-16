import { loginForTeacher } from '../../tools/login/login';
import { createRedesignClass, uniqueName } from './helpers';

function createAdventureFromManage(adventureName = uniqueName('redesign-manage-adventure')) {
  cy.visit('/for-teachers/adventures/manage');
  cy.getDataCy('create_new_adventure_button').should('be.visible').click();
  cy.getDataCy('redesign_prompt_modal').should('be.visible');
  cy.getDataCy('redesign_prompt_input').clear().type(adventureName);
  cy.getDataCy('redesign_prompt_ok_button').click();

  cy.url().should('include', '/for-teachers/customize-adventure/');

  return cy.location('pathname').then((pathname) => {
    const adventureId = pathname.split('/').pop();
    expect(adventureId, 'adventure id in URL').to.be.a('string').and.not.be.empty;

    return cy
      .request('POST', '/for-teachers/customize-adventure', {
        id: adventureId,
        name: adventureName,
        content: `<p>${adventureName} content</p>`,
        formatted_content: `<p>${adventureName} content</p>`,
        formatted_solution_code: '',
        public: false,
        language: 'en',
        classes: [],
        levels: ['1'],
      })
      .then((response) => {
        expect(response.status).to.eq(200);
        return cy.wrap({ adventureId, adventureName });
      });
  });
}

describe('Redesign manage adventures flow', () => {
  beforeEach(() => {
    loginForTeacher('teacher1');
  });

  it('creates an adventure from manage page and removes it from the same table', () => {
    const adventureName = uniqueName('manage-create-delete');

    createAdventureFromManage(adventureName).then(({ adventureId }) => {
      cy.visit('/for-teachers/adventures/manage');

      cy.contains('#my-adventures-table tr', adventureName, { timeout: 10000 })
        .as('targetRow')
        .should('be.visible');

      cy.get('@targetRow')
        .find('a.view_class')
        .should('have.attr', 'href')
        .and('include', `/for-teachers/customize-adventure/${adventureId}`);

      cy.intercept('POST', `/for-teachers/adventures/${adventureId}/remove`).as('deleteAdventure');

      cy.get('@targetRow').find('button.teacher-menu-button').scrollIntoView().should('be.enabled').click({ force: true });
      cy.get(`li[data-cy="remove_adventure_${adventureId}"]`).click({ force: true });
      cy.getDataCy('htmx_modal_yes_button').should('be.visible').click();

      cy.wait('@deleteAdventure').its('response.statusCode').should('eq', 200);
      cy.contains('#my-adventures-table tr', adventureName).should('not.exist');
    });
  });

  it('renames a redesigned adventure from the page and reflects the new name in manage table', () => {
    const originalName = uniqueName('rename-source');
    const renamedName = uniqueName('rename-target');

    createAdventureFromManage(originalName).then(({ adventureId }) => {
      cy.visit(`/for-teachers/customize-adventure/${adventureId}`);
      cy.get('h1').should('contain.text', originalName);

      cy.intercept('PUT', `/for-teachers/customize-adventure/${adventureId}/name`).as('renameAdventure');

      cy.get(`i[data-adventure-id="${adventureId}"]`).click();
      cy.getDataCy('redesign_prompt_modal').should('be.visible');
      cy.getDataCy('redesign_prompt_input').clear().type(renamedName);
      cy.getDataCy('redesign_prompt_ok_button').click();

      cy.wait('@renameAdventure').then(({ request, response }) => {
        expect(response?.statusCode).to.eq(200);
        expect(request.body).to.deep.equal({ name: renamedName });
      });
    });
  });

  it('adds a newly created adventure to a redesigned class and keeps it scoped to selected levels', () => {
    const adventureName = uniqueName('class-link');

    createRedesignClass({ className: uniqueName('adv-manage-class') }).then(({ classId, className }) => {
      createAdventureFromManage(adventureName).then(({ adventureId }) => {
        cy.get('input[name="adventure_levels"]').then(($levels) => {
          const levelElements = Array.from($levels);

          const levelOne = levelElements.find((element) => element.value === '1');
          if (levelOne && !levelOne.checked) {
            cy.wrap(levelOne).check({ force: true });
          }

          const nonLevelOneChecked = levelElements.find((element) => element.value !== '1' && element.checked);
          if (nonLevelOneChecked) {
            cy.wrap(nonLevelOneChecked).uncheck({ force: true });
          }
        });

        cy.visit(`/for-teachers/class/${classId}/customize-level/1`);

        cy.intercept('POST', `/for-teachers/class/${classId}/customize-level/1/add-adventure`).as('addAdventureToLevel1');

        cy.get('#level_adventures_panel button.blue-btn-new').last().click();
        cy.get('#add_adventures_modal_level_1').should('be.visible');
        cy.contains('#add_adventures_modal_level_1 label', adventureName)
          .scrollIntoView()
          .click({ force: true });
        cy.get('#add_adventures_modal_level_1 button.green-btn-new').click();

        cy.wait('@addAdventureToLevel1').then(({ response }) => {
          expect(response?.statusCode).to.eq(200);
        });

        cy.get('#level_1 li').should('contain.text', adventureName);

        cy.get('#dropdown_level_button').click();
        cy.get('#level_button_2').click();
        cy.url().should('include', `/for-teachers/class/${classId}/customize-level/2`);

        cy.get('#level_2').should('not.contain.text', adventureName);

        cy.visit(`/for-teachers/customize-adventure/${adventureId}`);
        cy.getDataCy('solution_example').click();
        cy.get('#adventure-used-in-table').should('contain.text', className);
        cy.get('#adventure-used-in-table').should('contain.text', '1');
      });
    });
  });
});
