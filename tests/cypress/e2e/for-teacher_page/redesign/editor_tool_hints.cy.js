import { loginForTeacher } from '../../tools/login/login';

function openNewAdventure(adventureName = `tool-hints-${Date.now()}`) {
  cy.visit('/for-teachers/adventures/manage');
  cy.getDataCy('create_new_adventure_button').should('be.visible').click();
  cy.getDataCy('redesign_prompt_modal').should('be.visible');
  cy.getDataCy('redesign_prompt_input').should('be.visible').clear().type(adventureName);
  cy.getDataCy('redesign_prompt_ok_button').click();
  cy.url().should('include', '/for-teachers/customize-adventure/');
}

describe('Adventure editor explanation panel', () => {
  beforeEach(() => {
    loginForTeacher('teacher1');
    openNewAdventure();
    cy.get('.ck-toolbar', { timeout: 20000 }).should('be.visible');
  });

  it('tags the real toolbar buttons with the tool they run', () => {
    cy.get('.ck-toolbar [data-hedy-tool="code"]').should('exist');
    cy.get('.ck-toolbar [data-hedy-tool="codeBlock"]').should('exist');
  });

  it('renders the panel glyphs as illustrations, not controls', () => {
    cy.get('#explanation [data-points-to]').should('have.length', 2);

    cy.get('#explanation [data-points-to]').each(($glyph) => {
      // Not a button, not focusable, and hidden from assistive tech: the
      // surrounding sentence carries the meaning instead.
      expect($glyph.prop('tagName')).to.eq('SPAN');
      expect($glyph.attr('aria-hidden')).to.eq('true');
      expect($glyph.attr('tabindex')).to.be.undefined;
      expect($glyph.attr('data-cke-tooltip-text')).to.be.undefined;
      expect($glyph.hasClass('ck-button')).to.eq(false);
    });
  });

  it('highlights the matching toolbar button when a glyph is hovered', () => {
    cy.get('.ck-toolbar .hedy-tool-spotlight').should('not.exist');

    cy.get('#explanation [data-points-to="codeBlock"]').trigger('mouseenter');
    cy.get('.ck-toolbar [data-hedy-tool="codeBlock"]').should('have.class', 'hedy-tool-spotlight');
    cy.get('.ck-toolbar [data-hedy-tool="code"]').should('not.have.class', 'hedy-tool-spotlight');

    cy.get('#explanation [data-points-to="codeBlock"]').trigger('mouseleave');
    cy.get('.ck-toolbar .hedy-tool-spotlight').should('not.exist');
  });

  it('holds the highlight after a click until it times out, for touch devices', () => {
    cy.get('#explanation [data-points-to="code"]').click();
    cy.get('.ck-toolbar [data-hedy-tool="code"]').should('have.class', 'hedy-tool-spotlight');
    cy.get('.ck-toolbar .hedy-tool-spotlight', { timeout: 4000 }).should('not.exist');
  });

  it('drops the highlight as soon as the pointer leaves, even after a click', () => {
    cy.get('#explanation [data-points-to="code"]').click();
    cy.get('.ck-toolbar [data-hedy-tool="code"]').should('have.class', 'hedy-tool-spotlight');

    cy.get('#explanation [data-points-to="code"]').trigger('mouseleave');
    cy.get('.ck-toolbar .hedy-tool-spotlight').should('not.exist');
  });

  it('does not change the adventure content when a glyph is clicked', () => {
    cy.window().then((win) => {
      const before = win.ckEditor.getData();
      cy.get('#explanation [data-points-to="codeBlock"]').click();
      cy.get('#explanation [data-points-to="code"]').click();
      cy.window().should((w) => {
        expect(w.ckEditor.getData()).to.eq(before);
      });
    });
  });
});
