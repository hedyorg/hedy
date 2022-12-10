import { loginForTeacher } from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";

describe('Testing individual adventure buttons', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    createClass();

    cy.get(".view_class").first().click(); // Press on view class button

    cy.get('#customize-class-button').click(); // Press customize class button

    // check every individual level button with for loop:
    var levelarray = Array.from({length:18},(v, k)=>k+1) // length reflects how many levels there are
    cy.wrap(levelarray).each((index) => {
      cy.get("#level_button_" + index).click()
      cy.get('.adventure_level_' + index).should('be.not.checked')
      cy.get('#level_button_' + index).click()
      cy.get('.adventure_level_' + index).should('be.checked')
    })
    
  })
})