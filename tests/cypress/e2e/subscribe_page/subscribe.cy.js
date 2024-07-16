import { goToSubscribePage } from "../tools/navigation/nav";

it('Is able to subscribe to newsletter', () => {
    goToSubscribePage()
    cy.getDataCy('name').type('test')
    cy.getDataCy('lastname').type('test')
    cy.getDataCy('email').type('testsubscribetonewsletter@gmail.com')
    cy.getDataCy('role').select('Teacher')
    cy.getDataCy('language').select('Dansk')
    // I am not sure how to check the redirect to https://hedycode.us7.list-manage.com/...
    cy.getDataCy('subscribe').should('be.visible');
})
