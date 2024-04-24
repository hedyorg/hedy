import {loginForTeacher} from '../../tools/login/login.js'

describe('Is able to preview adventures', () => {
  for (const adv of ["adventure1", "adventure3"]) {
    it(`Passes for ${adv}`, () => {
      loginForTeacher();
      // view the adventures if not opened.
        cy.get("#adventures_table").then($viewAdventure => {
            if (!$viewAdventure.is(':visible')) {
                cy.get("#view_adventures").click();
            }
        });
        // preview adventure3
        cy.get(`[data-cy="preview-${adv}"]`).click();
        // now it should be visible in code-page.
        cy.get(`[data-cy='${adv}']`)
          .should("be.visible")
          .should("contain.text", adv)
        cy.get("#adventures-tab").should("be.visible")
    })
  }
})
