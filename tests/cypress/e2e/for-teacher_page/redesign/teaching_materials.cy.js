import { loginForTeacher } from '../../tools/login/login';

describe('Teaching materials', () => {
  beforeEach(() => {
    loginForTeacher();
  });

  it('offers a level picker and a card per material', () => {
    cy.visit('/for-teachers/teaching-materials');

    cy.getDataCy('prepare_level_select').find('option').its('length').should('be.greaterThan', 1);
    cy.getDataCy('prepare_level_button').should('be.visible');
    cy.getDataCy('teaching_materials_cards').find('> div').should('have.length', 3);
    cy.getDataCy('background_information_link').should('have.attr', 'href', '/for-teachers/manual');
    cy.getDataCy('slides_link').should('have.attr', 'href', '/for-teachers/slides');
  });

  it('prepares the level picked in the dropdown', () => {
    cy.visit('/for-teachers/teaching-materials');

    cy.getDataCy('prepare_level_select').select('5');
    cy.getDataCy('prepare_level_button').click();

    cy.url().should('include', '/for-teachers/teaching-materials/5');
    cy.getDataCy('teaching_materials_level_dropdown').should('contain', 'Level 5');
  });

  it('has a page per level listing the materials it will hold', () => {
    cy.visit('/for-teachers/teaching-materials/3');

    cy.getDataCy('teaching_materials_level_dropdown').should('contain', 'Level 3');
    cy.getDataCy('teaching_materials_list').find('> li').should('have.length', 3);
    cy.getDataCy('teaching_materials_common_mistakes').should('be.visible');
  });

  it('picks another level from the title dropdown', () => {
    cy.visit('/for-teachers/teaching-materials/3');

    cy.getDataCy('teaching_materials_level_options').should('not.be.visible');
    cy.getDataCy('teaching_materials_level_dropdown').click();
    cy.getDataCy('teaching_materials_level_options').should('be.visible');
    cy.getDataCy('teaching_materials_level_7').click();

    cy.url().should('include', '/for-teachers/teaching-materials/7');
    cy.getDataCy('teaching_materials_level_dropdown').should('contain', 'Level 7');
  });

  it('shows what changes in the level and the mistakes to expect', () => {
    cy.visit('/for-teachers/teaching-materials/3');

    cy.getDataCy('level_concepts_and_changes').should('be.visible');
    cy.getDataCy('level_concepts_and_changes').find('li').should('have.length.greaterThan', 0);
    cy.getDataCy('common_mistakes_list')
      .find('[data-cy="common_mistake"]')
      .should('have.length.greaterThan', 0);
  });

  it('opens a menu per material with the actions it supports', () => {
    cy.visit('/for-teachers/teaching-materials/3');

    cy.getDataCy('teaching_materials_slides_menu').should('not.be.visible');
    cy.getDataCy('teaching_materials_slides_actions').click();
    cy.getDataCy('teaching_materials_slides_menu').should('be.visible');
    cy.getDataCy('teaching_materials_slides_view').should('have.attr', 'href', '/for-teachers/slides/3');

    // Opening another menu closes the previous one.
    cy.getDataCy('teaching_materials_workbook_actions').click();
    cy.getDataCy('teaching_materials_slides_menu').should('not.be.visible');
    cy.getDataCy('teaching_materials_workbook_view').should('have.attr', 'href', '/for-teachers/workbooks/3');
    // Downloading a workbook is not built yet, so the action is listed but disabled.
    cy.getDataCy('teaching_materials_workbook_download')
      .should('be.visible')
      .and('have.attr', 'aria-disabled', 'true');
  });

  it('disables the materials that do not exist for a level', () => {
    // Workbooks only go up to level 8, slides go further.
    cy.visit('/for-teachers/teaching-materials/12');

    cy.getDataCy('teaching_materials_slides_link').should('have.attr', 'href', '/for-teachers/slides/12');
    cy.getDataCy('teaching_materials_workbook_link').should('not.have.attr', 'href');

    cy.getDataCy('teaching_materials_workbook_actions').click();
    cy.getDataCy('teaching_materials_workbook_view').should('have.attr', 'aria-disabled', 'true');
  });
});
