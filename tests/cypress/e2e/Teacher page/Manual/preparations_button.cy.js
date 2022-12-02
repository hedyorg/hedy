import {loginForAdmin, loginForTeacher} from '../../tools/login/login.js'
import { goToHome, goToLogin, goToRegister, goToPage } from "../../tools/navigation/nav.js";

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    goToPage('/for-teachers/manual');
    cy.get('#button-2').should('be.visible');
    cy.get('#button-2').click();

  })
})
