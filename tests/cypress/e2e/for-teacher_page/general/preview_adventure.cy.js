import {loginForTeacher} from '../../tools/login/login.js'
import { openAdventureView } from '../../tools/classes/class.js';

const adventures = ["adventure1", "adventure3"];

adventures.forEach((adventure) => {
  it('Is able to preview adventures', () => {
    loginForTeacher();
    // view the adventures if not opened.
    openAdventureView();
    // preview adventure3
    cy.getDataCy(`preview_${adventure}`).click();
    // now it should be visible in code-page.
    cy.getDataCy(adventure)
      .should("be.visible")
      .should("contain.text", adventure)
    cy.get("#adventures_tab").should("be.visible")
  })
})
