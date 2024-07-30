import { navigateHomeButton, goToHome } from "../tools/navigation/nav";

it('Is able to click on all footer buttons', () => {
    navigateHomeButton('subscribe_button', Cypress.env('subscribe_page'))
    navigateHomeButton('learnmore_button', Cypress.env('learn_more_page'))
    navigateHomeButton('footer_manual_button', Cypress.env('manual_page'))
    navigateHomeButton('privacy_button', Cypress.env('privacy_page'))
    // I am not sure how to check a redirect to an external page
    goToHome();
    cy.getDataCy('github_button').should('be.visible')
    cy.getDataCy('sponsor_button').should('be.visible')
    cy.getDataCy('discord_button').should('be.visible')
    cy.getDataCy('translate_button').should('be.visible')
    cy.getDataCy('email_button').should('be.visible')
})
