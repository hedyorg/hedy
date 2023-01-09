import {loginForTeacher} from '../../tools/login/login.js'
import {goToPage} from "../../tools/navigation/nav.js";

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    goToPage('/for-teachers/manual');
    cy.contains('Frequently made mistakes').should('be.visible');
    cy.contains('Frequently made mistakes').click();

  })
})
