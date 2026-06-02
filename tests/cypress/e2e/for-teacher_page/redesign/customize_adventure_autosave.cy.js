import { loginForTeacher } from '../../tools/login/login';

describe('Customize adventure redesign autosave', () => {
  it('autosaves editor content when CKEditor changes', () => {
    loginForTeacher('teacher1');
    cy.visit('/for-teachers/adventures/manage');

    cy.get('tr[data-cy^="my_adventure_row_"] a.view_class')
      .first()
      .should('be.visible')
      .click();

    cy.url().should('include', '/for-teachers/redesign/customize-adventure/');

    const marker = `autosave-redesign-${Date.now()}`;

    cy.wait(1200);
    cy.intercept('POST', '/for-teachers/customize-adventure').as('autosaveAdventure');

    cy.window().then((win) => {
      win.ckEditor.setData(`<p>${marker}</p><p>This content is long enough for autosave validation.</p>`);
    });

    cy.wait('@autosaveAdventure', { timeout: 15000 }).then(({ request, response }) => {
      expect(response?.statusCode).to.eq(200);
      expect(request.body.content).to.contain(marker);
    });
  });

  it('autosaves successfully when editor content is emptied', () => {
    loginForTeacher('teacher1');
    cy.visit('/for-teachers/adventures/manage');

    cy.get('tr[data-cy^="my_adventure_row_"] a.view_class')
      .first()
      .should('be.visible')
      .click();

    cy.url().should('include', '/for-teachers/redesign/customize-adventure/');

    cy.wait(1200);
    cy.intercept('POST', '/for-teachers/customize-adventure').as('autosaveAdventure');

    cy.window().then((win) => {
      win.ckEditor.setData('');
    });

    cy.wait('@autosaveAdventure', { timeout: 15000 }).then(({ request, response }) => {
      expect(response?.statusCode).to.eq(200);
      const plain = request.body.content
        .replace(/<[^>]+>/g, '')
        .replace(/&nbsp;/g, '')
        .trim();
      expect(plain).to.eq('');
    });
  });
});
