import {loginForTeacher} from '../../tools/login/login.js'
import {goToEditAdventure} from '../../tools/navigation/nav.js'

describe('Add to class checkbox test', () => {
  it('passes', () => {
    loginForTeacher();
    goToEditAdventure();

    // Tests the first class out of all the classes we can add to
    // It does not matter which one we take (we choose the first one)
    cy.get(':nth-child(1) > .customize_adventure_class_checkbox')
      .should('be.visible')
      .should('not.be.disabled')
      .check()
      .should('be.checked')
      .uncheck()
      .should('not.be.checked');
  })
})
