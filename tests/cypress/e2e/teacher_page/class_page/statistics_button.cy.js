import {loginForAdmin, loginForTeacher} from '../../tools/login/login.js'
import {createClass} from '../../tools/classes/class.js'


describe('Is able to go back to teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();
    cy.get(":nth-child(1) > :nth-child(3) > .no-underline").click(); // Press view class button

    var currentUrl = '';
    cy.url().then(url => {
      currentUrl = url;
      let statsButton = `[onclick="window.location.href = '/stats/class/` + currentUrl.substring(currentUrl.indexOf('class/')+6) + `'"]`; // Get statistics class button
      cy.get(statsButton).click(); // Press class statistics button

      let statsUrl = '/stats/class/' + currentUrl.substring(currentUrl.indexOf('class/')+6);
      cy.url().should('include', statsUrl); // Check if you are in the statistics page
    })    
  })
})