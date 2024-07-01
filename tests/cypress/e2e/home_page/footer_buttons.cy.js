import { goToHome } from "../tools/navigation/nav";

beforeEach(() => {
  goToHome();
})

describe('Footer buttons', () => {
  it('Is able to subscribe to newsletter', () => {
    cy.getDataCy('subscribe_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/subscribe");
    })
  })

  it('Is able to click on learnmore button', () => {
    cy.getDataCy('learnmore_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/learn-more");
    })
  })

  it('Is able to click on manual button', () => {
    cy.getDataCy('footer_manual_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/for-teachers/manual");
    })
  })

  it('Is able to click on privacy button', () => {
    cy.getDataCy('privacy_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/privacy");
    })
  })
})
