import { loginForTeacher } from "../tools/login/login";
import { goToHome } from "../tools/navigation/nav";

beforeEach(() => {
  goToHome();
})

describe('Navigation buttons', () => {
  it('Is able to click on hedy button', () => {
    cy.getDataCy('hedy_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/hedy");
    })
  })

  it('Is able to click on explore button', () => {
    cy.getDataCy('explore_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/login");
    })
  })

  it('As a teacher, is able to click on explore button, for-teacher button, teacher manual button and go to my programs', () => {
    loginForTeacher();
    cy.getDataCy('explore_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/explore");
    })

    goToHome();
    cy.getDataCy('for_teacher_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/for-teachers");
    })

    goToHome();
    cy.getDataCy('manual_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/for-teachers/manual");
    })

    goToHome();
    cy.getDataCy('programs_button').click();
    
    cy.location().should((loc) => {
      expect(loc.pathname).equal("/programs");
    })
  })
})
