import {loginForTeacher, logout} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to see teacher page', () => {
  it('Passes', () => {
    
    loginForTeacher();
    cy.wait(500);
    

    cy.get('#class_view_button').click();

    cy.get('#add-student').click();
    cy.get('#copy-join-link').click();
    
  
    cy.window().then((win) => {
      win.navigator.clipboard.readText().then((text) => {
        expect(text).include('/hedy/l/26EUkkL');
      });
    });
  })
})
