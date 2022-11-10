import {loginForAdmin, loginForTeacher} from '../../tools/login/login.js'
import { createClass } from "../../tools/classes/class";
//import { goToPage } from "../navigation/nav";

describe('Testing individual adventure buttons', () => {
  it('Passes', () => {
    loginForTeacher();
    cy.wait(500);
    
    createClass();
    cy.get(':nth-child(3) > .no-underline').click()
    cy.get('.green-btn').contains("Customize class").click()

    cy.get('#level_button_1').click()
    cy.get('.adventure_level_1').should('be.not.checked')
    cy.get('#level_button_1').click()
    cy.get('.adventure_level_1').should('be.checked')

    cy.get('#level_button_2').click()
    cy.get('.adventure_level_2').should('be.not.checked')
    cy.get('#level_button_2').click()
    cy.get('.adventure_level_2').should('be.checked')

    cy.get('#level_button_3').click()
    cy.get('.adventure_level_3').should('be.not.checked')
    cy.get('#level_button_3').click()
    cy.get('.adventure_level_3').should('be.checked')

    cy.get('#level_button_4').click()
    cy.get('.adventure_level_4').should('be.not.checked')
    cy.get('#level_button_4').click()
    cy.get('.adventure_level_4').should('be.checked')

    cy.get('#level_button_5').click()
    cy.get('.adventure_level_5').should('be.not.checked')
    cy.get('#level_button_5').click()
    cy.get('.adventure_level_5').should('be.checked')

    cy.get('#level_button_6').click()
    cy.get('.adventure_level_6').should('be.not.checked')
    cy.get('#level_button_6').click()
    cy.get('.adventure_level_6').should('be.checked')

    cy.get('#level_button_7').click()
    cy.get('.adventure_level_7').should('be.not.checked')
    cy.get('#level_button_7').click()
    cy.get('.adventure_level_7').should('be.checked')

    cy.get('#level_button_8').click()
    cy.get('.adventure_level_8').should('be.not.checked')
    cy.get('#level_button_8').click()
    cy.get('.adventure_level_8').should('be.checked')

    cy.get('#level_button_9').click()
    cy.get('.adventure_level_9').should('be.not.checked')
    cy.get('#level_button_9').click()
    cy.get('.adventure_level_9').should('be.checked')

    cy.get('#level_button_10').click()
    cy.get('.adventure_level_10').should('be.not.checked')
    cy.get('#level_button_10').click()
    cy.get('.adventure_level_10').should('be.checked')

    cy.get('#level_button_11').click()
    cy.get('.adventure_level_11').should('be.not.checked')
    cy.get('#level_button_11').click()
    cy.get('.adventure_level_11').should('be.checked')

    cy.get('#level_button_12').click()
    cy.get('.adventure_level_12').should('be.not.checked')
    cy.get('#level_button_12').click()
    cy.get('.adventure_level_12').should('be.checked')

    cy.get('#level_button_13').click()
    cy.get('.adventure_level_13').should('be.not.checked')
    cy.get('#level_button_13').click()
    cy.get('.adventure_level_13').should('be.checked')

    cy.get('#level_button_14').click()
    cy.get('.adventure_level_14').should('be.not.checked')
    cy.get('#level_button_14').click()
    cy.get('.adventure_level_14').should('be.checked')

    cy.get('#level_button_15').click()
    cy.get('.adventure_level_15').should('be.not.checked')
    cy.get('#level_button_15').click()
    cy.get('.adventure_level_15').should('be.checked')

    cy.get('#level_button_16').click()
    cy.get('.adventure_level_16').should('be.not.checked')
    cy.get('#level_button_16').click()
    cy.get('.adventure_level_16').should('be.checked')

    cy.get('#level_button_17').click()
    cy.get('.adventure_level_17').should('be.not.checked')
    cy.get('#level_button_17').click()
    cy.get('.adventure_level_17').should('be.checked')

    cy.get('#level_button_18').click()
    cy.get('.adventure_level_18').should('be.not.checked')
    cy.get('#level_button_18').click()
    cy.get('.adventure_level_18').should('be.checked')
    
  })
})