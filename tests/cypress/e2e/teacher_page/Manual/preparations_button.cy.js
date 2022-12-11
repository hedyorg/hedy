import {loginForTeacher} from '../../tools/login/login.js'
import {goToPage} from "../../tools/navigation/nav.js";

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    goToPage('/for-teachers/manual');
    cy.get('#button-2').should('be.visible');
    cy.get('#button-2').click();

  })
})
