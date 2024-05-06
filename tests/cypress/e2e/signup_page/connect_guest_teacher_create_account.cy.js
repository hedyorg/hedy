import {goToRegisterTeacher} from '../tools/navigation/nav.js'

describe('Check connect with guest teacher', () => {
  it('passes', () => {

    goToRegisterTeacher();

       cy.get('#connect_guest_teacher').check()
      .should('be.visible')

      cy.get('#phone_number')
      .should('be.visible')
  })
})
