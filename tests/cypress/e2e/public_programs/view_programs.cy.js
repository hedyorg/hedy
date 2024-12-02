import { login } from "../tools/login/login"
import { codeMirrorContent } from "../tools/programs/program";

describe('Tests for viewing programs', () => {
    it('Seeing a program that contains an error in a different language, shouldnt result in a crash', () => {
        login('user2', '123456');
        cy.visit('/hedy/fb23d0fa90ce48b5bf87c0632969fc28/view')
        codeMirrorContent().should('have.text', 'répète 1 foistourne 3    avance 50');
    })
})