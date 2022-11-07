import {loginForAdmin, loginForTeacher} from '../../tools/login/login.js'
import { goToHome, goToLogin, goToRegister, goToPage } from "../../tools/navigation/nav.js";

describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    goToPage('/for-teachers/manual');
    cy.get('#button-4').click();

    for(let i = 1; i <= 18; i++)
    {
        cy.get('[onclick="$(\'#common_mistakes-' + i +  '\').slideToggle();"]').click();
    }
//
//    cy.get('[onclick="$('#common_mistakes-2').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-3').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-4').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-5').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-6').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-7').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-8').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-9').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-10').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-11').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-12').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-13').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-14').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-15').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-16').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-17').slideToggle();"]').click();
//    cy.get('[onclick="$('#common_mistakes-18').slideToggle();"]').click();




//    cy.location().then((loc) => {
//      expect(loc.pathname).to.equal('/for-teachers');
//    });



  })
})