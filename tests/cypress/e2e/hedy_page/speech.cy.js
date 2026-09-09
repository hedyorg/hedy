import { goToHedyPage} from "../tools/navigation/nav";

describe('the hedy page', () => {
  beforeEach(() => {
    goToHedyPage({onBeforeLoad(win) {
      cy.stub(win.speechSynthesis, 'getVoices').returns([
        {
          name: "Voice 1",
          lang: "en-US",
          voiceURI: "some-uri"
        },
        {
          name: "Voice 2",
          lang: "en-US",
          voiceURI: "some-other-uri"
        },
        {
          // Should not be selected since we're using English.
          name: "Spanish voice",
          lang: "es-ES",
          voiceURI: "some-other-other-uri"
        },
      ]);
    }});
  });

  it('has the speak controls.', () => {
    cy.get('#speak_dropdown').should('be.visible');
    cy.get('#speak_dropdown > option').should(($options) => {
      expect($options).to.have.length(3);
      expect($options[0]).to.contain('Choose');
      expect($options[1]).to.contain('1');
      expect($options[2]).to.contain('2');
    });
    cy.get('#speak_mute_button').should('be.visible').should('be.disabled').should('have.attr', 'aria-pressed', 'true');
  });

  it('unmutes when choosing a language.', () => {
    cy.get('#speak_dropdown').select(1);
    cy.get('#speak_mute_button').should('be.enabled').should('have.attr', 'aria-pressed', 'false');
  });

  it('mutes when the button is pressed.', () => {
    cy.get('#speak_dropdown').select(1);
    cy.get('#speak_mute_button').click();

    cy.get('#speak_mute_button').should('be.enabled').should('have.attr', 'aria-pressed', 'true');
  });

  it('stays muted when a new language is picked.', () => {
    cy.get('#speak_dropdown').select(1);
    cy.get('#speak_mute_button').click();
    cy.get('#speak_dropdown').select(2);

    cy.get('#speak_mute_button').should('be.enabled').should('have.attr', 'aria-pressed', 'true');
  });

  it('mutes itself when there is no language selected.', () => {
    cy.get('#speak_dropdown').select(1);
    cy.get('#speak_dropdown').select(0);

    cy.get('#speak_mute_button').should('be.disabled').should('have.attr', 'aria-pressed', 'true');
  });
});
