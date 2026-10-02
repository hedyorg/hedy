import { loginForTeacher } from '../../tools/login/login';

describe('Teacher manual index', () => {
  beforeEach(() => {
    loginForTeacher();
  });

  it('holds the whole manual on one page', () => {
    cy.visit('/for-teachers/manual');

    cy.getDataCy('manual_section').should('have.length', 2);
    cy.get('#manual-intro').should('exist');
    cy.get('#manual-common_mistakes').should('exist');

    // Everything in the index points into this page, so none of it loads another one.
    cy.getDataCy('manual_index').filter(':visible').within(() => {
      cy.get('a').should('have.length.at.least', 20);
      cy.get('a:not([href^="#"])').should('not.exist');
      cy.getDataCy('manual_index_link').first().should('have.attr', 'href', '#manual-intro-1');
    });
  });

  it('sends the links to the old pages of the manual to their place on it', () => {
    cy.request({ url: '/for-teachers/manual/common_mistakes', followRedirect: false })
      .then((response) => {
        expect(response.status).to.eq(302);
        expect(response.redirectedToUrl).to.include('/for-teachers/manual#manual-common_mistakes');
      });
  });

  it('folds a whole section of the manual away, and keeps it away while you read', () => {
    cy.visit('/for-teachers/manual');

    cy.getDataCy('manual_index_section_toggle_common_mistakes').filter(':visible').first().as('toggle');
    cy.get('@toggle').should('have.attr', 'aria-expanded', 'true');
    cy.get('#manual-index-wide-common_mistakes').should('be.visible');

    cy.get('@toggle').click();
    cy.get('@toggle').should('have.attr', 'aria-expanded', 'false');
    cy.get('#manual-index-wide-common_mistakes').should('not.be.visible');

    // Folding a section away is deliberate, so reading inside it does not undo it.
    cy.get('#manual-level-4').scrollIntoView();
    cy.get('@toggle').should('have.attr', 'aria-expanded', 'false');

    cy.get('@toggle').click();
    cy.get('#manual-index-wide-common_mistakes').should('be.visible');
  });

  it('folds the mistakes of a level open and shut', () => {
    cy.visit('/for-teachers/manual');

    cy.getDataCy('manual_index_toggle_1').filter(':visible').first().as('toggle');
    cy.get('@toggle').should('have.attr', 'aria-expanded', 'false');
    cy.get('#manual-index-wide-level-1').should('not.be.visible');

    cy.get('@toggle').click();
    cy.get('@toggle').should('have.attr', 'aria-expanded', 'true');
    cy.get('#manual-index-wide-level-1').should('be.visible')
      .find('a').first().should('have.attr', 'href', '#manual-level-1-mistake-1');

    cy.get('@toggle').click();
    cy.get('#manual-index-wide-level-1').should('not.be.visible');
  });

  it('follows along in the index while the page is scrolled', () => {
    cy.visit('/for-teachers/manual');

    // Nothing has been scrolled yet, so the first entry is the one being read.
    cy.get('a[href="#manual-intro"]').filter(':visible').first()
      .should('have.class', 'manual-index-link-active');

    cy.get('#manual-level-4').scrollIntoView();

    cy.get('a[href="#manual-level-4"]').filter(':visible').first()
      .should('have.class', 'manual-index-link-active');
    cy.get('a[href="#manual-intro"]').filter(':visible').first()
      .should('not.have.class', 'manual-index-link-active');

    // The level being read folds open by itself, so its mistakes are listed.
    cy.get('#manual-index-wide-level-4').should('be.visible');
  });

  it('offers a way back to the top once the top is out of sight', () => {
    cy.visit('/for-teachers/manual');

    cy.getDataCy('manual_to_top').should('not.be.visible');

    cy.get('#manual-level-8').scrollIntoView();
    cy.getDataCy('manual_to_top').should('be.visible').click();

    // Smooth scrolling can leave a fraction of a pixel behind.
    cy.window().its('scrollY').should('be.lessThan', 3);
    cy.getDataCy('manual_to_top').should('not.be.visible');
  });

  it('folds the index away above the text on a narrow screen', () => {
    cy.viewport('iphone-x');
    cy.visit('/for-teachers/manual');

    cy.getDataCy('manual_index_summary').should('be.visible').click();
    cy.getDataCy('manual_index').filter(':visible')
      .find('a[href="#manual-intro-2"]').first().click();

    // Picking an entry folds the index away again, so it stops covering the text.
    cy.getDataCy('manual_index_summary').parent().should('not.have.attr', 'open');
  });
});
