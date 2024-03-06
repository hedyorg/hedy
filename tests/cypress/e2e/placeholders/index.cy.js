import {goToRegisterStudent} from '../tools/navigation/nav.js'
import {login, loginForUser} from '../tools/login/login.js'

describe('Check placeholders', () => {
  it('passes', () => {
    cy.visit("/signup?teacher=true");
    cy.checkForPlaceholders();
  });
});
