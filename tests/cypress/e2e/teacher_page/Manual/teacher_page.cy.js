import { loginForTeacher } from '../../tools/login/login.js'
import { goToPage } from "../../tools/navigation/nav.js";

// The index of the manual has a spec of its own, in
// `for-teacher_page/redesign/manual_index.cy.js`.
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
});
