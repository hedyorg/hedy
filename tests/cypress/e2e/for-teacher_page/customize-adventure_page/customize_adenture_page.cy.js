import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'
import "cypress-real-events"

describe('Test for the Customize Adventure Page', () => {
    beforeEach(() => {
        loginForTeacher();
        goToEditAdventure();
    })
    
    it('Writing an word with several possible keywords should show an alert message, that can be closed', () => {
        cy.get('[data-cke-tooltip-text="Bold (Ctrl+B)"]').click()
        cy.get('[data-cke-tooltip-text="Bold (Ctrl+B)"]').click()
        cy.get('.ck-content[contenteditable=true]').realType('`to`')
        // The warning should be shown now and contain the right suggestions
        cy.get('#warnings_container').should('be.visible').and('contain.text', '{to}, {to_list}')
        // Once we click the close button
        cy.get('p[class="close-dialog"]').click()
        // The alert should not exist anymore
        cy.getBySel('test_warning_message').should('not.exist')
    })   
})
