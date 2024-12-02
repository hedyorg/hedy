import { login, logout } from "../tools/login/login"
import { codeMirrorContent } from "../tools/programs/program";

describe('Tests for viewing programs', () => {
    beforeEach(()=> {
        login('user2', '123456'); // user2 has Dutch language set
        // And we are accessing programs written by user1, that has French set
    })
    it('Seeing a program that contains an error in a different language, shouldnt result in a crash', () => {
        login('user1', '123456')
        cy.visit('/hedy/fb23d0fa90ce48b5bf87c0632969fc28/view')
        codeMirrorContent().should('have.text', 'répète 1 foistourne 3    avance 50');
        logout()
        login('user2', '123456')
        cy.visit('/hedy/fb23d0fa90ce48b5bf87c0632969fc28/view')
        codeMirrorContent().should('have.text', 'répète 1 foistourne 3    avance 50');
    })

    it("We can translate from any two languages that dont involve english", () => {
        login('user1', '123456')
        cy.visit('/hedy/4386f49502344c5cb915b37acb959a27/view')
        codeMirrorContent().should('have.text', 'répète 5 fois    affiche "Salut tout le monde"    affiche"Tout ceci sera répété 5 fois"');
        logout()
        login('user2', '123456')
        cy.visit('/hedy/4386f49502344c5cb915b37acb959a27/view')
        codeMirrorContent().should('have.text', 'herhaal 5 keer    print "Salut tout le monde"    print"Tout ceci sera répété 5 fois"');
    })
})