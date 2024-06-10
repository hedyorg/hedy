import {loginForTeacher} from '../../tools/login/login.js'

it('Is able to for teacher page', () => {
  loginForTeacher();
  cy.wait(500);
  cy.location().then((loc) => {
    expect(loc.pathname).to.equal('/for-teachers');
  });
})