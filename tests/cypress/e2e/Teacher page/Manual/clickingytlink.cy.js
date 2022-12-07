import {loginForAdmin, loginForTeacher} from '../../tools/login/login.js'
import { goToHome, goToLogin, goToRegister, goToPage } from "../../tools/navigation/nav.js";

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    goToPage('/for-teachers/manual');
    cy.get('#section-1 > :nth-child(3) > a').should('have.attr', 'href').and('include', 'https://www.youtube.com/watch?v=EdqT313rM40&t=2s');


  })
})
