import {loginForTeacher} from '../../tools/login/login.js'
import {goToPage} from "../../tools/navigation/nav.js";

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    goToPage('/for-teachers/manual');
    cy.get(':nth-child(21) > a').should('have.attr', 'href').and('include', 'https://discord.gg/8yY7dEme9r');

  })
})
