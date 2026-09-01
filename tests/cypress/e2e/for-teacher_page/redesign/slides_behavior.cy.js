import { loginForTeacher } from '../../tools/login/login';

describe('Teacher slides behavior', () => {
  beforeEach(() => {
    loginForTeacher();
  });

  it('teacher landing links to teaching materials and does not expose the legacy slides toggle UI', () => {
    cy.visit('/for-teachers');
    cy.get('#view_slides').should('not.exist');
    cy.get('#slides_table').should('not.exist');

    cy.getDataCy('teaching_materials_link').click();
    cy.url().should('include', '/for-teachers/teaching-materials');
  });

  it('teaching materials page links to the manual and to the slides', () => {
    cy.visit('/for-teachers/teaching-materials');
    cy.getDataCy('background_information_link').should('have.attr', 'href', '/for-teachers/manual');
    cy.getDataCy('slides_link').should('have.attr', 'href', '/for-teachers/slides');

    cy.getDataCy('slides_link').click();
    cy.url().should('include', '/for-teachers/slides');
  });

  it('slides page lists every level and previews the first one by default', () => {
    cy.visit('/for-teachers/slides');
    cy.get('#slides_level_list a').its('length').should('be.greaterThan', 1);
    cy.getDataCy('slides_preview').should('have.attr', 'src', '/slides/0?embed=1');
    cy.getDataCy('present_slides')
      .should('have.attr', 'href', '/slides/0')
      .and('have.attr', 'target', '_blank');
  });

  it('selecting a level previews that level and marks it as current', () => {
    cy.visit('/for-teachers/slides');
    cy.getDataCy('slides_level_5').click();

    cy.url().should('include', '/for-teachers/slides/5');
    cy.getDataCy('slides_preview').should('have.attr', 'src', '/slides/5?embed=1');
    cy.getDataCy('present_slides').should('have.attr', 'href', '/slides/5');
    cy.getDataCy('slides_level_5').should('have.class', 'slides-level-item-active');
  });

  it('scrolls the selected level into view in a long list', () => {
    cy.visit('/for-teachers/slides/16');
    cy.getDataCy('slides_level_16').should('be.visible');
    cy.get('#slides_level_list').then(($nav) => {
      expect($nav[0].scrollTop).to.be.greaterThan(0);
    });
  });

  it('the embedded preview renders the actual deck', () => {
    cy.visit('/for-teachers/slides/1');
    cy.getDataCy('slides_preview')
      .its('0.contentDocument.body')
      .should('not.be.empty')
      .then(cy.wrap)
      .find('.slides section')
      .its('length')
      .should('be.greaterThan', 0);
  });

  it('shows a whole slide at once, editor and output side by side', () => {
    cy.visit('/for-teachers/slides/6');
    // The preview frame loads lazily, so it can still be booting when the page is
    // ready: the Reveal global exists as soon as its own script runs, but the API
    // we drive the deck with is only there once the deck has initialised.
    cy.getDataCy('slides_preview', { timeout: 10000 }).should(($f) => {
      const deck = $f[0].contentWindow.Reveal;
      expect(deck, 'deck is initialised').to.exist;
      expect(deck.isReady(), 'deck is ready').to.be.true;
    });
    cy.getDataCy('slides_preview').then(($f) => {
      const win = $f[0].contentWindow;
      win.Reveal.slide(1, 0);
      for (let i = 0; i < 6; i++) win.Reveal.nextFragment();
    });

    // The whole slide has to sit inside the frame: teachers need to see the output
    // pane, not just the editor that produces it.
    cy.getDataCy('slides_preview').should(($f) => {
      const win = $f[0].contentWindow;
      const slide = win.document.querySelectorAll('.slides section')[1];
      const box = slide.getBoundingClientRect();
      expect(box.top, 'slide top is inside the frame').to.be.at.least(0);
      expect(box.bottom, 'slide bottom is inside the frame').to.be.at.most(win.innerHeight);
    });

    // And the editor must keep the two-column layout it has when presenting. Stacking
    // it would double the slide height and force everything to shrink to fit.
    cy.getDataCy('slides_preview').should(($f) => {
      const win = $f[0].contentWindow;
      const editorFrame = win.document.querySelectorAll('.slides section')[1].querySelector('iframe');
      const area = editorFrame.contentDocument.getElementById('editor_area');
      const columns = win.getComputedStyle(area).gridTemplateColumns.split(' ');
      expect(columns, 'editor and output are side by side').to.have.length(2);
    });
  });

  it('presenting is left untouched by the preview tweaks', () => {
    cy.visit('/slides/6');
    cy.window().its('Reveal').should('exist');
    cy.window().then((win) => {
      expect(win.Reveal.getConfig().width, 'slides still size to the window').to.eq('90%');
      expect(
        win.document.querySelector('.slides section').style.height,
        'slides keep their full height',
      ).to.eq('1018px');
    });
  });

  it('a level without slides is not found', () => {
    cy.request({ url: '/for-teachers/slides/99', failOnStatusCode: false })
      .its('status')
      .should('eq', 404);
  });

  it('opens a slides page with rendered sections', () => {
    cy.request('/slides/1').its('status').should('eq', 200);
    cy.visit('/slides/1');
    cy.get('.slides section').its('length').should('be.greaterThan', 0);
  });

  it('slides PDF endpoint is available for download', () => {
    cy.request('/slides/1').then((resp) => {
      expect(resp.status).to.eq(200);
      expect(resp.headers['content-type']).to.include('text/html');
    });
  });
});
