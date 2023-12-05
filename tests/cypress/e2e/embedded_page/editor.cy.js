describe('Is able to type in the editor box', () => {
    cy.visit(`${Cypress.env('embedded_page')}`);

    // click on textaread to get focus, then clear it
    codeMirrorContent().click();
    clearViaBackspace();

    cy.focused().type('print Hello world');
    codeMirrorContent().should('have.text', 'print Hello world');
    cy.get('#runit').click();
    cy.get('#output').should('contain.text', 'Hello world');
});

describe('Is able to render url parsed program', () => {
    // The following base64 string contains the program 'print Hello world'


    cy.visit(`${Cypress.env('embedded_page')}`);
    codeMirrorContent().should('have.text', 'print Hello world');
});
