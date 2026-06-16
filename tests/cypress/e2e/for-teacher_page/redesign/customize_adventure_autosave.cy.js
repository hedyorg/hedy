import { loginForTeacher } from '../../tools/login/login';

function waitForUploadContaining(alias, marker, getValue, remainingAttempts = 6) {
  cy.wait(alias, { timeout: 20000 }).then(({ request, response }) => {
    expect(response?.statusCode).to.eq(200);

    const value = getValue(request.body);
    if (typeof value === 'string' && value.includes(marker)) {
      return;
    }

    if (remainingAttempts <= 1) {
      throw new Error(`Expected uploaded payload to contain marker ${marker}`);
    }

    waitForUploadContaining(alias, marker, getValue, remainingAttempts - 1);
  });
}

function waitForUploadWithEmptyContent(alias, remainingAttempts = 6) {
  cy.wait(alias, { timeout: 20000 }).then(({ request, response }) => {
    expect(response?.statusCode).to.eq(200);

    const plain = request.body.content
      .replace(/<[^>]+>/g, '')
      .replace(/&nbsp;/g, '')
      .trim();

    if (plain === '') {
      return;
    }

    if (remainingAttempts <= 1) {
      throw new Error('Expected uploaded payload to contain empty content');
    }

    waitForUploadWithEmptyContent(alias, remainingAttempts - 1);
  });
}

describe('Customize adventure redesign autosave', () => {
  it('uploads latest local draft content and solution to backend', () => {
    loginForTeacher('teacher1');
    cy.visit('/for-teachers/adventures/manage');

    cy.get('tr[data-cy^="my_adventure_row_"] a.view_class')
      .first()
      .should('be.visible')
      .click();

    cy.url().should('include', '/for-teachers/redesign/customize-adventure/');

    const contentMarker = `autosave-redesign-content-${Date.now()}`;
    const solutionMarker = `autosave-redesign-solution-${Date.now()}`;

    cy.intercept('POST', '/for-teachers/customize-adventure').as('uploadAdventureDraft');

    cy.window().then((win) => {
      win.ckEditor.setData(`<p>${contentMarker}</p><p>This content is long enough for autosave validation.</p>`);
      win.ckSolutionEditor.setData(`<p>${solutionMarker}</p><pre data-language="Hedy"><code class="language-python">print hello</code></pre>`);
    });

    waitForUploadContaining('@uploadAdventureDraft', contentMarker, (body) => body.content);
    waitForUploadContaining('@uploadAdventureDraft', solutionMarker, (body) => body.formatted_solution_code);
    waitForUploadContaining('@uploadAdventureDraft', '{print}', (body) => body.formatted_solution_code);
  });

  it('uploads successfully when editor content is emptied', () => {
    loginForTeacher('teacher1');
    cy.visit('/for-teachers/adventures/manage');

    cy.get('tr[data-cy^="my_adventure_row_"] a.view_class')
      .first()
      .should('be.visible')
      .click();

    cy.url().should('include', '/for-teachers/redesign/customize-adventure/');

    cy.intercept('POST', '/for-teachers/customize-adventure').as('uploadAdventureDraft');

    cy.window().then((win) => {
      win.ckEditor.setData('');
    });

    waitForUploadWithEmptyContent('@uploadAdventureDraft');
  });

  it('uploads formatted_content with curly braces for snippets and inline keywords, using minimum selected level', () => {
    loginForTeacher('teacher1');
    cy.visit('/for-teachers/adventures/manage');

    cy.get('tr[data-cy^="my_adventure_row_"] a.view_class')
      .first()
      .should('be.visible')
      .click();

    cy.url().should('include', '/for-teachers/redesign/customize-adventure/');

    cy.intercept('POST', '/for-teachers/customize-adventure').as('uploadAdventureDraft');

    cy.window().then((win) => {
      win.ckEditor.setData(
        `<p>Inline keyword: <code>not in</code></p>` +
        `<pre><code class="language-python">if name is Hedy\n    print hello</code></pre>` +
        `<p>This sentence keeps payload long enough for backend validation.</p>`
      );
    });

    waitForUploadContaining('@uploadAdventureDraft', '{not_in}', (body) => body.formatted_content);
    waitForUploadContaining('@uploadAdventureDraft', '{print}', (body) => body.formatted_content);

    // Adventure has multiple levels and should use the minimum one.
    // At minimum level, `if` should not be transformed into a keyword placeholder.
    cy.wait('@uploadAdventureDraft', { timeout: 20000 }).then(({ request, response }) => {
      expect(response?.statusCode).to.eq(200);
      expect(request.body.formatted_content).to.include('{not_in}');
      expect(request.body.formatted_content).to.include('{print} hello');
      expect(request.body.formatted_content).to.not.include('{if}');
    });
  });
});
