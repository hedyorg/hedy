import { loginForTeacher } from '../../tools/login/login.js'
import { goToPage } from "../../tools/navigation/nav.js";

describe('Teacher page', () => {
  beforeEach(() => {
    loginForTeacher();
    goToPage('/for-teachers/manual');
  });

  it('contains a YouTube video', () => {
    cy.contains('video').should('have.attr', 'href').and('include', 'https://www.youtube.com/watch?v=EdqT313rM40&t=2s');
  });

  it('contains a link to Discord', () => {
    cy.contains('Discord').should('have.attr', 'href').and('include', 'https://discord.gg/8yY7dEme9r');
  });

  it('contains a link to Introduction', () => {
    cy.contains('Introduction').should('be.visible').and('have.attr', 'href');
  });

  it('contains a link to Preparations', () => {
    cy.contains('Preparations').should('be.visible').and('have.attr', 'href');
  });

  it('contains a link to Teaching', () => {
    cy.contains('Teaching').should('be.visible').and('have.attr', 'href');
  });

  it('contains a link to Frequently Made Mistakes', () => {
    cy.contains('Frequently made mistakes').should('be.visible').and('have.attr', 'href');
  });

  it('contains Levels under Frequently Made Mistakes', () => {
    cy.contains('Frequently made mistakes').click();
    cy.contains('Level 1').should('be.visible');
  });
});
