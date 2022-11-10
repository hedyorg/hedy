import {loginForTeacher} from '../../tools/login/login.js'
import { createClass} from '../../tools/classes/class'
describe('Is able to see teacher page', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    
    createClass();
    cy.get(':nth-child(3) > .no-underline').click();

    cy.get('.green-btn').contains("Add students").click();
    cy.get('.green-btn').contains("Copy join link").click();
    cy.window().then((win) => {
      win.navigator.clipboard.readText().then((text) => {
        expect(text).to.eq('http://localhost:8080/hedy/l/yH8QNXu');
      });
    });
  })
})