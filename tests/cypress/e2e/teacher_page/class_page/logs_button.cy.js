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
      let logsButton = `[onclick="window.location.href = '/logs/class/` + currentUrl.substring(currentUrl.indexOf('class/')+6) + `'"]`; // Get logs button
      cy.get(logsButton).click(); // Press logs button

      let statsUrl = '/logs/class/' + currentUrl.substring(currentUrl.indexOf('class/')+6);
      cy.url().should('include', statsUrl); // Check if you are in the logs page
    })    
  })
})