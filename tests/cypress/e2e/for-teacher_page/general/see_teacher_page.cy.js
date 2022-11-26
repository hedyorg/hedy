import {loginForTeacher} from '../../tools/login/login.js'

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    cy.location().then((loc) => {
      expect(loc.pathname).to.equal('/for-teachers');
    });
  })
})