import {loginForTeacher, logout} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to see teacher page', () => {
  it('Passes', () => {
    
    loginForTeacher();
    cy.wait(500);
    

    cy.get(':nth-child(1) > #class_view_button').click();

    cy.get('.green-btn').contains("Add students").click();
    cy.get('.green-btn').contains("Copy join link").click();
    
  
    cy.window().then((win) => {
      win.navigator.clipboard.readText().then((text) => {
        expect(text).include('/hedy/l/26EUkkL');
      });
    });
  })
})
