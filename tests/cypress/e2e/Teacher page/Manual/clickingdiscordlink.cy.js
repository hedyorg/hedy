import {loginForAdmin, loginForTeacher} from '../../tools/login/login.js'
import { goToHome, goToLogin, goToRegister, goToPage } from "../../tools/navigation/nav.js";

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    goToPage('/for-teachers/manual');
    cy.get(':nth-child(21) > a').should('have.attr', 'href').and('include', 'https://discord.gg/8yY7dEme9r');

  })
})
