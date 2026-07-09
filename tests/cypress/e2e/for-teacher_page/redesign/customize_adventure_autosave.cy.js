import { loginForTeacher } from '../../tools/login/login';
import { uniqueName } from './helpers';

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

function waitForSingleUpload(alias, assertions) {
  cy.wait(alias, { timeout: 20000 }).then(({ request, response }) => {
    expect(response?.statusCode).to.eq(200);
    assertions(request.body);
  });
}

function openNewAdventureInRedesign(adventureName = `redesign-flow-${Date.now()}`) {
  cy.visit('/for-teachers/adventures/manage');
  cy.getDataCy('create_new_adventure_button').should('be.visible').click();
  cy.getDataCy('redesign_prompt_modal').should('be.visible');
  cy.getDataCy('redesign_prompt_input').should('be.visible').clear().type(adventureName);
  cy.getDataCy('redesign_prompt_ok_button').click();
  cy.url().should('include', '/for-teachers/redesign/customize-adventure/');
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

    waitForSingleUpload('@uploadAdventureDraft', (body) => {
      expect(body.content).to.include(contentMarker);
      expect(body.formatted_solution_code).to.include(solutionMarker);
      expect(body.formatted_solution_code).to.include('{print}');
    });
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

    // Adventure has multiple levels and should use the minimum one.
    // At minimum level, `if` should not be transformed into a keyword placeholder.
    waitForSingleUpload('@uploadAdventureDraft', (body) => {
      expect(body.formatted_content).to.include('{not_in}');
      expect(body.formatted_content).to.include('{print} hello');
      expect(body.formatted_content).to.not.include('{if}');
    });
  });

  it('uploads usage settings changes (public and levels) through redesign autosave', () => {
    loginForTeacher('teacher1');
    openNewAdventureInRedesign(uniqueName('usage-settings'));

    cy.getDataCy('solution_example').click();

    cy.intercept('POST', '/for-teachers/customize-adventure').as('uploadAdventureDraft');

    let expectedPublic;
    cy.get('input[name="adventure_public"]').then(($switch) => {
      expectedPublic = !$switch.prop('checked');
      cy.wrap($switch).click({ force: true });
    });

    waitForSingleUpload('@uploadAdventureDraft', (body) => {
      expect(body.public).to.eq(expectedPublic);
    });

    let expectedLevel;
    cy.get('input[name="adventure_levels"]').then(($levels) => {
      const levelElements = Array.from($levels);
      const uncheckedLevel = levelElements.find((element) => !element.checked);

      if (uncheckedLevel) {
        expectedLevel = uncheckedLevel.value;
        cy.wrap(uncheckedLevel).check({ force: true });
        return;
      }

      const checkedLevel = levelElements.find((element) => element.checked);
      if (!checkedLevel) {
        throw new Error('Expected at least one available level switch');
      }

      expectedLevel = checkedLevel.value;
      cy.wrap(checkedLevel).check({ force: true });
    });

    waitForSingleUpload('@uploadAdventureDraft', (body) => {
      expect(Array.isArray(body.levels)).to.eq(true);
      expect(body.levels).to.include(expectedLevel);
    });
  });

  it('shows and hides public adventure options when public is toggled', () => {
    loginForTeacher('teacher1');
    openNewAdventureInRedesign(uniqueName('public-options-flow'));

    cy.getDataCy('solution_example').click();

    cy.intercept('POST', '/for-teachers/customize-adventure').as('uploadAdventureDraft');

    cy.get('input[name="adventure_public"]').click({ force: true });
    cy.wait('@uploadAdventureDraft');
    cy.get('#public_adventure_options').should('be.visible');
    cy.get('#public_adventure_options').find('#languages_dropdown').should('exist');

    cy.get('input[name="adventure_public"]').click({ force: true });
    cy.wait('@uploadAdventureDraft');
    cy.get('#public_adventure_options').should('have.class', 'hidden');
  });

  it('adds tags in redesigned customize adventure usage tab', () => {
    loginForTeacher('teacher1');
    openNewAdventureInRedesign(uniqueName('tags-flow'));

    cy.getDataCy('solution_example').click();

    cy.intercept('POST', '/for-teachers/customize-adventure').as('uploadAdventureDraft');

    cy.get('input[name="adventure_public"]').click({ force: true });
    cy.wait('@uploadAdventureDraft');
    cy.get('#public_adventure_options').should('be.visible');

    const tagName = uniqueName('adv-tag');

    cy.intercept('POST', '/tags/create/*').as('createTag');
    cy.getDataCy('search_tags_input').clear().type(tagName);
    cy.getDataCy('add_adventure_tags').click({ force: true });
    cy.wait('@createTag').then(({ request, response }) => {
      expect(request.body).to.include(`tag=${encodeURIComponent(tagName)}`);
      expect(response?.statusCode).to.be.oneOf([200, 400]);
    });
  });
});
