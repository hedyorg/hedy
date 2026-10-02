import { loginForTeacher } from '../../tools/login/login';

describe('Teaching materials', () => {
  beforeEach(() => {
    loginForTeacher();
  });

  it('offers a level picker and a card per material', () => {
    cy.visit('/for-teachers/teaching-materials');

    cy.getDataCy('prepare_level_button').should('be.visible');
    cy.getDataCy('prepare_level_options').should('not.be.visible');
    cy.getDataCy('teaching_materials_cards').find('> div').should('have.length', 3);
    cy.getDataCy('background_information_link').should('have.attr', 'href', '/for-teachers/manual');
    cy.getDataCy('slides_link').should('have.attr', 'href', '/for-teachers/slides');
  });

  it('marks the workbooks as work in progress instead of linking to them', () => {
    cy.visit('/for-teachers/teaching-materials');

    cy.getDataCy('workbooks_card_work_in_progress').should('be.visible');
    cy.getDataCy('workbooks_card').should('be.visible').find('a').should('not.exist');
    cy.get('a[href="/for-teachers/workbooks/all"]').should('not.exist');
  });

  it('prepares the level picked in the dropdown', () => {
    cy.visit('/for-teachers/teaching-materials');

    cy.getDataCy('prepare_level_button').click();
    cy.getDataCy('prepare_level_options').should('be.visible');
    cy.getDataCy('prepare_level_5').click();

    cy.url().should('include', '/for-teachers/teaching-materials/5');
    cy.getDataCy('teaching_materials_level_dropdown').should('contain', 'Level 5');
  });

  it('has a page per level listing its materials', () => {
    cy.visit('/for-teachers/teaching-materials/3');

    cy.getDataCy('teaching_materials_level_dropdown').should('contain', 'Level 3');
    cy.getDataCy('teaching_materials_slides_link').should('have.attr', 'href', '/for-teachers/slides/3');
    cy.getDataCy('teaching_materials_workbook').should('be.visible');
    cy.getDataCy('teaching_materials_workbook_work_in_progress').should('be.visible');
    cy.get('a[href="/for-teachers/workbooks/3"]').should('not.exist');
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

  it('leaves out materials a level does not have', () => {
    // Workbooks only go up to level 8, slides go further.
    cy.visit('/for-teachers/teaching-materials/12');

    cy.getDataCy('teaching_materials_slides_link').should('have.attr', 'href', '/for-teachers/slides/12');
    cy.getDataCy('teaching_materials_workbook').should('not.exist');
  });
});
